import requests
import os
from bs4 import BeautifulSoup
from pprint import pprint

def main():
    url_cnn = 'http://lite.cnn.com/en'
    url_npr = 'https://text.npr.org/'

    low_level_urls_npr = parse_base_urls(url_npr)
    validURLs_npr = parse_urls_NPR(url_npr, low_level_urls_npr)
    write_to_txt_NPR(validURLs_npr)

    low_level_urls_cnn = parse_base_urls(url_cnn)
    validURLs_cnn = parse_urls_CNN(url_cnn, low_level_urls_cnn)
    write_to_txt_CNN(validURLs_cnn)

def parse_base_urls(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.findAll('a', href=True)
    base = []
    for link in links:
        base.append(link.get('href'))
    return base


def parse_urls_NPR(urlRoot, urls):
    validURLs = []
    for url in urls:
        if "/s." in url:
            parsedURL = url.replace("/", "")
            validURLs.append(urlRoot+parsedURL)

    return validURLs

def write_to_txt_NPR(validURLs):
    for article in validURLs:
        print(article)
        text = parse_page_NPR(article)
        title = article.rsplit('=',1)[-1]
        writePath = os.getcwd()+"\\txtfiles\\"+title+".txt"
        with open(writePath,"w", encoding='utf-8') as text_file:
            text_file.write(text)

def parse_page_NPR(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tags = soup.find_all('p')
    text = ""
    for tag in tags:
        if 'NPR' not in tag.getText() and 'Home' not in tag.getText() and 'By' not in tag.getText():
            text = text + tag.getText()
    return text


def parse_urls_CNN(urlRoot,urls):
    validURLs = []
    for url in urls:
        if "article" in url:
            parsedURL = url.replace("/en", "")
            validURLs.append(urlRoot+parsedURL)

    return validURLs
        
def write_to_txt_CNN(validURLs):
    for article in validURLs:
        print(article)
        text = parse_page_CNN(article)
        title = article.rsplit('/',1)[-1]
        writePath = os.getcwd()+"\\txtfiles\\"+title+".txt"
        with open(writePath,"w", encoding='utf-8') as text_file:
            text_file.write(text)

def parse_page_CNN(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tags = soup.find_all('p')
    text = ""
    for tag in tags:
        if 'CNN' not in tag.getText() and 'Inc' not in tag.getText():
            text = text + tag.getText()
    return text

main()


   


