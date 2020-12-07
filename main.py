"""
This is my first independent Python project not from one of the books I have read as part of my self-study efforts.
This project aims to develop a program that can assist someone trying to engage in SEO (Search Engine Optimization).
Planned features include analysis of URL for length and presence of keywords, presence of keywords and stop words on
the page and an analysis/comparison of keywords across different sites. APIs may be used.
"""
import requests
from bs4 import BeautifulSoup

# Get a site URL and create empty list for keywords which will be analysed to be entered.
# These will be analysed together and separately
url = input("Please enter a URL for the page which you would like to be analysed: ")
keywords = []

# Ask user for keywords to be put into above list.
print("Please enter keywords to be analysed. Input nothing to end input: ")
while True:
    inp = input()
    if inp == "":
        break
    keywords.append(inp)

print(keywords)
