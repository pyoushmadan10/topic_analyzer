# Topic Analyzer

A Python-based tool for extracting and ranking most relevant topics from web pages using NLP and AI techniques.

---

## Features

- **Web Content Extraction:** Uses BeautifulSoup to fetch and parse web pages.
- **Stopword Management:** Filters out common and domain-specific stopwords.
- **Topic Extraction:** Utilizes spaCy for named entity recognition and noun phrase extraction.
- **Priority Scoring:** Ranks topics based on their prominence in title, headings, and body.
- **Error Handling:** Robust error management throughout the pipeline.
- **Extensible:** Ready for integration with advanced topic modeling (LDA, NMF).

---

## Techniques Used

- **Natural Language Processing:** spaCy for linguistic analysis, NLTK for stopwords.
- **Web Scraping:** BeautifulSoup for HTML parsing.
- **Custom Filtering:** Domain-specific stopword and keyword filtering.

---

## Setup Instructions

### 1. Clone the Repository

```sh
git clone <your-repo-url>
cd topic_analyzer
```

### 2. Create and Activate a Virtual Environment

```sh
python -m venv venv
venv\Scripts\activate   # On Windows
# Or
source venv/bin/activate   # On macOS/Linux
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, use:

```sh
pip install requests beautifulsoup4 nltk spacy
```

### 4. Download NLTK and spaCy Data

The code will automatically download required NLTK data and the spaCy model (`en_core_web_sm`) on first run.

---

## Usage

### Run the Topic Analyzer

```sh
python main.py
```

- Enter the URL you want to analyze when prompted.
- The tool will display the top topics ranked by confidence.

---

## File Structure

- `main.py` - Entry point for topic extraction.
- `content_fetcher.py` - Fetches and parses web content.
- `stopword_manager.py` - Manages stopwords and URL keywords.
- `topic_extractor.py` - Extracts and scores topics using NLP.
- `utils.py` - Utility functions for downloading models and data.

---

## Example Output

```
Analyzing URL: https://example.com
================================================================================

--- Topics Ranked by Confidence (High to Low) ---
 1. Example Topic 1                               | Confidence: 95.0%
 2. Example Topic 2                               | Confidence: 88.0%
...

================================================================================
Analysis complete!
```

---

## Troubleshooting

- If you encounter missing NLTK data errors, run:
  ```python
  import nltk
  nltk.download('punkt')
  nltk.download('stopwords')
  nltk.download('wordnet')
  nltk.download('averaged_perceptron_tagger')
  ```
- For spaCy model issues, run:
  ```sh
  python -m spacy download en_core_web_sm
  ```

---
