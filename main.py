from http.client import RemoteDisconnected
import requests
from Scraper import Scraper
import datetime
from Utility import Utility
import NewsAnalysisDatabase as Provider

# initialization
start_date = datetime.datetime.strptime("01-12-2016", "%d-%m-%Y")
end_date = datetime.datetime.strptime("31-01-2017", "%d-%m-%Y")
scraper = Scraper()
utility = Utility()
newspaper_list_db = Provider.get_platform_list()


def main():
    # collect_url()
    collect_articles()
    # time_range = [start_date + datetime.timedelta(days=x) for x in range(0, (end_date - start_date).days)]
    # content_uri = set()
    # for item in newspaper_list_db:
    #     uri_range = set()
    #     # For given date range, calls get_uri_of_date method.
    #     for date in time_range:
    #         uri_range.add(utility.get_uri_of_date(date, item.urldomain))
    #         uri_range.add(utility.get_uri_of_date(date, item.urldomain + item.commentaryurl))
    #     # Gets all uri's of web site via home page, using get_anchor_list_for_domain method
    #     for home_uri in uri_range:
    #         if home_uri is not None:
    #             r_get_homepage = requests.get(home_uri)
    #             if r_get_homepage.status_code == 200:
    #                 content_uri.update(scraper.get_anchor_list_for_domain(r_get_homepage.content, utility.get_fixed_domain(home_uri), item.urldomain))
    #                 print(str(content_uri.__len__()) + " URL extracted")
    # for content in content_uri:
    #     # Gets news text for a given specific url: makes get request, removes unnecessary text from response.
    #     try:
    #         r_get = requests.get(content.content_uri)
    #     except RemoteDisconnected as e:
    #         print(e.line)
    #         continue
    #     if r_get.status_code == 200:
    #         scraped_news = scraper.get_news_text(r_get.content, content.platform)
    #         if scraped_news and scraped_news.strip():
    #             Provider.create_collected_news(scraped_news, content.content_uri)
    #             print("article added")
    #         else:
    #             print("Nothing found on: " + content.content_uri)


def collect_url():
    time_range = [start_date + datetime.timedelta(days=x) for x in range(0, (end_date - start_date).days)]
    for item in newspaper_list_db:
        uri_range = set()
        # For given date range, calls get_uri_of_date method.
        for date in time_range:
            uri_range.add(utility.get_uri_of_date(date, item.urldomain))
            uri_range.add(utility.get_uri_of_date(date, item.urldomain + item.commentaryurl))
        # Gets all uri's of web site via home page, using get_anchor_list_for_domain method
        for home_uri in uri_range:
            if home_uri is not None:
                r_get_homepage = requests.get(home_uri)
                if r_get_homepage.status_code == 200:
                    content_list = scraper.get_anchor_list_for_domain(r_get_homepage.content, utility.get_fixed_domain(home_uri),
                                                           item.urldomain)
                    if len(content_list) > 0:
                        for content in content_list:
                            if content is not None:
                                Provider.create_url_information(content.content_uri, content.platform)
                    print(str(len(content_list)) + " more URL extracted")


def collect_articles():
    uri_list = Provider.get_url_information_list()
    for uri_inf in uri_list:
        # Gets news text for a given specific url: makes get request, removes unnecessary text from response.
        if uri_inf.iscollected == 0:
            try:
                r_get = requests.get(uri_inf.urltext)
            except RemoteDisconnected as e:
                print(e.line)
                continue
            if r_get.status_code == 200:
                platform = Provider.get_platform_by_object_id(uri_inf.platformid)
                if platform is not None:
                    scraped_news = scraper.get_news_text(r_get.content, platform)
                    if scraped_news and scraped_news.strip():
                        Provider.create_collected_news(scraped_news, uri_inf.urltext)
                        Provider.mark_as_collected_url(uri_inf.objectid)
                        print("article added")
                    else:
                        print("Nothing found on: " + uri_inf.urltext)

if __name__ == "__main__":
    main()
    exit()

