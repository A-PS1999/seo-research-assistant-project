"""
This is my first independent Python project not from one of the books I have read as part of my self-study efforts.
This project aims to develop a program that can assist someone trying to engage in SEO (Search Engine Optimization).
Features include an analysis of URL length, analysis of whether or not keywords are present in a URL or the page it
relates to and analysis of backlinks data collected by an API to provide the user with information about their
domain/page authority and the number of external pages linking to the provided URL.
"""
from tkinter import *
from tkinter import scrolledtext as st
import requests
import re
import json
import os
import sys
import errno
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from datetime import datetime
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

# create directory for files which are created as part of running the program
try:
    if not os.path.exists('output_files'):
        os.makedirs('output_files')
except OSError as e:
    if e.errno != errno.EEXIST:
        raise e

# `resource_path` used to access stopwords.txt from within compiled program


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def get_url():
    global urlSoup
    # 'agent' added as part of effort to avoid HTTP Error 403: Forbidden
    url_request = requests.get(url_entry.get(), headers={'User-Agent': agent})

    try:
        url_request.raise_for_status()
    except requests.exceptions.MissingSchema as exc:
        log_text.insert(INSERT, "\nERROR: Invalid URL provided. Please try again with a valid URL.")
        raise exc

    urlSoup = BeautifulSoup(url_request.text, 'lxml')

# below function gets keywords from GUI, puts them into a list


def append_keyword_entry():
    entry_for_list = keywords_entry.get().split(", ")
    for entry in entry_for_list:
        keywords_list.append(entry)


# below function scans provided URL and returns all found keywords and the number of times they appear
def seo_find_keywords(keywords_list, urlSoup):
    try:
        for keyword in keywords_list:
            keyword_count = len(re.findall(keyword, str(urlSoup), re.IGNORECASE))
            if keyword_count > 0:
                log_text.insert(INSERT, "\nThe keyword " + keyword + " was found " + str(keyword_count) +
                                " times in " + url_entry.get() + ".")
            else:
                log_text.insert(INSERT, "\nThe keyword '" + keyword + "' was not found on the page.")
    except UnicodeDecodeError as exc:
        log_text.insert(INSERT, "\nError: {0}".format(exc))
        raise exc


# searches HTML page title for SEO stop words from stopwords.txt, then provides number and list of present stop words
def seo_find_stopwords(urlSoup):
    stopwords_count = 0
    stopwords_list = []
    if urlSoup.title:
        with open(resource_path('stopwords.txt'), 'r', encoding='utf-8') as file:
            for line in file:
                if re.search(r'\b' + line.rstrip('\n') + r'\b', urlSoup.title.text.casefold()):
                    stopwords_count += 1
                    stopwords_list.append(line.rstrip('\n'))

        if stopwords_count > 0:
            log_text.insert(INSERT, "\n{0} stop words were found in your page title. If possible, it would be good to "
                            "reduce them. The stop words found are: {1}".format(stopwords_count, stopwords_list))
        else:
            log_text.insert(INSERT, "\nYour page title has no stop words. That's good!")
    else:
        log_text.insert(INSERT, "\nA title was not found for your page.")


# below lists and seo_find_404 function used for purpose of finding all broken links in provided url
search_links = []
broken_links = []


def seo_find_404(urlSoup):
    s = requests.Session()
    s.headers['User-Agent'] = 'SEO Research Assistant Program'
    retry_strategy = Retry(connect=3, backoff_factor=1)
    adapter = HTTPAdapter(max_retries=retry_strategy)
    s.mount('http://', adapter)
    s.mount('https://', adapter)

    for link in urlSoup.find_all('a', href=True):
        search_links.append(link.get('href'))

    broken_links_count = 0
    for search_link in search_links:
        try:
            if search_link.startswith('http') and not search_link.startswith('mailto:') \
                    and 'javascript:' not in search_link and 'tel:' not in search_link:
                broken_query = s.get(search_link, allow_redirects=3)

                if broken_query.status_code == 404:
                    broken_links.append(search_link)
                    broken_links_count += 1

        except requests.exceptions.ConnectionError as exc:
            log_text.insert(INSERT, '\nError: {0}'.format(exc))

    log_text.insert(INSERT, "\n{0} broken links were found.".format(broken_links_count))
    for broken_link in broken_links:
        log_text.insert(INSERT, "\nBroken link found: {0}".format(broken_link))


# checks to see if URL is less than 60 characters long for optimum SEO
def seo_url_length(url):
    if len(url) < 60:
        log_text.insert(INSERT, "\nYour URL is in the optimum length range, that's good!")
    elif len(url) > 60:
        log_text.insert(INSERT, "\nYour URL is too long for optimum SEO. If possible, try shortening it.")


# checks for presence of keywords in URL, as keyword presence can be SEO boost
def seo_url_keywords(keywords_list, url):
    for keyword in keywords_list:
        if keyword.casefold() in url:
            log_text.insert(INSERT, "\nThe keyword \"{0}\" was found in your URL. That's good!".format(keyword))
        else:
            log_text.insert(INSERT, "\nThe keyword \"{0}\" was not found in your URL. Your URL may be improved by "
                                    "adding keywords if you lack enough of them.".format(keyword))

    keywords_list.clear()


