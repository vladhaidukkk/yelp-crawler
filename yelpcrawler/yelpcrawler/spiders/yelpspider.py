import scrapy
from scrapy.http import Response
from yelpcrawler.items import BusinessItem


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

    def parse(self, response: Response):
        list_items = response.css("#main-content > div > ul > li")
        for idx, item in enumerate(list_items):
            section_title = item.css("div > h2::text").get()
            if section_title and section_title.startswith("All "):
                businesses = list_items[idx + 1 : idx + 11]

        for idx, business in enumerate(businesses, start=1):
            page = business.css("h3 > span > a::attr(href)").get()
            page_url = f"https://www.yelp.com{page}"
            yield scrapy.Request(page_url, callback=self._parse_business_page)

        next_page_url = response.css('a[class^="next-link"]::attr(href)').get()
        if next_page_url:
            yield response.follow(next_page_url, self.parse)

    def _parse_business_page(self, response: Response):
        business_id = response.css('meta[name="yelp-biz-id"]::attr(content)').get()
        print(f"===> Business ID: {business_id}")
        api_url = (
            f"https://www.yelp.com/biz/{business_id}/props?osq={self.category}"
            f"&override_cta=Request+a+Quote"
        )
        yield scrapy.Request(
            api_url, callback=self._create_business_api_parser(response.url)
        )

    def _create_business_api_parser(self, yelp_url: str):
        def parse_business_api(response: Response):
            data = response.json()["bizDetailsPageProps"]
            portfolio_props = data.get("bizPortfolioProps")
            reviews = data["reviewFeedQueryProps"]["reviews"]

            website = (
                portfolio_props["ctaProps"].get("website")
                if portfolio_props and "ctaProps" in portfolio_props
                else None
            )

            business_item = BusinessItem()
            business_item["name"] = data["businessName"]
            business_item["yelp_url"] = yelp_url
            business_item["website_url"] = (
                f"https://www.yelp.com{website}" if website else None
            )
            business_item["rating"] = sum(review["rating"] for review in reviews) / len(
                reviews
            )
            business_item["reviews_number"] = len(reviews)
            business_item["reviews"] = [
                {
                    "name": review["user"].get("markupDisplayName"),
                    "location": review["user"].get("displayLocation"),
                    "date": review["localizedDate"],
                }
                for review in reviews[:5]
            ]
            yield business_item

        return parse_business_api
