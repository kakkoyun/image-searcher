# -*- coding: utf-8 -*-

"""Simple command-line tool for Google Image Custom Search.
Command-line application that does a search and download.
"""

__author__ = 'kakkoyun@gmail.com (Kemal Akkoyun)'

import os
import sys
import json
import argparse

from google_image_search_service import GoogleImageSearchService


def main():
    parser = argparse.ArgumentParser(
        description='Image Searcher: Provide parameters to search for images for given term.')
    parser.add_argument('term', nargs='+',
                        help='a search term to be searched')
    parser.add_argument('--count', type=int,
                        help='a parameter to specify how many images to download.')
    parser.add_argument('--api_key',
                        help='an API keys from Google Developer Console, (https://console.developers.google.com/apis/api/customsearch.googleapis.com/overview)')
    parser.add_argument('--engine_id',
                        help='an engine id from Google Custom Search Engine Console (https://cse.google.com/cse/all)')

    args = parser.parse_args()
    term = ' '.join(args.term)
    count = args.count

    try:
        api_key = args.api_key if args.api_key else os.environ['GOOGLE_API_KEY']
        engine_id = args.engine_id if args.engine_id else os.environ['GOOGLE_SEARCH_ENGINE_ID']
    except KeyError, e:
        print 'You need to provide %s, either by using optional arguments or environment variables.' % e
        sys.exit()

    service = GoogleImageSearchService(api_key, engine_id)
    result = service.image_search(term, count)

    print json.dumps(result, indent=4, sort_keys=True)

if __name__ == '__main__':
    main()
