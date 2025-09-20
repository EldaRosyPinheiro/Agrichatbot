import re
import string

def clean_text(text):
    """Clean and normalize text"""
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text

def remove_punctuation(text):
    """Remove punctuation from text"""
    return text.translate(str.maketrans('', '', string.punctuation))

def find_best_match(query, options):
    """Find the best matching option for a query"""
    query_words = set(clean_text(query).split())
    best_match = None
    highest_score = 0
    
    for option in options:
        option_words = set(clean_text(str(option)).split())
        
        # Calculate Jaccard similarity
        intersection = len(query_words.intersection(option_words))
        union = len(query_words.union(option_words))
        
        if union > 0:
            score = intersection / union
            if score > highest_score:
                highest_score = score
                best_match = option
    
    return best_match if highest_score > 0.1 else None

def extract_keywords(text):
    """Extract important keywords from text"""
    # Common agriculture-related keywords
    agriculture_keywords = [
        'crop', 'crops', 'plant', 'plants', 'farming', 'agriculture',
        'soil', 'fertilizer', 'pest', 'pests', 'disease', 'diseases',
        'seed', 'seeds', 'harvest', 'grow', 'growing', 'cultivation',
        'weather', 'rain', 'season', 'water', 'irrigation',
        'organic', 'pesticide', 'herbicide', 'compost'
    ]
    
    words = clean_text(text).split()
    keywords = [word for word in words if word in agriculture_keywords]
    
    return list(set(keywords))  # Remove duplicates

def is_agriculture_related(text):
    """Check if text is related to agriculture"""
    keywords = extract_keywords(text)
    return len(keywords) > 0

def format_response_with_emojis(text, topic=None):
    """Add appropriate emojis based on topic"""
    emoji_map = {
        'crops': '🌱',
        'pests': '🐛',
        'soil': '🌾',
        'weather': '🌧️',
        'seeds': '🌰',
        'harvest': '📦',
        'water': '💧',
        'organic': '🌿'
    }
    
    if topic and topic in emoji_map:
        return f"{emoji_map[topic]} {text}"
    
    # Auto-detect topic from text
    text_lower = text.lower()
    for topic, emoji in emoji_map.items():
        if topic in text_lower:
            return f"{emoji} {text}"
    
    return f"🌾 {text}"  # Default agriculture emoji

def validate_input(text, max_length=500):
    """Validate user input"""
    if not text or not text.strip():
        return False, "Please enter a message"
    
    if len(text) > max_length:
        return False, f"Message too long. Please keep it under {max_length} characters"
    
    # Check for inappropriate content (basic check)
    inappropriate_words = ['spam', 'hack', 'virus']  # Add more as needed
    if any(word in text.lower() for word in inappropriate_words):
        return False, "Please keep the conversation focused on agriculture"
    
    return True, "Valid input"

def get_crop_season_info(crop_name):
    """Get seasonal information for crops"""
    crop_seasons = {
        'rice': 'Monsoon (June-October)',
        'wheat': 'Winter (November-April)', 
        'corn': 'Summer (April-August)',
        'tomato': 'Summer (March-June)',
        'potato': 'Winter (October-February)',
        'onion': 'Winter (November-March)',
        'cotton': 'Summer (April-September)',
        'sugarcane': 'Year-round (plant February-March)',
        'soybean': 'Monsoon (June-September)',
        'mustard': 'Winter (October-January)'
    }
    
    return crop_seasons.get(crop_name.lower(), 'Season information not available')

def calculate_similarity(text1, text2):
    """Calculate text similarity using simple word overlap"""
    words1 = set(clean_text(text1).split())
    words2 = set(clean_text(text2).split())
    
    if not words1 or not words2:
        return 0
    
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))
    
    return intersection / union if union > 0 else 0
