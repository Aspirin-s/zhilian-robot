"""
数据处理管道
"""
from app.database.mongodb import mongodb_conn
import re
import logging

logger = logging.getLogger(__name__)


class TextCleaningPipeline:
    """文本清洗管道"""
    
    def process_item(self, item, spider):
        """清洗文本数据"""
        if 'content' in item:
            # 去除多余空白
            item['content'] = re.sub(r'\s+', ' ', item['content']).strip()
            
            # 去除HTML标签
            item['content'] = re.sub(r'<[^>]+>', '', item['content'])
        
        if 'title' in item:
            item['title'] = item['title'].strip()
        
        return item


class MongoDBPipeline:
    """MongoDB存储管道"""
    
    def __init__(self):
        self.collection_name = 'crawled_data'
    
    def open_spider(self, spider):
        """爬虫开启时连接数据库"""
        try:
            mongodb_conn.connect()
            logger.info("MongoDB管道已连接")
        except Exception as e:
            logger.error(f"MongoDB管道连接失败: {str(e)}")
    
    def close_spider(self, spider):
        """爬虫关闭时断开连接"""
        mongodb_conn.close()
    
    def process_item(self, item, spider):
        """保存数据到MongoDB"""
        try:
            mongodb_conn.insert_one(self.collection_name, dict(item))
            logger.info(f"数据已保存: {item.get('title', 'N/A')}")
        except Exception as e:
            logger.error(f"数据保存失败: {str(e)}")
        
        return item


class Neo4jPipeline:
    """Neo4j图数据库管道"""
    
    def process_item(self, item, spider):
        """提取实体和关系并存入图数据库"""
        # TODO: 调用NLP模块进行实体和关系提取
        # TODO: 存入Neo4j
        return item
