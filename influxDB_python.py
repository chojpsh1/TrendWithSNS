import os

class database():
    """database"""

    insert_query = "curl -i -XPOST 'http://localhost:8086/write?db=GP' -u admin:admin --data-binary '"
    id_insert_query = '%s,id=%s favorite_count=%s,retweet_count=%s,followers_count=%s\n'

    def insert(self, curl_str):
        run_curl = os.system(curl_str)
        return run_curl
