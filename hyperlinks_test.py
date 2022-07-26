#!/usr/bin/env python3

import unittest
from unittest.mock import MagicMock

from testdata import *
from hyperlinks import *

# TODO: need to define how tests are going to be run

# mocking a requests.get() call with a 'text' attribute
class dummy_response:
    def __init__(self, text):
        self.text = text


# test cases for parsing pulled web pages, we're mocking the networks call even though example.com is stable
class test_collect_hyperlinks_from_url(unittest.TestCase):
    @unittest.mock.patch("hyperlinks.requests.get")
    def test_example_dot_com(self, fake_get):
        # create the mock response object
        response = dummy_response(example_dot_com)
        fake_get.return_value = response

        answer = collect_hyperlinks_from_url("http://www.example.com")
        self.assertEqual(answer, ["https://www.iana.org/domains/example/"])

    @unittest.mock.patch("hyperlinks.requests.get")
    def test_iana_reserved(self, fake_get):
        # create the mock response object
        response = dummy_response(iana_reserved_domains)
        fake_get.return_value = response

        answer = collect_hyperlinks_from_url("https://www.iana.org/domains/reserved/")
        self.assertEqual(answer, iana_link_list)


# checking that cleanLinks can handle fragments and attributes
class test_clean_link(unittest.TestCase):
    def test_unchanged_link(self):
        link = "http://www.wikipedia.com/"
        answer = clean_link(link, link)
        self.assertEqual(answer, link)

    def test_missing_http_and_slash(self):
        link = "//www.wikipedia.com"
        answer = clean_link(link, link)
        self.assertEqual(answer, "http://www.wikipedia.com/")

    def test_remove_link_attribute(self):
        link = "http://www.wikipedia.com/?=super-cool-page"
        answer = clean_link(link, link)
        self.assertEqual(answer, "http://www.wikipedia.com/")

    def test_base_url_add(self):
        link = "/super-cool-page"
        url = "http://www.wikipedia.com/"
        answer = clean_link(link, url)
        self.assertEqual(answer, "http://www.wikipedia.com/super-cool-page/")


# kick off the unit tests
if __name__ == "__main__":
    unittest.main()
