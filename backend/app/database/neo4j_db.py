"""
数据库连接模块 - Neo4j图数据库
"""
from neo4j import GraphDatabase
from config.settings import settings
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class Neo4jConnection:
    """Neo4j数据库连接管理"""
    
    def __init__(self):
        self._driver: Optional[GraphDatabase.driver] = None
    
    def connect(self):
        """建立连接"""
        try:
            self._driver = GraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
            )
            logger.info("Neo4j连接成功")
        except Exception as e:
            logger.error(f"Neo4j连接失败: {str(e)}")
            raise
    
    def close(self):
        """关闭连接"""
        if self._driver:
            self._driver.close()
            logger.info("Neo4j连接已关闭")
    
    def execute_query(self, query: str, parameters: dict = None):
        """执行Cypher查询"""
        if not self._driver:
            logger.error("Neo4j driver 未初始化")
            return []
        
        try:
            with self._driver.session() as session:
                result = session.run(query, parameters or {})
                # 完整读取所有记录
                records = []
                for record in result:
                    record_dict = {}
                    for key in record.keys():
                        value = record[key]
                        # 处理 Neo4j 节点对象
                        if hasattr(value, '_properties'):
                            record_dict[key] = dict(value._properties)
                        else:
                            record_dict[key] = value
                    records.append(record_dict)
                return records
        except Exception as e:
            logger.error(f"查询执行失败: {str(e)}")
            return []
    
    def execute_write(self, query: str, parameters: dict = None):
        """执行写入操作"""
        with self._driver.session() as session:
            result = session.write_transaction(
                lambda tx: tx.run(query, parameters or {})
            )
            return result


# 全局连接实例
neo4j_conn = Neo4jConnection()
