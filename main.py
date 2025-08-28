from utils import download_nltk_dependencies, load_spacy_model
from topic_extractor import TopicExtractor


class PriorityTopicExtractor:
    def __init__(self, url):
        self.url = url
        # Initialize dependencies
        download_nltk_dependencies()
        self.nlp = load_spacy_model()
        
        # Initialize the topic extractor
        self.topic_extractor = TopicExtractor(url, self.nlp)

    def analyze_and_extract_topics(self, n_topics=5):
        """Main extraction method."""
        return self.topic_extractor.analyze_and_extract_topics(n_topics)


def run_topic_analysis(url, n_topics=5):
    """Run the topic analysis and display results."""
    print(f"Analyzing URL: {url}")
    print("=" * 80)
    try:
        extractor = PriorityTopicExtractor(url)
        topics = extractor.analyze_and_extract_topics(n_topics)
    except Exception as e:
        print(f"Error during topic analysis: {e}")
        print("\n" + "=" * 80)
        print("Analysis failed!")
        return []

    print("\n" + "--- Topics Ranked by Confidence (High to Low) ---".center(80))
    if topics and topics[0][1] > 0:
        for i, (topic, confidence) in enumerate(topics, 1):
            print(f"{i:2}. {topic:<50} | Confidence: {confidence:.1f}%")
    else:
        print("  - No topics could be extracted.")
    
    print("\n" + "=" * 80)
    print("Analysis complete!")
    return topics


# --- Main Execution ---
if __name__ == "__main__":
    try:
        url_to_analyze = input("Enter the URL here: ")
        topics = run_topic_analysis(url_to_analyze, n_topics=6)
    except Exception as e:
        print(f"Fatal error: {e}")