# gets info about backlinks and domain authority from MOZ API, then writes response to
# a json file
def seo_get_backlinks(url):
    endpoint = 'https://lsapi.seomoz.com/v2/url_metrics'
    headers = {"User-Agent": agent}
    url = url_entry.get()
    apirequest = {
        "targets": [url],
        "daily_history_values": ["external_pages_to_root_domain", "external_pages_to_page"],
        "monthly_history_values": ["domain_authority"]
    }

    apiresponse = requests.post(endpoint, json=apirequest, headers=headers,
                                auth=(os.environ.get('MOZ_ID'), os.environ.get('MOZ_SECRET')))
    if apiresponse.status_code != 200:
        print(apiresponse.status_code)
        raise SystemExit

    with open(r'output_files\backlinks_api_response.json', 'w', encoding='utf-8') as responsefile:
        to_json = apiresponse.json()
        json.dump(to_json, responsefile, ensure_ascii=False)


# creation of various GUI elements; window, info labels, text entry boxes and button
root = Tk()
root.title("SEO Research Assistant Program")

keywords_label = Label(root, text="Please enter keywords which you would like to analyse."
                                  " Please enter them like this: 'word, example, test'.")
keywords_entry = Entry(root, width=80)
keywords_list = []
log_text = st.ScrolledText(root, width=80)

url_label = Label(root, text="Please enter a URL for the page you would like to analyse:")
url_entry = Entry(root, width=80)
url_entry.bind('<Return>', get_url)
url = url_entry.get()


start_button = Button(root, text='Run program', command=lambda: [get_url(), append_keyword_entry(),
                                                                 seo_find_keywords(keywords_list, urlSoup),
                                                                 seo_find_stopwords(urlSoup),
                                                                 seo_find_404(urlSoup), seo_url_length(url),
                                                                 seo_url_keywords(keywords_list, url),
                                                                 seo_get_backlinks(url),
                                                                 seo_backlinks_report()])

url_label.grid(column=0, row=0)
url_entry.grid(column=0, row=1)
keywords_label.grid(column=0, row=3)
keywords_entry.grid(column=0, row=4)
log_text.grid(column=2, row=0, rowspan=3)
start_button.grid(column=1, row=5)


# provides data from API response to user in form of print statements and chart made with matplotlib
def seo_backlinks_report():
    # below .replace() usage to avoid OSError when performing plt.savefig()
    to_save = url_entry.get()
    save_url = to_save.replace("http://", "").replace("https://", "").replace("/", "")
    with open(r'output_files\backlinks_api_response.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        page_crawled_dates = [datetime.strptime(key['date'], '%Y-%m-%d').date() for key in data['results']
                              [0]['daily_history_values']['external_pages_to_root_domain']]

        pages_to_root_counts = [int(key['count']) for key in data['results'][0]['daily_history_values']
                                ['external_pages_to_root_domain']]

        ext_pages_page_counts = [int(key['count']) for key in data['results'][0]['daily_history_values']
                                 ['external_pages_to_page']]

        log_text.insert(INSERT, "\nThe current domain authority of {0} is "
                                "{1}.".format(url_entry.get(), data['results'][0]['domain_authority']))
        log_text.insert(INSERT, "\nThe current page authority of {0} is "
                                "{1}.".format(url_entry.get(), data['results'][0]['page_authority']))

    log_text.insert(INSERT, "\nCreating graphs for the 'external pages to page' and 'external pages to root domain' "
                            "metrics for {0}.".format(url_entry.get()))

    # below code creates and saves graph for external_pages_to_root_domain data
    rootfig = plt.figure(dpi=200)
    plt.plot(page_crawled_dates, pages_to_root_counts, c='blue')

    plt.title("Number of external pages to root domain, {0} - {1}".format(page_crawled_dates[0],
                                                                          page_crawled_dates[-1]))
    plt.xlabel("", fontsize=16)
    rootfig.autofmt_xdate()
    plt.ylabel("External pages to root domain", fontsize=13)

    try:
        plt.savefig(r"output_files\{0}_external_pages_to_root_domain_{1}_to_{2}.png".format(save_url,
                                                                                            page_crawled_dates[0],
                                                                                            page_crawled_dates[-1]))
        log_text.insert(INSERT, "\nSuccessfully saved an image of "
                                "'{0}_external_pages_to_root_domain_{1}_to_{2}' to your computer.".format(save_url,
                                                                                                page_crawled_dates[0],
                                                                                                page_crawled_dates[-1]))
    except Exception as exc:
        log_text.insert(INSERT, "Error: {0}".format(exc))

    # below code creates and saves graph for external_pages_to_page data
    page_to_pagefig = plt.figure(dpi=200)
    plt.plot(page_crawled_dates, ext_pages_page_counts, c='blue')

    plt.title("Number of external pages to URL, {0} - {1}".format(page_crawled_dates[0],
                                                                  page_crawled_dates[-1]))
    plt.xlabel("", fontsize=13)
    page_to_pagefig.autofmt_xdate()
    plt.ylabel("External pages to URL", fontsize=13)

    plt.tight_layout()
    ax = page_to_pagefig.gca()
    ax.get_yaxis().set_major_formatter(plt.FormatStrFormatter('%.0f'))
    ax.tick_params(axis='x', labelsize=8)

    try:
        plt.savefig(r"output_files\{0}_external_pages_to_page_{1}_to_{2}.png".format(save_url, page_crawled_dates[0],
                                                                                               page_crawled_dates[-1]))
        log_text.insert(INSERT, "\nSuccessfully saved an image of "
                                "'{0}_external_pages_to_page_{1}_to_{2}' to your computer.".format(save_url,
                                                                                            page_crawled_dates[0],
                                                                                            page_crawled_dates[-1]))
    except Exception as exc:
        log_text.insert(INSERT, "Error: {0}".format(exc))


agent = "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0"

root.mainloop()
