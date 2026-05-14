import requests

HN_TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

def get_top_stories(limit: int = 5) -> list:
    """
    Fetch the top N story IDs from Hacker News.
    """
    try:
        response = requests.get(HN_TOP_STORIES_URL, timeout=10)
        response.raise_for_status()
        story_ids = response.json()
        return story_ids[:limit]
    except Exception as e:
        return []


def get_story_details(story_id: int) -> dict:
    """
    Fetch details for a single story by ID.
    Returns title, url, score, and author.
    """
    try:
        response = requests.get(HN_ITEM_URL.format(story_id), timeout=10)
        response.raise_for_status()
        story = response.json()

        return {
            "title": story.get("title", "No title"),
            "url": story.get("url", ""),
            "score": story.get("score", 0),
            "author": story.get("by", "unknown"),
            "story_id": story_id
        }
    except Exception as e:
        return {"error": f"Could not fetch story {story_id}: {str(e)}"}


def fetch_hn_briefing(limit: int = 5) -> dict:
    """
    Fetch top N HN stories and combine them into a single article dict
    ready to pass to llm_processor.
    """
    try:
        print(f"Fetching top {limit} stories from Hacker News...")
        story_ids = get_top_stories(limit=limit)

        if not story_ids:
            return {"error": "Could not fetch Hacker News stories."}

        stories = []
        for story_id in story_ids:
            details = get_story_details(story_id)
            if "error" not in details:
                stories.append(details)
                print(f"  ✅ {details['title'][:60]}...")

        if not stories:
            return {"error": "No stories could be fetched."}

        # Build a combined content string for the LLM
        content = "Top stories from Hacker News today:\n\n"
        for i, story in enumerate(stories, start=1):
            content += f"{i}. {story['title']} (score: {story['score']}, by {story['author']})\n"
            if story["url"]:
                content += f"   URL: {story['url']}\n"
            content += "\n"

        return {
            "title": "Hacker News Top Stories",
            "content": content,
            "url": "https://news.ycombinator.com",
            "stories": stories
        }

    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


# Quick test
if __name__ == "__main__":
    result = fetch_hn_briefing(limit=5)

    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"\nTitle: {result['title']}")
        print(f"\nContent:\n{result['content']}")