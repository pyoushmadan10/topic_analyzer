from nltk.corpus import stopwords
from urllib.parse import urlparse


class StopwordManager:
    def __init__(self, url):
        self.url = url
        try:
            self.stop_words = set(stopwords.words("english"))
        except Exception as e:
            print(f"Error loading NLTK stopwords: {e}")
            self.stop_words = set()
        try:
            self.url_keywords = self.extract_url_keywords()
        except Exception as e:
            print(f"Error extracting URL keywords: {e}")
            self.url_keywords = set()
        try:
            self._initialize_stopwords()
        except Exception as e:
            print(f"Error initializing stopwords: {e}")

    def extract_url_keywords(self):
        """Extract company/brand names from URL to filter them out."""
        url_keywords = set()
        try:
            parsed_url = urlparse(self.url)
            domain = parsed_url.netloc.lower().replace('www.', '')
            
            # Extract domain parts
            domain_parts = domain.split('.')
            for part in domain_parts:
                if len(part) > 2 and part not in ['com', 'org', 'net', 'co', 'uk', 'in', 'de', 'fr']:
                    url_keywords.add(part)
                    url_keywords.add(part.capitalize())
        except Exception as e:
            print(f"Error parsing URL for keywords: {e}")
        return url_keywords

    def _initialize_stopwords(self):
        """Initialize stopwords with additional custom words."""
        additional_stopwords = [
            'buy', 'shop', 'product', 'item', 'brand', 'model', 'said', 'says',
            'would', 'could', 'also', 'one', 'two', 'get', 'make', 'take', 'go',
            'come', 'see', 'know', 'think', 'want', 'use', 'work', 'way', 'new',
            'good', 'first', 'last', 'long', 'great', 'little', 'own', 'other',
            'old', 'right', 'big', 'high', 'different', 'small', 'large', 'next',
            'early', 'young', 'important', 'few', 'public', 'bad', 'same', 'able',
            'day', 'time', 'year', 'look', 'find', 'give', 'tell', 'become',
            'today', 'home', 'page', 'website', 'site', 'click', 'here', 'more',
            'information', 'contact', 'email', 'phone', 'address', 'privacy'
        ]
        try:
            self.stop_words.update(additional_stopwords)
            self.stop_words.update(self.url_keywords)
        except Exception as e:
            print(f"Error updating stopwords: {e}")

    def is_stopword(self, word):
        """Check if a word is a stopword."""
        try:
            return word.lower() in self.stop_words
        except Exception as e:
            print(f"Error checking stopword: {e}")
            return False

    def get_stopwords(self):
        """Get all stopwords."""
        try:
            return self.stop_words
        except Exception as e:
            print(f"Error getting stopwords: {e}")
            return set()