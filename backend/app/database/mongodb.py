"""
数据库连接模块 - MongoDB文档数据库
"""
from pymongo import MongoClient
from config.settings import settings
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class MongoDBConnection:
    """MongoDB数据库连接管理"""
    
    def __init__(self):
        self._client: Optional[MongoClient] = None
        self._db = None
    
    def connect(self):
        """建立连接"""
        try:
            self._client = MongoClient(settings.MONGODB_URI)
            self._db = self._client[settings.MONGODB_DATABASE]
            # 测试连接
            self._client.server_info()
            logger.info("MongoDB连接成功")
        except Exception as e:
            logger.error(f"MongoDB连接失败: {str(e)}")
            raise
    
    def close(self):
        """关闭连接"""
        if self._client:
            self._client.close()
            logger.info("MongoDB连接已关闭")
    
    def get_collection(self, collection_name: str):
        """获取集合"""
        return self._db[collection_name]
    
    def insert_one(self, collection_name: str, document: dict):
        """插入单个文档"""
        collection = self.get_collection(collection_name)
        return collection.insert_one(document)
    
    def insert_many(self, collection_name: str, documents: list):
        """批量插入文档"""
        collection = self.get_collection(collection_name)
        return collection.insert_many(documents)
    
    def find_one(self, collection_name: str, query: dict):
        """查询单个文档"""
        collection = self.get_collection(collection_name)
        return collection.find_one(query)
    
    def find_many(self, collection_name: str, query: dict = None, limit: int = 0):
        """查询多个文档"""
        collection = self.get_collection(collection_name)
        return list(collection.find(query or {}).limit(limit))


# 全局连接实例
mongodb_conn = MongoDBConnection()
