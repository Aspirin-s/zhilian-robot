"""
数据库模块初始化
"""
from .neo4j_db import neo4j_conn
from .mongodb import mongodb_conn
from .redis_db import redis_conn

__all__ = ['neo4j_conn', 'mongodb_conn', 'redis_conn']


def init_databases():
    """初始化所有数据库连接"""
    neo4j_conn.connect()
    mongodb_conn.connect()
    redis_conn.connect()


def close_databases():
    """关闭所有数据库连接"""
    neo4j_conn.close()
    mongodb_conn.close()
    redis_conn.close()
