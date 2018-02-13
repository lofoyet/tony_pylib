#! /usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from bs4 import BeautifulSoup


def extractAll(html):
    soup = BeautifulSoup(html, 'html.parser')
    result = []
    result.append(("title", extractTitle(soup)))
    result.append(("time", extractTime(soup)))
    result.append(("profile_name", extractProfileName(soup)))
    result.append(("content", extractContent(soup)))
    return tuple(result)


def extractTitle(soup):
    title = []
    title = soup.findAll("h2", {"class": "rich_media_title"})
    if title:
        return title[0].text
    else:
        return ""


def extractTime(soup):
    time = []
    time = soup.findAll("em", {"id": "post-date"})
    if time:
        return time[0].text
    else:
        return ""


def extractProfileName(soup):
    name = []
    name = soup.findAll("strong", {"class": "profile_nickname"})
    if name:
        return name[0].text
    else:
        return ""


def extractContent(soup):
    content = []
    content = soup.findAll("div", {"class": "rich_media_content "})
    if content:
        return "\n".join([content[i].text for i in range(len(content))])
    else:
        return ""


def test_extract_all():
    test_html = ""
    assert extractAll(test_html) == (
        ("title", ""), ("time", ""), ("profile_name", ""), ("0", ""), )
