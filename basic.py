# Import necessary libraries for web scraping
import requests  # For making HTTP requests
from bs4 import BeautifulSoup  # For parsing HTML content

# Send GET request to Hacker News homepage
response = requests.get('https://news.ycombinator.com/news')

# # Print response object (shows status code and other metadata)
# print(response)

# # Print the HTML content of the page
# print(response.text)

# Parse the HTML content using BeautifulSoup with html.parser
soup = BeautifulSoup(response.text, 'html.parser')

# # Print the entire parsed HTML structure
# print(soup)

# # Print only the body tag of the HTML
# print(soup.body)

# # Print all direct children elements within the body tag
# print(soup.body.contents)

# # Find all div elements
# print(soup.find_all('div'))
# print()

# # Find all anchor tags
# print(soup.find_all('a'))

# # Print the title tag of the page
# print(soup.title)

# # Print the first anchor tag found in the document
# print(soup.a)

# # Equivalent to soup.a - finds the first anchor tag
# print(soup.find('a'))

# # Find an element with the specific ID 'score_46374413'
# print(soup.find(id="score_46374413"))


# CSS selector - Find all div elements
# print(soup.select('div'))

# # CSS selector - Find all elements with class 'score' (. means class)
# print(soup.select('.score'))

# # CSS selector - Find element with ID 'score_46374413' (# means ID)
# print(soup.select('#score_46374413'))

links= soup.select('.titleline')
votes = soup.select('.score')
print(votes[0])
print(votes[0].get('id'))
print("Thats so cool!!")