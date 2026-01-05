import requests
from bs4 import BeautifulSoup
from pprint import pprint
from urllib.parse import urljoin


# 1) Download the HTML from Hacker News (page 1 and page 2)
#
# requests.get(...) returns a Response object.
# The actual HTML content is inside response.text
res1 = requests.get('https://news.ycombinator.com/news')
res2 = requests.get('https://news.ycombinator.com/news?p=2')

# 2) Parse the HTML text into a BeautifulSoup "tree" so we can search it
soup1 = BeautifulSoup(res1.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')

# 3) Collect two separate lists from each page:
#    - links: the <a> tags that contain story title + href
#    - subtext: the blocks that contain votes (and other metadata)
#
# NOTE: This approach assumes links[idx] matches subtext[idx].
# On some pages, that alignment can break (e.g., job posts), which is a common scraping pitfall.
links1 = soup1.select('.titleline > a')
links2 = soup2.select('.titleline > a')
subtext1 = soup1.select('.subtext')
subtext2 = soup2.select('.subtext')

# 4) Combine page 1 + page 2 lists into one big list
mega_link = links1 + links2
mega_subtext = subtext1 + subtext2


def sort_hn_list_by_votes(hnlist):
    # Sort list of dictionaries by the 'points' field, highest first
    return sorted(hnlist, key=lambda k: k['points'], reverse=True)


def create_custom_hn(link, subtext):
    # Build a list of story dictionaries like:
    # {'text': title, 'URL': full_link, 'points': 123}
    hn = []
    for idx, item in enumerate(link):
        # item is an <a> tag like: <a href="...">Some title</a>
        text = item.getText()

        # Read the href attribute (may be a full URL or a relative link like "item?id=...")
        href = item.get('href', None)

        # Convert relative HN links into a full URL
        # - "item?id=123" -> "https://news.ycombinator.com/item?id=123"
        # - "https://github.com/..." stays the same
        if href:
            href = urljoin('https://news.ycombinator.com/', href)

        # Find the score element inside the matching subtext block
        # .select(...) returns a list; it may be empty if there is no score
        score_tag = subtext[idx].select('.score')
        if len(score_tag):
            # score_tag[0].getText() looks like "123 points".
            # Remove the word " points" and convert to an int.
            # NOTE: This can fail for "1 point" (singular) without extra handling.
            points = int(score_tag[0].getText().replace(' points', ''))

            # Keep only popular stories (100+ points)
            if points >= 100:
                hn.append({'text': text, 'URL': href, 'points': points})
                

    # Return stories sorted by points (highest first)
    return sort_hn_list_by_votes(hn)


# 5) Build and print the final list
custom_news = create_custom_hn(mega_link, mega_subtext)
pprint(custom_news)
        