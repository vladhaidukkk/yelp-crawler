# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html


from random import randint
from urllib.parse import urlencode

import requests
from scrapy.crawler import Crawler
from scrapy.http import Request
from scrapy.settings import Settings
from scrapy.spiders import Spider


class FakeUserAgentMiddleware:
    @classmethod
    def from_crawler(cls, crawler: Crawler):
        return cls(crawler.settings)

    def __init__(self, settings: Settings) -> None:
        self.scrapeops_api_key = settings.get("SCRAPEOPS_API_KEY")
        self.scrapeops_endpoint = settings.get("SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT")
        self.scrapeops_results_number = settings.get("SCRAPEOPS_RESULTS_NUMBER")
        self.scrapeops_fake_user_agent_enabled = (
            self.scrapeops_api_key
            and self.scrapeops_endpoint
            and settings.get("SCRAPEOPS_FAKE_USER_AGENT_ENABLED")
        )
        self.fake_user_agents = self._load_fake_user_agents()

    def _load_fake_user_agents(self):
        if not self.scrapeops_fake_user_agent_enabled:
            return []

        params = {"api_key": self.scrapeops_api_key}
        if self.scrapeops_results_number:
            params["num_results"] = self.scrapeops_results_number

        response = requests.get(self.scrapeops_endpoint, params=urlencode(params))
        data = response.json()
        return data.get("result", [])

    def _get_fake_user_agent(self):
        try:
            rand_idx = randint(0, len(self.fake_user_agents) - 1)
        except Exception:
            return None
        else:
            return self.fake_user_agents[rand_idx]

    def process_request(self, request: Request, spider: Spider):
        request.headers["User-Agent"] = self._get_fake_user_agent()
