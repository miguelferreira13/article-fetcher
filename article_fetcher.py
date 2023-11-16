"""Script that fetches articles and prints the top 10"""

from dataclasses import dataclass, field
from typing import List
import argparse
import csv

import requests
from tqdm import tqdm


@dataclass
class Article:

    """Article Class"""

    title: str
    url: str
    author: str
    num_comments: int
    story_id: int
    story_title: str
    # story_url: str
    # parent_id: int
    # created_at: int

    @classmethod
    def from_json(cls, data:dict):
        """Initialize an instance of Article from json data

        Args:
            data (dict): Json / Dict data

        Returns:
            Article: object
        """
        return cls(
            data.get('title'),
            data.get('url'),
            data.get('author'),
            data.get('num_comments'),
            data.get('story_id'),
            data.get('story_title'),
            # data.get('story_url'),
            # data.get('parent_id'),
            # data.get('created_at')
        )

@dataclass
class Articles:

    """Articles class"""

    articles: List[Article] = field(default_factory=list)

    def fetch_page(self, page_number:int) -> dict:

        """Fetches the json response  given a page

        Args:
            page_number (int): Page number to fetch

        Returns:
            dict: json response / dict
        """

        url = f"https://jsonmock.hackerrank.com/api/articles?page={page_number}"
        response = requests.get(url, timeout=5)
        return response.json()

    def fetch_all_articles(self):

        """Fetches all the articles"""

        total_pages = self.fetch_page(1)['total_pages']
        for page in tqdm(range(1, total_pages + 1), desc="Fetching Articles"):
            response = self.fetch_page(page)
            for article_data in response['data']:
                article = Article.from_json(article_data)
                self.articles.append(article)

    def get_top_articles(self, n:int):
        """Fetches all articles and get the top n

        Args:
            n (int): number of results

        Returns:
            list[Article]: List of Articles
        """
        self.fetch_all_articles()
        filtered_articles = [article for article in self.articles if
                             (article.title or article.story_title) and article.num_comments]
        sorted_articles = sorted(filtered_articles, key=lambda x: x.num_comments, reverse=True)
        return sorted_articles[:n]




if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Fetch top articles and optionally download CSV')
    parser.add_argument('--csv', action='store_true', help='Download top articles as CSV')

    args = parser.parse_args()

    articles = Articles()
    top_articles = articles.get_top_articles(10)

    if args.csv:
        # save csv
        with open('top_articles.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = Article.__dataclass_fields__.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for artc in top_articles:
                writer.writerow(artc.__dict__)
    else:
        # print to console
        for i, artc in enumerate(top_articles, start=1):
            title = artc.title if artc.title else artc.story_title
            print(f"{i:<5} {title[:80]:<80}  #{artc.num_comments:<20}")
