from pymongo import MongoClient
import time
from dotenv import load_dotenv
import os

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

class MongoCryptoDatabase:
    def __init__(self):
        # خواندن Connection String از متغیر محیطی
        connection_string = os.getenv("MONGO_CONNECTION_STRING")
        if not connection_string:
            raise ValueError("MONGO_CONNECTION_STRING در فایل .env تعریف نشده است!")
        
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