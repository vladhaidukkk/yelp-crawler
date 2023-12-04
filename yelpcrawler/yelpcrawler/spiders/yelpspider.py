from typing import Iterable

import scrapy
from scrapy.http import Request, Response


class YelpspiderSpider(scrapy.Spider):
    name = "yelpspider"
    allowed_domains = ["www.yelp.com"]

    custom_settings = {
        "FEEDS": {
            "%(category)s-%(location)s.json": {
                "format": "json",
                "overwrite": True,
            }
        }
    }

    def __init__(self, category: str, location: str, **kwargs: dict):
        super().__init__(category=category, location=location, **kwargs)
        self.start_urls = [
            f"https://www.yelp.com/search?find_desc={category}&find_loc={location}"
        ]

    def start_requests(self) -> Iterable[Request]:
        yield scrapy.Request(
            self.start_urls[0],
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
                    "(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
                )
            },
        )

    def parse(self, response: Response):
        yield {
            "name": "test",
            "surname": "test",
        }
