from pymongo import MongoClient
import time
from dotenv import load_dotenv
import os

load_dotenv()



class MongoCryptoDatabase:
    def __init__(self, connection_string=os.getenv("MONGODB_CONNECTION_STRING")):
        # جایگزین connection_string با رشته‌ای که از Atlas گرفتی
        self.client = MongoClient(connection_string)
        self.db = self.client["crypto_db"]
        self.collection = self.db["crypto_data"]
        print("اتصال به MongoDB Atlas برقرار شد.")

    def store_data(self, service, data):
        # حذف داده‌های قبلی برای این سرویس
        self.collection.delete_many({"service": service})
        # ذخیره داده جدید با زمان
        document = {
            "service": service,
            "data": data,
            "timestamp": int(time.time())
        }
        self.collection.insert_one(document)
        print(f"داده‌ها برای سرویس {service} در MongoDB Atlas ذخیره شد. تعداد: {len(data)}")

    def get_data(self, service):
        result = self.collection.find_one({"service": service})
        if result:
            return result["data"]
        return []

    def close(self):
        self.client.close()
        print("اتصال به MongoDB Atlas بسته شد.")