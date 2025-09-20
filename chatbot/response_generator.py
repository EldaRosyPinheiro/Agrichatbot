import json
import os
from datetime import datetime
from .knowledge_base import AgricultureKnowledgeBase
from .utils import clean_text
import google.generativeai as genai
import random
import requests


class AgricultureBot:
    def __init__(self):
        # Configure Gemini API client
        self.model = None
        self.chat = None
        try:
            genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
            # Use your .env GEMINI_MODEL if needed
            model_name = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
            self.model = genai.GenerativeModel(model_name)
            self.chat = self.model.start_chat(history=[
                {
                    "role": "user",
                    "parts": [
                        """You are a friendly and knowledgeable Agriculture Assistant. 
                        Your goal is to provide helpful, accurate, and concise information about farming, 
                        crops, soil, pests, and weather. 
                        When weather data is provided, analyze and explain it for the farmer. 
                        Format answers clearly and use emojis where appropriate."""
                    ]
                },
                {
                    "role": "model",
                    "parts": [
                        "Understood! I am ready to assist with any agriculture-related questions. 🌱"
                    ]
                }
            ])
        except Exception as e:
            print(f"Error configuring Gemini API: {e}")

        # Initialize greeting patterns
        self.greetings = [
            "Hello! I'm your Agriculture Assistant. How can I help you with farming today?",
            "Hi there! I'm here to help with all your agriculture and farming questions.",
            "Welcome! Ask me anything about crops, cultivation, pests, or farming techniques."
        ]

        self.knowledge_base = AgricultureKnowledgeBase()

        # Common patterns for different topics
        self.topic_patterns = {
            'crops': ['crop', 'crops', 'plant', 'plants', 'grow', 'cultivation', 'farming'],
            'pests': ['pest', 'pests', 'insect', 'insects', 'bug', 'bugs', 'disease', 'diseases'],
            'soil': ['soil', 'fertilizer', 'fertiliser', 'nutrients', 'ph', 'compost'],
            'weather': ['weather', 'rain', 'season', 'climate', 'temperature', 'humidity', 'pressure', 'forecast'],
            'seeds': ['seed', 'seeds', 'planting', 'sowing', 'germination'],
            'harvest': ['harvest', 'harvesting', 'yield', 'production', 'storage']
        }

    def get_response(self, user_input):
        """Generate response based on user input"""
        user_input = clean_text(user_input.lower())

        # Greetings
        if self._is_greeting(user_input):
            return random.choice(self.greetings)
        # Goodbyes
        elif self._is_goodbye(user_input):
            return "Thank you for using Agriculture Assistant! Happy farming! 🌱"
        # Weather queries (ThingSpeak + Gemini explanation)
        elif any(word in user_input for word in self.topic_patterns['weather']):
            weather_info = self.get_weather()
            if weather_info:
                context = {
                    "temperature": weather_info["temperature"],
                    "humidity": weather_info["humidity"],
                    "pressure": weather_info["pressure"]
                }
                return self._get_ai_response(
                    f"User asked about weather. Current sensor readings are: "
                    f"Temperature: {weather_info['temperature']}°C, "
                    f"Humidity: {weather_info['humidity']}%, "
                    f"Pressure: {weather_info['pressure']} hPa. "
                    f"Explain what this means for farming."
                )
            else:
                return "Sorry, I couldn't fetch the live weather data from ThingSpeak right now. Please try again later."
        # Agriculture queries (crops, soil, pests, etc.)
        else:
            return self._process_agriculture_query(user_input)

    def _is_greeting(self, text):
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']
        return any(greeting in text for greeting in greetings)

    def _is_goodbye(self, text):
        goodbyes = ['bye', 'goodbye', 'see you', 'thanks', 'thank you', 'exit', 'quit']
        return any(goodbye in text for goodbye in goodbyes)

    def _process_agriculture_query(self, user_input):
        """Process queries with optional knowledge base context"""
        topic = self._identify_topic(user_input)
        context_info = self.knowledge_base.search(user_input, topic) if topic else None
        return self._get_ai_response(user_input, context_info)

    def _get_ai_response(self, user_input, context=None):
        """Generate response using Gemini AI"""
        if not self.chat:
            return "I'm sorry, my AI capabilities are currently offline. Please try again later."

        prompt = f"User question: '{user_input}'"
        if context:
            context_str = json.dumps(context, indent=2)
            prompt += f"\n\nHere is some relevant context:\n{context_str}"

        try:
            response = self.chat.send_message(prompt)
            text = response.text
            if text.startswith("```markdown"):
                text = text.replace("```markdown\n", "").replace("\n```", "")
            return text
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return "I'm sorry, I'm having trouble connecting to my knowledge source right now. Please try again later."

    def _identify_topic(self, text):
        """Identify main topic based on keywords"""
        topic_scores = {}
        for topic, keywords in self.topic_patterns.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                topic_scores[topic] = score
        if topic_scores:
            return max(topic_scores.items(), key=lambda x: x[1])[0]
        return None

    def get_timestamp(self):
        return datetime.now().isoformat()

    def get_weather(self):
        """Fetch latest weather from ThingSpeak channel"""
        channel_id = os.environ.get("THINGSPEAK_WEATHER_CHANNEL")
        if not channel_id:
            return None

        url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json?results=1"
        try:
            response = requests.get(url)
            data = response.json()
            feeds = data.get("feeds")
            if not feeds or len(feeds) == 0:
                return None

            latest = feeds[0]
            weather_info = {
                "temperature": latest.get("field1"),
                "humidity": latest.get("field2"),
                "pressure": latest.get("field3", "N/A")
            }
            return weather_info
        except Exception as e:
            print(f"ThingSpeak API error: {e}")
            return None
