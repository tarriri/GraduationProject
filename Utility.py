from memento_client import MementoClient
import requests
from urllib.parse import urlparse


class Newspaper:

    def __init__(self, name, domain, commentary_url):
        self.name = name
        self.domain = domain
        self.commentary_url = domain + commentary_url


class Content:

    def __init__(self, content_uri, platform):
        self.content_uri = content_uri
        self.platform = platform


class MementoError(Exception):

    def __init__(self, timestamp, domain):
        self.args = "No memento has found"
        self.timestamp = timestamp
        self.domain = domain


class Utility:
    memento = MementoClient()
    wayback_url = "http://archive.org/wayback/available?url={}&timestamp={}"

    # For given date and domain, returns closest snapshot of domain in web archive.
    def get_uri_of_date(self, given_date, domain):
        try:
            memento_info = self.memento.get_memento_info(domain, given_date)
            if memento_info.get("mementos"):
                mementos = memento_info.get("mementos")
                if mementos is not None and mementos.get("closest").get("uri") and \
                                mementos.get("closest").get("uri").__len__() > 0:
                    return mementos.get("closest").get("uri")[0]
            raise Exception()
        except Exception:
            timestamp = given_date.strftime("%Y%m%d%H%M%S")
            wayback_get = requests.get(self.wayback_url.format(domain, timestamp))
            if wayback_get.status_code == 200:
                result = wayback_get.json()["archived_snapshots"]
                if result is not None and result.get("closest") and result["closest"]["available"] is True:
                    return result["closest"]["url"]
            return None

    def get_fixed_domain(self, uri):
        parsed_uri = urlparse(uri)
        return '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

    def create_json_data(self, text, url):
        return {"url": url, "text": text}
