import nltk
import spacy
import warnings
warnings.filterwarnings('ignore')


def download_nltk_dependencies():
    """Download required NLTK dependencies."""
    try:
        nltk.download("punkt", quiet=True)
    except Exception as e:
        print(f"Error downloading 'punkt': {e}")
    try:
        nltk.download("stopwords", quiet=True)
    except Exception as e:
        print(f"Error downloading 'stopwords': {e}")
    try:
        nltk.download("wordnet", quiet=True)
    except Exception as e:
        print(f"Error downloading 'wordnet': {e}")
    try:
        nltk.download("averaged_perceptron_tagger", quiet=True)
    except Exception as e:
        print(f"Error downloading 'averaged_perceptron_tagger': {e}")


def load_spacy_model():
    """Load spaCy model, download if necessary."""
    try:
        nlp = spacy.load('en_core_web_sm')
    except OSError:
        try:
            print("Downloading spaCy model 'en_core_web_sm'...")
            from spacy.cli import download
            download('en_core_web_sm')
            nlp = spacy.load('en_core_web_sm')
        except Exception as e:
            print(f"Error downloading/loading spaCy model: {e}")
            nlp = None
    except Exception as e:
        print(f"Error loading spaCy model: {e}")
        nlp = None
    return nlp