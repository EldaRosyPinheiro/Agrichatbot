import json
import os
from .utils import find_best_match

class AgricultureKnowledgeBase:
    def __init__(self):
        self.knowledge = self._load_knowledge()
    
    def _load_knowledge(self):
        """Load agriculture knowledge from JSON files"""
        knowledge = {
            'crops': {},
            'pests': {},
            'soil': {},
            'weather': {},
            'general': {}
        }
        
        # Load from files if they exist, otherwise use default data
        try:
            # Try to load from data files
            crops_file = os.path.join('data', 'crops_data.json')
            if os.path.exists(crops_file):
                with open(crops_file, 'r') as f:
                    knowledge['crops'] = json.load(f)
            else:
                knowledge['crops'] = self._get_default_crops_data()
                
        except Exception as e:
            print(f"Warning: Could not load knowledge files, using defaults: {e}")
            knowledge = self._get_default_knowledge()
        
        return knowledge
    
    def search(self, query, topic=None):
        """Search for relevant information"""
        query_lower = query.lower()
        
        if topic and topic in self.knowledge:
            # Search within specific topic
            topic_data = self.knowledge[topic]
            
            # Find best match
            best_match = None
            highest_score = 0
            
            for key, value in topic_data.items():
                score = self._calculate_relevance(query_lower, key, value)
                if score > highest_score:
                    highest_score = score
                    best_match = value
            
            return best_match if highest_score > 0 else None
        
        # Search across all topics
        best_result = None
        highest_score = 0
        
        for topic_name, topic_data in self.knowledge.items():
            for key, value in topic_data.items():
                score = self._calculate_relevance(query_lower, key, value)
                if score > highest_score:
                    highest_score = score
                    best_result = value
        
        return best_result if highest_score > 0 else None
    
    def _calculate_relevance(self, query, key, data):
        """Calculate relevance score between query and data"""
        score = 0
        
        # Check key match
        if any(word in key.lower() for word in query.split()):
            score += 2
        
        # Check content match
        if isinstance(data, dict):
            for field, content in data.items():
                if isinstance(content, str) and any(word in content.lower() for word in query.split()):
                    score += 1
        elif isinstance(data, str):
            if any(word in data.lower() for word in query.split()):
                score += 1
        
        return score
    
    def _get_default_crops_data(self):
        """Default crop information"""
        return {
            'rice': {
                'name': 'Rice',
                'description': 'Rice is a staple cereal grain and one of the most important crops worldwide.',
                'growing_tips': '• Plant in flooded fields\n• Requires warm climate\n• 120-150 days to maturity\n• pH 5.5-6.5 preferred',
                'season': 'Monsoon season (June-October)',
                'pests': ['Brown planthopper', 'Rice stem borer', 'Blast disease']
            },
            'wheat': {
                'name': 'Wheat',
                'description': 'Wheat is a cereal grain that is a worldwide staple food.',
                'growing_tips': '• Cool, dry climate preferred\n• Well-drained soil\n• 100-130 days to harvest\n• pH 6.0-7.0 optimal',
                'season': 'Winter season (November-April)',
                'pests': ['Aphids', 'Rust diseases', 'Hessian fly']
            },
            'tomato': {
                'name': 'Tomato',
                'description': 'Tomatoes are versatile fruits used in cooking worldwide.',
                'growing_tips': '• Warm weather crop\n• Rich, well-drained soil\n• Regular watering\n• Support with stakes',
                'season': 'Summer season (March-June)',
                'pests': ['Tomato hornworm', 'Aphids', 'Blight diseases']
            },
            'potato': {
                'name': 'Potato',
                'description': 'Potatoes are underground tubers that are a major food crop.',
                'growing_tips': '• Cool weather preferred\n• Loose, fertile soil\n• Hill up plants regularly\n• Consistent moisture',
                'season': 'Winter season (October-February)',
                'pests': ['Colorado potato beetle', 'Late blight', 'Aphids']
            },
            'corn': {
                'name': 'Corn (Maize)',
                'description': 'Corn is a cereal grain that serves as food for humans and livestock.',
                'growing_tips': '• Warm season crop\n• Full sun exposure\n• Rich, well-drained soil\n• Adequate spacing for pollination',
                'season': 'Summer season (April-August)',
                'pests': ['Corn borer', 'Armyworm', 'Corn smut']
            }
        }
    
    def _get_default_knowledge(self):
        """Get default knowledge base"""
        return {
            'crops': self._get_default_crops_data(),
            'pests': {
                'aphids': {
                    'name': 'Aphids',
                    'description': 'Small, soft-bodied insects that feed on plant sap.',
                    'treatment': 'Use neem oil spray, introduce ladybugs, or use insecticidal soap.',
                    'prevention': 'Regular inspection, avoid over-fertilization'
                },
                'caterpillars': {
                    'name': 'Caterpillars',
                    'description': 'Larvae of moths and butterflies that eat plant leaves.',
                    'treatment': 'Hand picking, Bt spray, or appropriate insecticides.',
                    'prevention': 'Row covers, companion planting'
                }
            },
            'soil': {
                'ph_testing': {
                    'description': 'Soil pH affects nutrient availability to plants.',
                    'recommendations': 'Test pH annually. Most crops prefer pH 6.0-7.0. Use lime to raise pH, sulfur to lower it.'
                },
                'composting': {
                    'description': 'Composting creates rich organic matter for soil improvement.',
                    'recommendations': 'Mix green and brown materials, maintain moisture, turn regularly for aeration.'
                }
            },
            'weather': {
                'seasonal_planning': {
                    'description': 'Planning crops according to seasonal weather patterns.',
                    'recommendations': 'Plant warm-season crops after last frost, cool-season crops in fall/winter.'
                }
            },
            'general': {
                'organic_farming': {
                    'description': 'Farming without synthetic chemicals, focusing on natural methods.',
                    'recommendations': 'Use compost, crop rotation, biological pest control, and cover crops.'
                }
            }
        }
