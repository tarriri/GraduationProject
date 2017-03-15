import requests
from Scraper import Scraper
import datetime
from Utility import Newspaper
from Utility import Utility
import NewsAnalysisDAL as Provider

# initialization
start_date = datetime.datetime.strptime("01-12-2016", "%d-%m-%Y")
end_date = datetime.datetime.strptime("02-12-2016", "%d-%m-%Y")
scraper = Scraper()
utility = Utility()
newspaper_list_db = Provider.get_platform_list()
newspaper_list = set((Newspaper("Hürriyet", "http://www.hurriyet.com.tr", "/yazarlar/"),\
                      Newspaper("Sabah", "http://www.sabah.com.tr", "/yazarlar"),\
                      Newspaper("Sözcü", "http://www.sozcu.com.tr", "/kategori/yazarlar"),\
                      Newspaper("Posta", "http://www.posta.com.tr", "/yazarlar"),\
                      Newspaper("Türkiye", "http://www.turkiyegazetesi.com.tr/", "/yazarlar"),\
                      Newspaper("Millliyet", "http://www.milliyet.com.tr", "/Yazarlar"),\
                      Newspaper("Habertürk", "http://www.haberturk.com", "/htyazarlar"),\
                      Newspaper("Yeni Şafak", "http://www.yenisafak.com", "/Yazarlar"),\
                      Newspaper("Akşam", "http://www.aksam.com.tr", "/yazarlar"),\
                      Newspaper("Takvim", "http://www.takvim.com.tr", "/yazarlar")))


def main():
    time_range = [start_date + datetime.timedelta(days=x) for x in range(0, (end_date - start_date).days)]
    content_uri = set()
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
                    content_uri.update(scraper.get_anchor_list_for_domain(r_get_homepage.content, utility.get_fixed_domain(home_uri), item.urldomain))
    print("URL list extracted: " + str(content_uri.__len__()) + " found")
    for content in content_uri:
        # Gets news text for a given specific url: makes get request, removes unnecessary text from response.
        r_get = requests.get(content.content_uri)
        if r_get.status_code == 200:
            print(scraper.get_news_text(r_get.content, content.platform))


def foo():
    deneme = requests.get("http://web.archive.org/web/20161130210521/http://www.hurriyet.com.tr/aof-soru-ve-cevaplari-aciklandi-aof-sinav-sonuclari-ne-zaman-aciklanacak-40291170")
    if deneme.status_code == 200:
        print("got it")
        print(scraper.get_news_text(deneme.content, newspaper_list_db[0]))

if __name__ == "__main__":
    main()
    exit()

