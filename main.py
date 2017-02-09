# -*- coding: utf-8 -*-

"""Simple command-line tool for Google Image Custom Search.
Command-line application that does a search and download.
"""

__author__ = 'kakkoyun@gmail.com (Kemal Akkoyun)'

import os
import sys
import json
import argparse
import logging
import coloredlogs
import re

from google_image_search_service import GoogleImageSearchService
from image_download_service import ImageDownloadService
from metadata_file_storage_service import MetadataFileStorageService


def _initialize_argument_parser():
    parser = argparse.ArgumentParser(
        description='Image Searcher: Provide parameters to search for images for given term.')
    parser.add_argument('--term', nargs='+',
                        help='a search term to be searched')
    parser.add_argument('--file', type=argparse.FileType('r'),
                        help='a file that contains search terms')
    parser.add_argument('--count', type=int,
                        help='a parameter to specify how many images to download.')
    parser.add_argument('--api_key',
                        help='an API keys from Google Developer Console, (https://console.developers.google.com/apis/api/customsearch.googleapis.com/overview)')
    parser.add_argument('--engine_id',
                        help='an engine id from Google Custom Search Engine Console (https://cse.google.com/cse/all)')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='to enable debug mode')
    return parser


def _initialize_logger(debug=False):
    if debug:
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    coloredlogs.install()


def _sanitize_search_term(term):
    return re.sub('\W+', '', term.replace(" ", "_").lower())


def search_and_download_term(term, count, api_key, engine_id):
    logger = logging.getLogger(__name__)
    search_service = GoogleImageSearchService(api_key, engine_id)
    result = search_service.call(term, count)
    logger.debug(json.dumps(result, indent=4, sort_keys=True))
    dir_name = os.path.join('data', _sanitize_search_term(term))
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    download_service = ImageDownloadService(dir_name)
    storage_service = MetadataFileStorageService(dir_name)
    for item in result:
        url = item['link']
        download_service.call(url) and storage_service.call(url, item)


def main():
    parser = _initialize_argument_parser()

    args = parser.parse_args()
    count = args.count
    debug = args.debug

    terms = []
    if args.term:
        term = ' '.join(args.term)
        terms = [term]

    # File will have precedence
    with args.file as file:
        content = file.readlines()
        terms = [x.strip() for x in content]

    _initialize_logger(debug)
    logger = logging.getLogger(__name__)

    try:
        api_key = args.api_key if args.api_key else os.environ['GOOGLE_API_KEY']
        engine_id = args.engine_id if args.engine_id else os.environ['GOOGLE_SEARCH_ENGINE_ID']
    except KeyError, e:
        print 'You need to provide %s, either by using optional arguments or environment variables.' % e
        sys.exit()

    for term in terms:
        search_and_download_term(term, count, api_key, engine_id)


if __name__ == '__main__':
    main()
