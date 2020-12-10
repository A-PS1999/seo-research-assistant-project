"""
This is my first independent Python project not from one of the books I have read as part of my self-study efforts.
This project aims to develop a program that can assist someone trying to engage in SEO (Search Engine Optimization).
Planned features include analysis of URL for length and presence of keywords, presence of keywords and stop words on
the page and an analysis/comparison of keywords across different sites. APIs may be used.
"""
import requests
import re
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

# attempts to access provided URL, returns errors if unable
try:
    agent = "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0"
    url_request = requests.get(url, headers={'User-Agent': agent})
    url_request.raise_for_status()
    urlSoup = BeautifulSoup(url_request.text, 'lxml')
except requests.exceptions.MissingSchema as exc:
    print("ERROR: Invalid URL provided. Please try again with a valid URL.")
    raise exc
except requests.exceptions.HTTPError as exc:
    print("ERROR: 404 error, URL not found.")
    raise exc


# below function scans provided URL and returns all found keywords and the number of times they appear
def seo_find_keywords(keywords, urlSoup):
    try:
        for keyword in keywords:
            keyword_count = len(re.findall(keyword, str(urlSoup), re.IGNORECASE))
            if keyword_count > 0:
                print("The keyword " + keyword + " was found " + str(keyword_count) + " times in " + url + ".")
            else:
                print("The keyword '" + keyword + "' was not found in the URL you provided.")
    except UnicodeDecodeError as exc:
        print("Error: %s" % exc)
        raise exc


# searches HTML page title for SEO stop words from stopwords.txt, then provides number and list of present stop words
def seo_find_stopwords(urlSoup):
    stopwords_count = 0
    stopwords_list = []
    if urlSoup.title:
        with open('stopwords.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if re.search(r'\b' + line.rstrip('\n') + r'\b', urlSoup.title.text.casefold()):
                    stopwords_count += 1
                    stopwords_list.append(line.rstrip('\n'))

        if stopwords_count > 0:
            print("{0} stop words were found in your page title. If possible, it would be good to "
                  "reduce them. The stop words found are: {1}".format(stopwords_count, stopwords_list))
        else:
            print("Your page title has no stop words. That's good!")
    else:
        print("A title was not found for your page.")


# checks to see if URL is less than 60 characters long for optimum SEO
def seo_url_length(url):
    if len(url) < 60:
        print("Your URL is in the optimum length range, that's good!")
    elif len(url) > 60:
        print("Your URL is too long for optimum SEO. If possible, try shortening it.")


# checks for presence of keywords in URL, as keyword presence can be SEO boost
def seo_url_keywords(keywords, url):
    for keyword in keywords:
        if keyword.casefold() in url:
            print("The keyword \"{0}\" was found in your URL. That's good!".format(keyword))
        else:
            print("The keyword \"{0}\" was not found in your URL. Your URL may be improved by adding "
                  "keywords if you lack enough of them.".format(keyword))


seo_find_keywords(keywords, urlSoup)
seo_find_stopwords(urlSoup)
seo_url_length(url)
seo_url_keywords(keywords, url)
