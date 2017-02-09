import logging
import json

from os import path as os_path
from urlparse import urlparse

logger = logging.getLogger(__name__)


class MetadataFileStorageService:
    def __init__(self, dir_path):
        self.dir_path = dir_path

    def call(self, url, data):
        """
        Save metadata of image to a text file.

        Parameters
        ----------
        url : string
            URL of image
        data : Dictionary
            Metadata of image as a Dictionary

        """

        url_object = urlparse(url)
        file_name = os_path.basename(url_object.path).split('.')[0]
        file_path = os_path.join(self.dir_path, '%s.json' % file_name)

        # Download the file if it does not exist.
        if not os_path.isfile(file_path):
            logger.info('Writing metadata file, %s ' % file_path)
            with open(file_path, 'w') as outfile:
                json.dump(data, outfile)
        else:
            logger.info('File already exists, %s' % file_path)
