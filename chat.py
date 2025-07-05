import json
import re
from typing import Dict, List, Optional

class RuleBasedChatbot:
    def __init__(self, intents_file: str = 'intents.json'):
        """Initialize the chatbot with intents from JSON file"""
        self.intents = self.load_intents(intents_file)
        
    def load_intents(self, filename: str) -> Dict:
        """Load intents from JSON file"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: {filename} not found!")
            return {"intents": []}
    
    def preprocess_message(self, message: str) -> str:
        """Clean and normalize user input"""
        # Convert to lowercase and remove extra spaces
        message = message.lower().strip()
        # Remove punctuation except apostrophes
        message = re.sub(r'[^\w\s\']', ' ', message)
        # Remove extra whitespace
        message = ' '.join(message.split())
        return message
    
    def calculate_keyword_score(self, user_message: str, keywords: List[str]) -> float:
        """Calculate how well the message matches the keywords"""
        if not keywords:
            return 0.0
            
        user_words = set(user_message.split())
        keyword_matches = 0
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            # Exact word match
            if keyword_lower in user_words:
                keyword_matches += 2
            # Partial match (substring)
            elif keyword_lower in user_message:
                keyword_matches += 1
                
        # Return percentage match
        return (keyword_matches / len(keywords)) * 100
    
    def find_best_intent(self, user_message: str) -> Optional[Dict]:
        """Find the best matching intent based on keywords"""
        preprocessed_message = self.preprocess_message(user_message)
        best_intent = None
        best_score = 0
        
        for intent in self.intents.get('intents', []):
            keywords = intent.get('keywords', [])
            score = self.calculate_keyword_score(preprocessed_message, keywords)
            
            # Also check exact pattern matches
            for pattern in intent.get('patterns', []):
                if pattern.lower() in preprocessed_message:
                    score += 50  # Boost score for pattern matches
            
            if score > best_score and score > 10:  # Minimum threshold
                best_score = score
                best_intent = intent
                
        return best_intent
    
    def get_response(self, user_message: str) -> str:
        """Get chatbot response for user message"""
        if not user_message.strip():
            return "I'm here to help! Please ask me something."
        
        # Find matching intent
        intent = self.find_best_intent(user_message)
        
        if intent:
            responses = intent.get('responses', [])
            if responses:
                import random
                return random.choice(responses)
        
        # Default fallback response
        return "I'm sorry, I didn't understand that. Could you please rephrase your question?"

# Initialize global chatbot instance
chatbot = RuleBasedChatbot()

def get_chatbot_response(message: str) -> str:
    """Main function to get chatbot response"""
    return chatbot.get_response(message)
