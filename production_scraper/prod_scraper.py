import scrapy
import IPython
import requests
import lxml.html


def get_urls(response, tag, klass):
    """
    get the urls for each level down in the subsequent hierachy
    
    Parameters:
    @text - is the text of the html page
    @klass - is the css class of the link to be scraped
    """
    base_url = "http://www.usasexguide.nl/forum/"
    html = lxml.html.fromstring(response.text)
    xpath_query = '//{}[@class="{}"]//@href'.format(tag, klass)
    url_endings = html.xpath(xpath_query)
    return [base_url+url_ending for url_ending in url_endings]


def generate_start_urls():
    overall_response = requests.get("http://www.usasexguide.nl/forum/forum.php")
    return get_urls(overall_response, 'div', "forumrowdata")

class USASexGuidesForumSpider(scrapy.Spider):
    name = "usa_sex_guides_forum_spider"
    start_urls = generate_start_urls()

    def parse(self, response):
        base_url = "http://www.usasexguide.nl/forum/"
        for forum in response.xpath('//h2[@class="forumtitle"]//@href'):
            url = forum.root

class USASexGuidesSubForumSpider(scrapy.Spider):
    name = "usa_sex_guides_subforum_spider"
    start_urls = generate_start_urls()

    def parse(self, response):
        base_url = "http://www.usasexguide.nl/forum/"
        for forum in response.xpath('//h3[@class="threadtitle"]//@href'):
            url = forum.root



