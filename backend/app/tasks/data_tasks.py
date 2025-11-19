"""
数据管理任务
"""
from celery import shared_task
from app.database.mongodb import mongodb_conn
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


@shared_task(name='app.tasks.data_tasks.cleanup_old_crawl_data')
def cleanup_old_crawl_data(days: int = 30):
    """
    清理旧的爬取数据
    
    Args:
        days: 保留最近多少天的数据
    """
    logger.info(f"🧹 开始清理 {days} 天前的爬取数据")
    
    try:
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # 删除旧文章
        result = mongodb_conn.get_collection('crawled_articles').delete_many({
            'crawled_at': {'$lt': cutoff_date}
        })
        
        deleted_count = result.deleted_count
        
        logger.info(f"✅ 清理完成! 删除了 {deleted_count} 条旧数据")
        
        # 记录清理任务
        mongodb_conn.get_collection('task_history').insert_one({
            'task': 'cleanup_old_crawl_data',
            'status': 'completed',
            'days': days,
            'deleted_count': deleted_count,
            'completed_at': datetime.now()
        })
        
        return {
            'deleted_count': deleted_count,
            'cutoff_date': cutoff_date
        }
        
    except Exception as e:
        logger.error(f"❌ 清理数据失败: {e}", exc_info=True)
        raise


@shared_task(name='app.tasks.data_tasks.get_crawl_statistics')
def get_crawl_statistics():
    """
    获取爬取统计信息
    """
    try:
        collection = mongodb_conn.get_collection('crawled_articles')
        
        # 总文章数
        total_articles = collection.count_documents({})
        
        # 按来源统计
        source_stats = list(collection.aggregate([
            {'$group': {
                '_id': '$source',
                'count': {'$sum': 1}
            }}
        ]))
        
        # 最近7天的文章数
        week_ago = datetime.now() - timedelta(days=7)
        recent_articles = collection.count_documents({
            'crawled_at': {'$gte': week_ago}
        })
        
        # 最近的任务执行记录
        recent_tasks = list(
            mongodb_conn.get_collection('task_history')
            .find()
            .sort('completed_at', -1)
            .limit(10)
        )
        
        # 转换ObjectId为字符串
        for task in recent_tasks:
            task['_id'] = str(task['_id'])
            if 'completed_at' in task:
                task['completed_at'] = task['completed_at'].isoformat()
        
        return {
            'total_articles': total_articles,
            'recent_articles': recent_articles,
            'source_stats': source_stats,
            'recent_tasks': recent_tasks
        }
        
    except Exception as e:
        logger.error(f"获取统计信息失败: {e}")
        return {}
