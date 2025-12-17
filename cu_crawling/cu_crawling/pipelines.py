# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CuCrawlingPipeline:
    def process_item(self, item: dict[str, str | None], spider):
        address = item.get("address")
        if address is not None:
            item["address"] = address.split("—")[-1].strip()

        org_name = item.get("org_desc")
        if org_name is not None:
            item["org_desc"] = org_name.replace(item["org_name"], "").strip()

        merchant_name = item.get("merchant_name")
        if merchant_name is not None:
            item["merchant_name"] = merchant_name.strip()

        mcc = item.get("mcc")
        if mcc is not None:
            item["mcc"] = int(mcc)

        geo_coordinates = item.get("geo_coordinates")
        if geo_coordinates is not None:
            item["geo_coordinates"] = tuple(
                float(c) for c in geo_coordinates.split(", ")
            )

        return item
