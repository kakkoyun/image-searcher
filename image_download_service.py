import logging

from os import path as os_path
from urllib import urlretrieve
from urlparse import urlparse

logger = logging.getLogger(__name__)


class ImageDownloadService:
    def __init__(self, dir_path):
        self.dir_path = dir_path

    def call(self, url):
        """
        Downloads and saves Image.

        Parameters
        ----------
        url : string
            URL of image
        filename : string
            Filename of image

        """
        url_object = urlparse(url)
        file_name = os_path.basename(url_object.path)
        file_path = os_path.join(self.dir_path, file_name)

        # Download the file if it does not exist.
        if not os_path.isfile(file_path):
            logger.info('Downloading, %s ' % file_path)
            urlretrieve(url, file_path)
        else:
            logger.info('File already exists, %s' % file_path)
