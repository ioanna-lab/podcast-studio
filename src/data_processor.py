import requests
from bs4 import BeautifulSoup

def fetch_article(url: str) -> dict:
    """
    Fetch and extract text content from a URL.
    Returns a dictionary with title and content.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract title
        title = soup.find("title")
        title_text = title.get_text(strip=True) if title else "No title found"

        # Remove unwanted tags
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        # Extract main text
        paragraphs = soup.find_all("p")
        content = " ".join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 50])

        if not content:
            return {"error": "Could not extract content from this URL."}

        return {
            "title": title_text,
            "content": content[:5000],  # limit to 5000 chars to stay within token limits
            "url": url
        }

    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Please try a different URL."}
    except requests.exceptions.ConnectionError:
        return {"error": "Could not connect to the URL. Please check the address."}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


# Quick test — run this file directly to verify it works
if __name__ == "__main__":
    test_url = "https://www.bbc.com/news"
    result = fetch_article(test_url)
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Title: {result['title']}")
        print(f"Content preview: {result['content'][:300]}...")