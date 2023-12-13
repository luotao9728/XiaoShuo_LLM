import requests
import re
from bs4 import BeautifulSoup

class scrape_xbiquge():
    def __init__(self):
        self.titles_re = re.compile(r'<a href="([^\"]+\.html)">([\s\S]+?)<\/a>')
        self.novels_re = re.compile(r'<a href="(https://www\.xbiquge\.bz/book/\d+/)" title="([^"]+)">')

    def scrape_novels(self, url):
        response = requests.get(url)
        novels = re.findall(self.novels_re, response.text)
        return novels

    def scrape_titles(self, url):
        response = requests.get(url)
        return re.findall(self.titles_re, response.text)

    def scrape_chapter(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        texts = soup.find_all(id="content")
        return " ".join([text.get_text() for text in texts])

    def save_novels(self):
        novels = self.scrape_novels(self.url)
        for novel_url, novel in novels:
            with open(novel + '.txt', 'w', encoding='utf-8') as file:
                titles = self.scrape_titles(novel_url)
                for title_url, title in titles:
                    chapter_content = self.scrape_chapter(novel_url + title_url).strip().replace('******', '').replace('    ', '\n')
                    try:
                        first_line = chapter_content.index('\n')
                        chapter_content = chapter_content[first_line+1:]
                    except ValueError:
                        continue
                    file.write(title + '\n')
                    file.write(chapter_content + '\n\n')
            print(novel + '.txt saved!')

    def save_xbiquge(self):
        for i in range(1, 100):
            self.url = 'https://www.xbiquge.bz/top/allvote/%d.html' % i
            self.save_novels()

scrape = scrape_xbiquge()
scrape.save_xbiquge()
