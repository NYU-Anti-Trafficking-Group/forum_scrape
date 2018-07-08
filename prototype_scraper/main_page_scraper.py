import requests
import lxml.html
import code
import time


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


def states_cities():
    overall_response = requests.get("http://www.usasexguide.nl/forum/forum.php")
    forum_urls = get_urls(overall_response, 'div', "forumrowdata")
    subforum_lists = []
    threads = []
    for forum_url in forum_urls:
        url_response = requests.get(forum_url)
        subforum_list = get_urls(url_response, 'h2', "forumtitle")
        subforum_lists.extend(subforum_list)
    for subforum_url in subforum_lists:
        subforum_url_response = requests.get(subforum_url)
        thread_urls = get_urls(subforum_url_response, 'h3', 'threadtitle')
        threads.extend(thread_urls)

    
states_cities()
