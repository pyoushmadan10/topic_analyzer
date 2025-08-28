import requests
from bs4 import BeautifulSoup
import time
import re


class ContentFetcher:
    def __init__(self, url):
        self.url = url
        self.text = ""
        self.title_text = ""
        self.heading_text = ""
        self.body_text = ""

    def has_domain_extension(self, text):
        """Check if text contains domain extensions."""
        return bool(re.search(r'\.(com|org|net|co|uk|in|de|fr)(\s|$)', text.lower()))

    def fetch_and_extract_text(self, retries=3):
        """Fetch and extract text with priority hierarchy."""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }
        
        for attempt in range(retries):
            try:
                response = requests.get(self.url, headers=headers, timeout=60)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'lxml')

                # Extract title (HIGHEST PRIORITY)
                try:
                    title_elements = soup.select('title')
                    self.title_text = ' '.join([elem.get_text(strip=True) for elem in title_elements])
                except Exception as e:
                    print(f"Error extracting title: {e}")
                    self.title_text = ""

                # Extract headings (HIGH PRIORITY)
                try:
                    heading_elements = soup.select('h1, h2, h3,span')
                    self.heading_text = ' '.join([elem.get_text(strip=True) for elem in heading_elements])
                except Exception as e:
                    print(f"Error extracting headings: {e}")
                    self.heading_text = ""

                # Remove unwanted elements
                try:
                    for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
                        script.decompose()
                except Exception as e:
                    print(f"Error removing unwanted elements: {e}")

                # Extract main content
                main_selectors = ['main', 'article','section',]
                
                body_text = ""
                try:
                    for selector in main_selectors:
                        elements = soup.select(selector)
                        if elements:
                            body_text = elements[0].get_text(separator=" ", strip=True)
                            break
                except Exception as e:
                    print(f"Error extracting main content: {e}")

                if not body_text:
                    try:
                        body_text = soup.get_text(separator=" ", strip=True)
                    except Exception as e:
                        print(f"Error extracting fallback body text: {e}")
                        body_text = ""

                try:
                    self.body_text = body_text.replace(self.title_text, '').replace(self.heading_text, '')
                except Exception as e:
                    print(f"Error cleaning body text: {e}")
                    self.body_text = body_text

                try:
                    self.text = f"{self.title_text} {self.heading_text} {self.body_text}"
                    self.text = ' '.join(self.text.split())
                except Exception as e:
                    print(f"Error finalizing text: {e}")
                    self.text = f"{self.title_text} {self.heading_text} {self.body_text}"

                print(f"Extracted {len(self.text)} characters from {self.url}")
                return len(self.text) > 100
                
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < retries - 1:
                    time.sleep(2)
        return False