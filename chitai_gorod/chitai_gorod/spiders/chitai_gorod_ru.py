import re

import scrapy

from chitai_gorod.items import ChitaygorodItem


class ChitaiGorodRuSpider(scrapy.spiders.SitemapSpider):
    name = "chitai_gorod_ru"
    allowed_domains = ["chitai-gorod.ru"]

    sitemap_urls = ["https://www.chitai-gorod.ru/sitemap.xml"]
    sitemap_follow = ["/products"]
    sitemap_rules = [
        ("product/", "parse"),
    ]

    custom_settings = {
        "ITEM_PIPELINES": {"chitai_gorod.pipelines.MongoPipeline": 300},
        "CLOSESPIDER_ITEMCOUNT": 1500,
    }

    currency_mapping = {"₽": "RUB"}

    ## Помог ГПТ:
    def _parse_int_from_text(self, value: str | None) -> int:
        """
        Convert price strings like "1 155 ₽" (NBSP/thin spaces/etc) into ints.
        """
        if not value:
            return 0
        normalized = value.replace("&nbsp;", " ").replace("\xa0", " ")

        # Extract the first "number-ish" token, then drop any decimal part.
        # Examples:
        # - "1 155 ₽"   -> "1 155"
        # - "1155.00"   -> "1155"
        # - "1 155,00₽" -> "1 155"
        m = re.search(r"[\d\s]+(?:[.,]\d+)?", normalized)
        if not m:
            return 0

        number_token = m.group(0)
        integer_part = re.split(r"[.,]", number_token, maxsplit=1)[0]
        digits = re.sub(r"\D", "", integer_part)
        return int(digits) if digits else 0

    def _extract_price_info(self, response: scrapy.http.Response) -> tuple[int, str]:
        old_price_raw = response.xpath(
            "//span[@class='product-offer-price__old-text']/text()"
        ).get()
        if old_price_raw:
            old_price_text = (
                old_price_raw.replace("&nbsp;", " ").replace("\xa0", " ").strip()
            )
            amount = self._parse_int_from_text(old_price_text)
            currency = "RUB"
            for symbol, code in self.currency_mapping.items():
                if symbol in old_price_text:
                    currency = code
                    break
            return amount, currency

        new_price = response.xpath(
            "//div[@class='product-offer']//meta[@itemprop='price']/@content"
        ).get()
        if not new_price:
            return 0, "RUB"

        amount = self._parse_int_from_text(new_price)

        new_currency = response.xpath(
            "//div[@class='product-offer']//meta[@itemprop='priceCurrency']/@content"
        ).get()

        return amount, new_currency or "RUB"

    def parse(self, response):
        title = response.xpath("//h1/text()").get()
        isbn = response.xpath("//span[@itemprop='isbn']/span/text()").get()
        author = response.xpath("//ul[@class='product-authors']//li/a/text()").get()
        description = response.xpath(
            "//div[contains(@class, 'product-description')]/text()"
        ).get()
        price_amount, price_currency = self._extract_price_info(response)
        rating_value = response.xpath(
            "//span[@class='product-rating-detail__count']/text()"
        ).get()
        rating_count = response.xpath("//span[contains(., 'оценок')]/@content").get()
        publication_year = response.xpath(
            "//span[@itemprop='datePublished']//span/text()"
        ).get()
        pages_cnt = response.xpath(
            "//div[@id='properties']//span[@itemprop='numberOfPages']/span/text()"
        ).get()
        publisher = response.xpath("//span[@itemprop='publisher']/@content").get()
        book_cover = response.xpath("//div[@class='product-preview']//img/@src").get()

        return ChitaygorodItem(
            title=title,
            author=author,
            description=description,
            price_amount=price_amount,
            price_currency=price_currency,
            rating_value=rating_value,
            rating_count=rating_count,
            publication_year=publication_year,
            isbn=isbn,
            pages_cnt=pages_cnt,
            publisher=publisher,
            book_cover=book_cover,
            source_url=response.url,
        )
