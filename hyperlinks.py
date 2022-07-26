#!/usr/bin/env python3

import argparse
from bs4 import BeautifulSoup as bs
from collections import deque
import json
import requests
import sys

# TODO:
#   ensure everything is formatted with "black"
#   remove to-to comments

# TODO: plan
#   document how to use the tests and why they should go in ci (merge to master and branch commit)
#   Next:
#       clean everything up
#       ensure everything is commented
#       shoot for bonus points

# function to save the computed json to a file or stdout
def output_json(results, output=None):
    if output is not None:
        # this means --out= file was provided, so we'll write to that
        with open(output, "w") as output_file:
            json.dump(results, output_file, indent=4)
    else:
        # no --out file, so we write to stdout
        # using json.dump over print() to get pretty printing
        json.dump(results, sys.stdout, indent=4)


# cleans links to remove parameters and fragments
def clean_link(link, url):
    url_parts = url.split("//")
    base_url = url_parts[0] + "//" + url_parts[1].split("/")[0]

    # append http if not part of link
    if link[0:2] == "//":
        cleaned_output = "http:" + link
    elif link[0:1] == "/" or "//" not in link:
        cleaned_output = base_url + link
    else:
        cleaned_output = link

    # remove attributes from a url
    if "?" in cleaned_output:
        cleaned_output = cleaned_output.split("?")[0]

    # add a trailing slash if none is provided
    if cleaned_output[-1] != "/":
        cleaned_output = cleaned_output + "/"

    return cleaned_output


# extract hyperlinks from location provided by a url
def collect_hyperlinks_from_url(url):
    # bs4 was selected over re as it seemed to produced more reliable results than re when searching JS heavy sites
    #   example: Facebook and TikTok
    # the regular expression call is:
    #   single_link = re.findall(r'[<a href="].*?["]', url)
    #   the link will be contained in single_link[1]

    # get the source page from url
    link_html = requests.get(url).text

    # create a beautifulsoup object
    link_soup = bs(link_html, "html.parser")
    # find all the links in the pulled source
    hyperlinks = link_soup.find_all("a")
    hyperlink_list = []
    for link in hyperlinks:
        if link.get("href") is not None:
            link = link.get("href")
            # skip anchor tags
            if len(link) != 0 and link[0] == "#":
                continue
            # clean up the link for later usage
            cleaned_link = clean_link(link, url)
            hyperlink_list.append(cleaned_link)

    return hyperlink_list


# logic for the main page scraping function
def scrape_links(startUrl, limit, out=None):
    count = 0
    # setting up a double ended queue, faster operation than removing the head of a list
    hyperlinks = deque()
    hyperlinks.append(startUrl)

    visited_links = []
    results = {}

    while count < limit:
        link = hyperlinks[0]
        # prevent cyclical looping when pages link to themselves
        if link not in visited_links:
            visited_links.append(link)
            # print statement is to help a user view that the program is running
            # not called for in the project description but found to be helpful
            print(f"parsing: {link}")
            page_links = list(collect_hyperlinks_from_url(link))
            if link not in results:
                results[link] = {"outgoing": page_links}
            elif "outgoing" not in results[link]:
                results[link]["outgoing"] = page_links

            # add new links to the queue
            hyperlinks.extend(page_links)

            # create dictionary entries with incoming data for scraped links
            for outgoing_link in page_links:
                if outgoing_link not in results:
                    results[outgoing_link] = {"incoming": [link]}
                elif "incoming" not in results[outgoing_link]:
                    results[outgoing_link]["incoming"] = [link]
                else:
                    results[outgoing_link]["incoming"].append(link)

            # track the total number of links parsed
            count = count + 1
            # print statement is to help a user keep track of number of checked pages
            # not called for in the project description but found to be helpful
            if count == 1:
                print(f"parsed {count} page")
            else:
                print(f"parsed {count} pages")

        # remove the parsed url
        hyperlinks.popleft()

        # if the queue is empty we are done
        if len(hyperlinks) == 0:
            break

    # write output to json file or standard out if none is provided
    output_json(results, out)
    return results


if __name__ == "__main__":
    # set up the parser
    argument_parser = argparse.ArgumentParser(
        description="traverse the Web as a linked graph from the starting --url "
        "finding all outgoing links (<a> tag): it will store each outgoing link "
        "for the URL, and then repeat the process for each of them, until "
        "--limit URLs will have been traversed.",
        epilog="Example: hyperlinks.py --url https://docs.python.org/ --limit 10 --out links.json",
    )
    argument_parser.add_argument("--url", help="Starting URL", required=True)
    argument_parser.add_argument(
        "--limit",
        help="Number of URLs to traverse",
        type=int,
        default=1000,
        action="store",
        required=True,
    )
    argument_parser.add_argument(
        "--out",
        help="File to store computed json data in, defaults to stdout",
        type=str,
        action="store",
    )
    arguments = argument_parser.parse_args()

    # catch urls without https://
    url = arguments.url
    if not arguments.url.startswith("https://") and not arguments.url.startswith(
        "http://"
    ):
        # logging for when a http schema can not be inferred
        print("no schema detected, attempting to use http://")
        url = "http://" + arguments.url

    if not url.endswith("/"):
        url = url + "/"

    # print statement is for displaying the users given parameters
    # not called for in the project description but found to be helpful
    print(f"starting url: {url}")
    print(f"limit: {arguments.limit}\n")

    # entrypoint for main logic
    scrape_links(url, arguments.limit, arguments.out)
