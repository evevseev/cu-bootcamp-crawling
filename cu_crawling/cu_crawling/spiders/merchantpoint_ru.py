import scrapy
import scrapy.http


class MerchantpointRuSpider(scrapy.Spider):
    name = "merchantpoint_ru"
    allowed_domains = ["merchantpoint.ru"]
    start_urls = ["https://merchantpoint.ru/brand/4390"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "cu_crawling.pipelines.CuCrawlingPipeline": 300,
        }
    }

    def parse(self, response: scrapy.http.Response):
        ord_desc = (
            response.xpath("//div[contains(@class, 'description_brand')]/text()")
            .get()
            .strip()
        )  # type: ignore
        merchant_urls = response.xpath(
            "//table[@class='finance-table']//a/@href"
        ).getall()

        yield from response.follow_all(
            urls=merchant_urls,  # type: ignore
            cb_kwargs={"org_desc": ord_desc},
            callback=self.parse_merchant,
        )

    # merchant_name - //h1/text()
    # mcc - //section[@id='description']//p/a/text()
    # address - //div//p[contains(., 'Адрес')]/text()
    # geo_coordinates - //div//p[contains(., 'Гео')]/text()
    # org_name - //p/a[contains(@href,'brand')]/text()

    # org_description - //div[contains(@class, 'description_brand')]/text()

    def parse_merchant(self, response: scrapy.http.Response, org_desc: str):
        return {
            "org_name": response.xpath("//p/a[contains(@href,'brand')]/text()").get(),
            "org_desc": org_desc,
            "merchant_name": response.xpath("//h1/text()").get(),
            "mcc": response.xpath("//section[@id='description']//p/a/text()").get(),
            "address": response.xpath("//div//p[contains(., 'Адрес')]/text()").get(),
            "geo_coordinates": response.xpath(
                "//div//p[contains(., 'Гео')]/text()"
            ).get(),
            "source_url": response.url,
        }
