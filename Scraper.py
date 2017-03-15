from bs4 import BeautifulSoup
from Utility import Content
import NewsAnalysisDAL as Provider


class Scraper:

    @property
    def parser(self):
        return "lxml"

    def get_news_text(self, content):
        soup = BeautifulSoup(content, self.parser)
        self.remove_web_archive_header(soup)
        self.remove_script_tag(soup)
        self.remove_style_tag(soup)
        return soup.get_text()

    def get_news_text(self, content, platform):
        result = ""
        soup = BeautifulSoup(content, self.parser)
        self.remove_web_archive_header(soup)
        self.remove_script_tag(soup)
        self.remove_style_tag(soup)
        news_div = soup.findAll(platform.newsdomelement, {"class": platform.newscssclass})
        for item in news_div:
            result += " " + item.get_text()
        return result

    def get_anchor_list_for_domain(self, content, fixed_domain, newspaper_domain):
        platform = Provider.get_platform_by_domain(newspaper_domain)
        if platform is None:
            return None
        result = set()
        soup = BeautifulSoup(content, self.parser)
        anchor_list = set(soup.find_all('a'))
        for anchor in anchor_list:
            if anchor.has_attr("href"):
                href = self.format_href(anchor["href"], fixed_domain)
                if self.filter_uri(href, fixed_domain, newspaper_domain) is True:
                    result.add(Content(href, platform))
                elif href.endswith("/") is False:
                    continue
        return result

    def format_href(self, href_link, domain):
        if not href_link.startswith(("http://", "https://")):
            if href_link.startswith("/"):
                if domain.endswith("/"):
                    return domain[:-1] + href_link
                else:
                    return domain + href_link
            else:
                if domain.endswith("/"):
                    return domain + href_link
                else:
                    return domain + "/" + href_link
        else:
            return href_link

    def filter_uri(self, uri, domain, newspaper_domain):
        if not uri.startswith(domain):
            return False
        if newspaper_domain not in uri:
            return False
        if uri.endswith("/"):
            return False
        if "javascript" in uri:
            return False
        if "mailto" in uri:
            return False
        if "index" in uri:
            return False
        if "whatsapp" in uri:
            return False
        if "rss" in uri:
            return False
        if "twitter.com" in uri:
            return False
        return True

    def remove_script_tag(self, soup):
        to_remove = soup("script")
        if to_remove is not None:
            for item in to_remove:
                item.extract()

    def remove_style_tag(self, soup):
        to_remove = soup("style")
        if to_remove is not None:
            for item in to_remove:
                item.extract()

    def remove_web_archive_header(self, soup):
        to_remove = soup.find("div", {"id": "wm-ipp"})
        if to_remove is not None:
            for item in to_remove:
                item.extract()