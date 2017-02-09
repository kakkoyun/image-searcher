from googleapiclient.discovery import build


class GoogleImageSearchService:
    DEFAULT_SEARCH_FIELDS = 'items(fileFormat,image(byteSize,height,width),labels,link,mime,snippet,title),queries,searchInformation(searchTime,totalResults)'
    DEFAULT_PAGE_SIZE = 10

    def __init__(self, api_key, engine_id):
        """
        Google Image search service wrapper.

        Parameters
        ----------
        api_key : string
            Google API Key that you obtain from https://console.developers.google.com/apis/api/customsearch.googleapis.com/overview
        engine_id : string
            Custom Search Engine Id that you obtain from https://cse.google.com/cse/all

        Returns
        -------
        Dictionary
            Returns search results as a Dictionary

        """
        self.api_key = api_key
        self.engine_id = engine_id

    def _calculate_page_count(self, count):
        page_count = count / self.DEFAULT_PAGE_SIZE
        if count % self.DEFAULT_PAGE_SIZE:
            page_count += 1
        return page_count

    def image_search(self, term, count=10, search_fields=DEFAULT_SEARCH_FIELDS):
        """
        Image search by give term.

        Parameters
        ----------
        term : string
            Keyword to search
        fields : string
            Field descriptions to include in search results

        Returns
        -------
        Dictionary
            Returns search results as a Dictionary

        """
        service = build('customsearch', 'v1', developerKey=self.api_key)

        items = []
        start_index = 1
        for page in range(0, self._calculate_page_count(count)):
            print 'Downloading search terms, page %d' % page
            response = service.cse().list(
                q=term,
                cx=self.engine_id,
                searchType='image',
                fields=search_fields,
                start=start_index
            ).execute()
            items += response['items']
            start_index = response['queries']['nextPage'][0]['startIndex']

        return items
