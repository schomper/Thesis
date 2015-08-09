#! /usr/bin/python3

import re
import sys
import urllib

from bs4 import BeautifulSoup
from nltk.corpus import stopwords

#   get_area_links:
#       Function gets the hyperlinks present in a certain area
#
#   input:
#       relevantArea: area of markup in which to search for links
#
#   return:
#       array of links within relevantArea markup
def get_area_links(relevantArea):
    links = []

    for link in relevantArea.findAll("a", href=True):
        link = link["href"]

        # avoid local links
        if "#" in link:
            continue

        links.append(link)

    return links


def process_next_level(relevant_links, depth):
    global count
    global MAX_REPS

    for link in relevant_links:
        print("%d: processing %d:%d links" % (depth, relevant_links.index(link),
                                              len(relevant_links)))
        # relative urls
        if link.startswith("/"):

            host = url.replace('https://', '', 1)
            if "/" in host:
                host, rest = re.split("/", host, 1)

            link = "https://" + host + link

        if count % 20 == 0:
            print("Processing link: %d" % count)

        if count == MAX_REPS:
            return

        if depth:
            process_pages(link, depth - 1)


def print_document_to_file(page_title, page_body, doc_file):
    global count

    count += 1

    doc_file.write("<DOC>\n")
    doc_file.write("<DOCNAME>%s</DOCNAME>\n" % page_title)
    doc_file.write("<TEXT>\n")
    cached_stop_words = stopwords.words("english")
    text = page_body.getText()
    text = ' '.join([word for word in text.split() if word not in cached_stop_words])
    doc_file.write("%s\n" % text)
    doc_file.write("</TEXT>\n")
    doc_file.write("</DOC>\n")


def process_pages(url, depth):
    global HEADING
    global BODY
    global HOST
    global doc_file
    global processedPages

    if url.startswith(HOST) and (url not in processedPages):

        # add page to processed pages
        processedPages.append(url)

        try:
            # print("Trying: %s" % url)
            response = urllib.request.urlopen(url)

        except(Exception, urllib.error.HTTPError):
            # print("Skipping %s: 404" % (url))
            return

        response_contents = response.read()
        page_soup = BeautifulSoup(response_contents)

        try:
            page_title = page_soup.find("h1", {"id": HEADING}).getText()
            page_body = page_soup.find("div", {"id": BODY})
        except(Exception, AttributeError):
            return

        print_document_to_file(page_title, page_body, doc_file)

        # process the next depth level of links
        relevant_links = get_area_links(page_body)
        process_next_level(relevant_links, depth)


if __name__ == "__main__":

    if len(sys.argv) != 7:
        print("Usage: ./web_crawler.py <url> <depth> <heading> <body> <max_iter> <output>")
        exit(1)
        
    # set crawl properties
    count = 0
    processedPages = []

    url = sys.argv[1] 
    depth = int(sys.argv[2])
    HEADING = sys.argv[3] 
    BODY = sys.argv[4] 
    MAX_REPS = int(sys.argv[5])
    OUTPUT_FILE = sys.argv[6]

    doc_file = open(OUTPUT_FILE, "w")

    # set up host
    HOST = url.replace('https://', '', 1)
    HOST = "https://" + HOST.split("/", 1)[0]

    # process pages
    process_pages(url, int(depth))
