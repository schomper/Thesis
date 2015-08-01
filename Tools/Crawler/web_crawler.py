import re
import urllib
from bs4 import BeautifulSoup

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
        if("#" in link):
            continue

        links.append(link)

    return links

def process_next_level(relevant_links, depth):
    global count

    for link in relevant_links:
        print("%d: processing %d:%d links" % (depth, relevant_links.index(link),
                            len(relevant_links)))
        # relative urls
        if link.startswith("/"):

            host = url.replace('https://', '', 1)
            if("/" in host):
                host, rest = re.split("/", host, 1)

            link = "https://" + host + link

        if (count == 100):
            return

        if depth:
            processPages(link, depth - 1)

def print_document_to_file(page_title, page_body, doc_file):
    global count

    count = count + 1

    doc_file.write("<DOC>\n")
    doc_file.write("<DOCNAME>%s</DOCNAME>\n" % page_title)
    doc_file.write("<TEXT>\n")
    doc_file.write("%s\n" % page_body.getText())
    doc_file.write("</TEXT>\n")
    doc_file.write("</DOC>\n")

def processPages(url, depth):
    global HEADING
    global BODY
    global HOST
    global doc_file
    global processedPages

    if(url.startswith(HOST) and (not url in processedPages)):

        # add page to processed pages
        processedPages.append(url)

        try:
            #print("Trying: %s" % url)
            response = urllib.request.urlopen(url)

        except(Exception, urllib.error.HTTPError):
            #print("Skipping %s: 404" % (url))
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


if(__name__ == "__main__"):
    # set crawl properties
    config_file = open("crawl_config.txt", "r")
    doc_file = open("doc.txt", "w")
    count = 0
    processedPages = []

    url       = config_file.readline().strip().split(":", 1)[1]
    HEADING   = config_file.readline().strip().split(":", 1)[1]
    BODY      = config_file.readline().strip().split(":", 1)[1]
    depth     = config_file.readline().strip().split(":", 1)[1]

    # set up host
    HOST = url.replace('https://', '', 1)
    HOST = "https://" + HOST.split("/", 1)[0]

    # close file
    config_file.close()

    # process pages
    processPages(url, int(depth))
