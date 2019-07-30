"""Provide access to google analytics data for search.

"""


class GAData(object):
    def __init__(self, ga_client, date):
        self.client = ga_client
        self.date = date
        self.date_idstr = date.strftime("%Y%m%d")
        self.date_str = '%04d-%02d-%02dT00:00:00Z' % (
            self.date.year,
            self.date.month,
            self.date.day,
        )

    def fetch_traffic_info(self):
        """Fetch info on views of pages.

        Returns a dict keyed by path.  Values are a tuple of:

         - total number of views (unique per session)
         - boolean: True iff the page consistently returns a not found error.

        """
        not_found_title = 'Page not found - 404'
        result = {}
        for row in self.client.fetch(
            'search', self.date,
            metrics='ga:uniquePageViews',
            dimensions='ga:pagePath,ga:pageTitle',
            sort='-ga:uniquePageViews',
            name_map={
                'uniquePageViews': 'views',
                'pagePath': 'path',
                'pageTitle': 'title',
            },
        ):
            path = row['path']
            views = row['views']
            title = row['title']
            not_found = (title == not_found_title)
            item = result.get(path)
            if item is None:
                result[path] = [views, not_found]
            else:
                item[0] += views
                item[1] = (item[1] and not_found)
        return result
