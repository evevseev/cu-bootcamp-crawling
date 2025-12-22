# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class ChitaiGorodPipeline:
    def process_item(self, item, spider):
        return item


class MongoPipeline:
    mongo_db: str
    mongo_uri: str

    def __init__(self):
        self.mongo_db = "items"
        self.mongo_uri = (
            f"mongodb://admin:pass@localhost:27017/{self.mongo_db}?authSource=admin"
        )
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db["collection"]

    def process_item(self, item, spider):
        if item:
            doc = ItemAdapter(item).asdict()
            isbn = (doc.get("isbn") or "").strip()
            if not isbn:
                spider.logger.warning(
                    "Dropping item without ISBN (source_url=%s, title=%s)",
                    doc.get("source_url"),
                    doc.get("title"),
                )
                raise DropItem("Missing ISBN")
            self.collection.update_one({"isbn": isbn}, {"$set": doc}, upsert=True)
        return item

    def close_spider(self, spider):
        self.client.close()
