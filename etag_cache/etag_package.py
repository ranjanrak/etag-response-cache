"""
@author: rakeshr
"""

"""
Python package for caching HTTP response based on etag
"""

import os
import dbm
import json


class EtagCache(object):
    
    # Default cache location
    _dir_path = os.path.join(os.getenv("HOME"), ".pyapp")

    def __init__(self, dir_path=None):
        self.dir_path = dir_path or self._dir_path
        self.etag_path = os.path.join(self.dir_path, "etag")
        self.cache_path = os.path.join(self.dir_path, "cache")

    def save_etag(self, response):
        """ Store etag to etag path """
        # Store Etag data to user's dir path
        if "Etag" in response.headers:
            # Create client directory if it doesn't exists
            if not os.path.exists(self.dir_path):
                os.makedirs(self.dir_path)

            # Create etag file if it doesn't exists
            if not os.path.exists(self.etag_path):
                with dbm.open(self.etag_path, 'c') as db:
                    db[response.url] = response.headers["Etag"]
            else:
                # Update the Etag value if exists
                with dbm.open(self.etag_path, 'w') as db:
                    db[response.url] = response.headers["Etag"]

    def add_etag(self, method, headers, url):
        """ Add etag to request header """
        # Add Etag header for GET request
        if method == 'GET' and os.path.exists(self.etag_path):
            with dbm.open(self.etag_path, 'r') as db:
                headers["If-None-Match"] = db.get(url)
        return headers

    def add_read_cache(self, response):
        """ Return cache/response data """
        if response.status_code == 304:
            with dbm.open(self.cache_path, 'r') as db:
                byte_response = db.get(response.url)
        else:
            data = response.content.decode("utf-8")
            with dbm.open(self.cache_path, 'c') as db:
                db[response.url] = data
            byte_response = response.text
        # Return dictionary
        json_data = json.loads(byte_response)
        return json_data
