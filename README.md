# Yelp Crawler

The purpose is to develop a yelp crawler that scraps all the businesses from Yelp website.

## Get Started

1. At the beginning create a virtual environment and activate it:

```shell
python -m venv venv
source ./venv/bin/activate
```

2. Install dependencies from the `requirements.txt` with `make install` command:

```shell
make install
```

3. *(Optional):* To manage project dependencies use `pip-tools` with `make compile` and `make sync` commands:

```shell
pip install pip-tools
make compile  # create requirements.txt from requirements.in
make sync  # sync site-packages with requirements.txt
```

## Usage

To run the crawler, you need to be in the `yelpcrawler` directory and run this command:

```shell
scrapy crawl yelpspider -a category="Electricians" -a location="San Francisco, CA"
```
