from bs4 import BeautifulSoup
import requests
import re
import time
import cloudscraper


#取得特定網址網頁內容
def get_page_content(url):
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)
    htmlContent = response.text
    
    # 解析 HTML
    soup = BeautifulSoup(htmlContent, 'html.parser')

    return soup

