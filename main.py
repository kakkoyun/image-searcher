# -*- coding: utf-8 -*-

"""Simple command-line tool for Google Image Custom Search.
Command-line application that does a search and download.
"""

__author__ = 'kakkoyun@gmail.com (Kemal Akkoyun)'

import os
import pprint

from googleapiclient.discovery import build


def main():
    API_KEY = os.environ["GOOGLE_API_KEY"]
    ENGINE_ID = os.environ["GOOGLE_SEARCH_ENGINE_ID"]

    service = build('customsearch', 'v1', developerKey=API_KEY)

    res = service.cse().list(
        q='paradoy',
        cx=ENGINE_ID,
    ).execute()

    pprint.pprint(res)


if __name__ == '__main__':
    main()
