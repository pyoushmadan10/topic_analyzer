import re
from content_fetcher import ContentFetcher
from stopword_manager import StopwordManager


class TopicExtractor:
    def __init__(self, url, nlp_model):
        self.url = url
        self.nlp = nlp_model
        try:
            self.content_fetcher = ContentFetcher(url)
        except Exception as e:
            print(f"Error initializing ContentFetcher: {e}")
            self.content_fetcher = None
        try:
            self.stopword_manager = StopwordManager(url)
        except Exception as e:
            print(f"Error initializing StopwordManager: {e}")
            self.stopword_manager = None

    def should_filter(self, text):
        """Check if text should be filtered out."""
        try:
            text_lower = text.lower().strip()
            
            # Filter URL keywords
            if self.stopword_manager and any(url_kw.lower() in text_lower for url_kw in self.stopword_manager.url_keywords):
                return True
            
            # Filter domain extensions
            if self.content_fetcher and self.content_fetcher.has_domain_extension(text):
                return True
            
            # Filter stop words
            if self.stopword_manager and self.stopword_manager.is_stopword(text_lower):
                return True
            
            # Filter generic web terms
            web_terms = ['website', 'homepage', 'login', 'account', 'download', 'browse']
            if any(term in text_lower for term in web_terms):
                return True
            
            return False
        except Exception as e:
            print(f"Error in should_filter: {e}")
            return False

    def clean_phrase(self, phrase):
        """Clean and normalize phrases."""
        try:
            phrase = re.sub(r'\s+', ' ', phrase.strip())
            phrase = re.sub(r'^(the|a|an)\s+', '', phrase, flags=re.IGNORECASE)
            return phrase.title() if phrase else ""
        except Exception as e:
            print(f"Error cleaning phrase: {e}")
            return ""

    def extract_from_text(self, text, priority_multiplier=1.0):
        """Extract topics from text using spaCy."""
        try:
            if not text or len(text.strip()) < 3:
                return {}
            
            topics = {}
            doc = self.nlp(text)
            
            # Named entities
            for ent in doc.ents:
                if (ent.label_ in ['PERSON', 'ORG', 'GPE', 'PRODUCT', 'WORK_OF_ART'] and
                    len(ent.text.strip()) > 2 and
                    not self.should_filter(ent.text)):
                    
                    clean_topic = ' '.join(ent.text.split())
                    topics[clean_topic] = 80.0 * priority_multiplier
            
            # Noun phrases
            for chunk in doc.noun_chunks:
                clean_chunk = self.clean_phrase(chunk.text)
                if (clean_chunk and 
                    len(clean_chunk) > 2 and 
                    len(clean_chunk.split()) <= 4 and
                    not self.should_filter(clean_chunk)):
                    
                    confidence = 60.0 * priority_multiplier
                    if len(clean_chunk.split()) > 1:
                        confidence *= 1.3
                    topics[clean_chunk] = max(topics.get(clean_chunk, 0), confidence)
            
            # Important words
            for token in doc:
                if (token.pos_ in ['NOUN', 'PROPN', 'ADJ'] and
                    not token.is_stop and
                    len(token.text) > 3 and
                    token.is_alpha and
                    not self.should_filter(token.text)):
                    
                    word = token.text.title()
                    confidence = 40.0 * priority_multiplier
                    if token.pos_ == 'PROPN':
                        confidence *= 1.5
                    topics[word] = max(topics.get(word, 0), confidence)
            
            return topics
        except Exception as e:
            print(f"Error extracting from text: {e}")
            return {}

    def extract_topics_with_priority(self):
        """Extract topics with priority-based scoring."""
        try:
            all_topics = {}
            
            # Title topics (10x priority)
            if self.content_fetcher and self.content_fetcher.title_text:
                title_topics = self.extract_from_text(self.content_fetcher.title_text, 10.0)
                all_topics.update(title_topics)
            
            # Heading topics (5x priority)
            if self.content_fetcher and self.content_fetcher.heading_text:
                heading_topics = self.extract_from_text(self.content_fetcher.heading_text, 5.0)
                for topic, score in heading_topics.items():
                    all_topics[topic] = max(all_topics.get(topic, 0), score)
            
            # Body topics (1x priority)
            if self.content_fetcher and self.content_fetcher.body_text:
                body_topics = self.extract_from_text(self.content_fetcher.body_text[:2000], 1.0)
                for topic, score in body_topics.items():
                    all_topics[topic] = max(all_topics.get(topic, 0), score)
            
            return all_topics
        except Exception as e:
            print(f"Error extracting topics with priority: {e}")
            return {}

    def remove_duplicates(self, topics):
        """Remove overlapping topics."""
        try:
            sorted_topics = sorted(topics.items(), key=lambda x: (x[1], len(x[0])), reverse=True)
            filtered_topics = {}
            
            for topic, score in sorted_topics:
                is_duplicate = False
                for existing in filtered_topics.keys():
                    # Check for substring overlap
                    if (topic.lower() in existing.lower() or 
                        existing.lower() in topic.lower()):
                        is_duplicate = True
                        break
                
                if not is_duplicate:
                    filtered_topics[topic] = score
            
            return filtered_topics
        except Exception as e:
            print(f"Error removing duplicates: {e}")
            return topics

    def analyze_and_extract_topics(self, n_topics=5):
        """Main extraction method."""
        try:
            if not self.content_fetcher or not self.content_fetcher.fetch_and_extract_text():
                return [("Could not analyze page.", 0)]

            print("Extracting topics with priority scoring...")
            all_topics = self.extract_topics_with_priority()
            
            if not all_topics:
                return [("No topics found.", 0)]
            
            # Remove duplicates
            filtered_topics = self.remove_duplicates(all_topics)
            
            # Normalize scores to 0-100
            if filtered_topics:
                max_score = max(filtered_topics.values())
                min_score = min(filtered_topics.values())
                
                normalized_topics = []
                for topic, score in filtered_topics.items():
                    if max_score > min_score:
                        normalized_score = ((score - min_score) / (max_score - min_score)) * 80 + 20
                    else:
                        normalized_score = 50
                    normalized_topics.append((topic, min(100, normalized_score)))
            else:
                normalized_topics = []
            
            # Sort by confidence (High to Low)
            final_topics = sorted(normalized_topics, key=lambda x: x[1], reverse=True)
            return final_topics[:n_topics]
        except Exception as e:
            print(f"Error in analyze_and_extract_topics: {e}")
            return [("Error analyzing topics.", 0)]