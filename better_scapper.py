import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
from urllib.parse import urljoin

# 1) Download HTML for page 1 and page 2
res1 = requests.get('https://news.ycombinator.com/news')
res2 = requests.get('https://news.ycombinator.com/news?p=2')

# 2) Parse HTML strings into BeautifulSoup “trees”
soup1 = BeautifulSoup(res1.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')

def parse_page(soup, min_points=100):
    """Parse a Hacker News page soup and return stories with >= min_points.

    This version avoids the common 'index mismatch' bug by pairing each story row
    with its *next sibling row* (where the score lives).
    """
    results = []
    
    # Each story title lives in a <tr class="athing ..."> row.
    # That story row is followed by another <tr> which contains meta info (score, author, etc.).
    for story_row in soup.select('tr.athing'):
        # Find the story title link inside this row.
        a = story_row.select_one('.titleline > a')
        if not a:
            continue
        
        # Extract the visible title text.
        title = a.get_text(strip=True)

        # Extract the href attribute (can be a full URL or a relative HN link like "item?id=...").
        href = a.get('href')

        # Convert relative links into full URLs.
        url = urljoin('https://news.ycombinator.com/', href) if href else None
        
        # The next <tr> right after the story row contains metadata, including the score.
        meta_row = story_row.find_next_sibling('tr')

        # Pull the score element (e.g., <span class="score">123 points</span>) if it exists.
        score = meta_row.select_one('.score') if meta_row else None
        if not score:
            continue

        # score.get_text() looks like "123 points" or "1 point".
        # Use regex to extract the digits so both cases work.
        m = re.search(r'\d+', score.get_text())
        points = int(m.group()) if m else 0
        
        # Filter: keep only stories with enough points.
        if points >= min_points:
            results.append({'text': title, 'URL': url, 'points': points})
            
    return results

# 3) Parse each page separately
custom_news1 = parse_page(soup1)
custom_new2 = parse_page(soup2)

# 4) Combine results from both pages
mega_news_hn = custom_news1 + custom_new2

# 5) Sort final list by points (highest first)
new_mega_news_hn = sorted(mega_news_hn, key= lambda k: k['points'], reverse=True)

# 6) Print results nicely
pprint(new_mega_news_hn)


# # =========================
# # VISUALIZATION (Learning)
# # =========================
# # This section prints a beginner-friendly “what happened” summary.

# print("\n" + "=" * 60)
# print("VISUALIZATION: How the scraper pairs title row -> votes row")
# print("=" * 60)

# print("\nStep 1: Download HTML")
# print(f"- Page 1 status: {res1.status_code}")
# print(f"- Page 2 status: {res2.status_code}")

# print("\nStep 2: Parse HTML into a tree (BeautifulSoup)")
# print("- Now we can search using CSS selectors like 'tr.athing' and '.score'.")

# story_rows_1 = soup1.select('tr.athing')
# story_rows_2 = soup2.select('tr.athing')
# print("\nStep 3: Find story rows")
# print(f"- Page 1 story rows (tr.athing): {len(story_rows_1)}")
# print(f"- Page 2 story rows (tr.athing): {len(story_rows_2)}")

# print("\nStep 4: For each story row")
# print("- Find the title link: row.select_one('.titleline > a')")
# print("- Find the votes row: row.find_next_sibling('tr')")
# print("- Find the score: meta_row.select_one('.score')")

# if story_rows_1:
#     example_row = story_rows_1[0]
#     example_a = example_row.select_one('.titleline > a')
#     example_meta = example_row.find_next_sibling('tr')
#     example_score = example_meta.select_one('.score') if example_meta else None

#     print("\nExample (first story on page 1)")
#     if example_a:
#         ex_title = example_a.get_text(strip=True)
#         ex_href = example_a.get('href')
#         ex_url = urljoin('https://news.ycombinator.com/', ex_href) if ex_href else None
#         print(f"- Title text: {ex_title}")
#         print(f"- Raw href: {ex_href}")
#         print(f"- Full URL (urljoin): {ex_url}")
#     else:
#         print("- Could not find title link in this row (unexpected).")

#     if example_score:
#         score_text = example_score.get_text(strip=True)
#         m = re.search(r'\d+', score_text)
#         ex_points = int(m.group()) if m else 0
#         print(f"- Score text: {score_text}")
#         print(f"- Digits extracted (m.group()): {m.group() if m else None}")
#         print(f"- Parsed points (int): {ex_points}")
#     else:
#         print("- This story has no .score (job/promoted/edge case), so we skip it.")

# print("\nStep 5: Filter + sort")
# print("- We keep only points >= 100")
# print("- Then sort by 'points' descending")
# print(f"- Final kept stories: {len(new_mega_news_hn)}")
        