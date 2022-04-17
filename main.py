import os

import requests
import string
from bs4 import BeautifulSoup


def get_source(n_pages, article_type):
    while n_pages > 0:
        url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=' + str(n_pages)
        response = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
        if response:
            dir_name = "PAGE_" + str(n_pages)
            os.mkdir(dir_name)
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.findAll('article')
            for article in articles:
                type = article.find('span', {'class': 'c-meta__type'}).text
                if type == article_type:
                    link = "https://www.nature.com" + article.find('a')['href']
                    body_article = requests.get(link)
                    print(link)
                    if body_article:
                        soup = BeautifulSoup(body_article.text, 'html.parser')
                        content = soup.find('div', {'class': 'c-article-body u-clearfix'}).text.strip()
                        path = os.path.join(dir_name, get_name(article.find('a', {'itemprop': 'url'}).text) + ".txt")
                        file = open(path, 'w')
                        file.write(content)
                        file.write("\nLink to the article: " + link)
                        file.close()
                        print("Content saved.")
                    else:
                        break

        else:
            print(f"The URL returned X {response}")
        n_pages -= 1


def get_name(name):
    table = name.maketrans(" -", "__")
    name = name.translate(str.maketrans('', '', string.punctuation))
    return name.translate(table)


if __name__ == "__main__":
    n_pages = int(input("Number of pages to get searched: "))
    type_article = input("Article type: ")
    print(get_source(n_pages, type_article))
