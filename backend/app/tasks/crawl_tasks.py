"""
爬虫定时任务
"""
from celery import shared_task
from app.crawler.news_crawler import news_crawler
from app.crawler.rss_parser import rss_parser
from app.nlp.llm import llm_processor
from app.services.graph_service import graph_service
from app.database.mongodb import mongodb_conn
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


@shared_task(name='app.tasks.crawl_tasks.crawl_all_news', bind=True)
def crawl_all_news(self):
    """
    爬取所有关键词的新闻并构建图谱
    """
    logger.info("⏰ 定时任务启动: 爬取行业新闻")
    
    # 预定义关键词
    keywords = [
        "工业机器人",
        "华为",
        "ABB机器人",
        "库卡机器人",
        "发那科",
        "安川电机",
        "机器人产业链",
        "智能制造"
    ]
    
    total_processed = 0
    total_entities = 0
    total_relations = 0
    
    try:
        for keyword in keywords:
            logger.info(f"📰 正在处理关键词: {keyword}")
            
            # 1. 爬取新闻
            articles = news_crawler.crawl_all_sources(keyword)
            
            for article in articles:
                try:
                    # 2. 使用DeepSeek提取实体和关系
                    result = llm_processor.analyze_industry_chain(article['content'])
                    entities = result.get('entities', {})
                    relations = result.get('relations', [])
                    
                    # 3. 保存到Neo4j图数据库
                    save_result = graph_service.save_analyzed_data(entities, relations)
                    
                    if save_result.get('success'):
                        total_entities += save_result.get('entities_count', 0)
                        total_relations += save_result.get('relations_count', 0)
                    
                    # 4. 保存原始数据到MongoDB
                    article_doc = {
                        'title': article['title'],
                        'content': article['content'],
                        'source': article['source'],
                        'keyword': article.get('keyword', keyword),
                        'url': article.get('url', ''),
                        'entities': entities,
                        'relations': relations,
                        'crawled_at': article.get('crawled_at', datetime.now()),
                        'processed_at': datetime.now()
                    }
                    
                    mongodb_conn.get_collection('crawled_articles').insert_one(article_doc)
                    total_processed += 1
                    
                    logger.info(f"✅ 处理成功: {article['title'][:50]}...")
                    
                except Exception as e:
                    logger.error(f"❌ 处理文章失败: {e}")
                    continue
        
        summary = {
            'task': 'crawl_all_news',
            'status': 'completed',
            'keywords': keywords,
            'articles_processed': total_processed,
            'entities_extracted': total_entities,
            'relations_extracted': total_relations,
            'completed_at': datetime.now()
        }
        
        # 保存任务执行记录
        mongodb_conn.get_collection('task_history').insert_one(summary)
        
        logger.info(f"🎉 任务完成! 处理 {total_processed} 篇文章, "
                   f"提取 {total_entities} 个实体, {total_relations} 个关系")
        
        return summary
        
    except Exception as e:
        logger.error(f"💥 任务执行失败: {e}", exc_info=True)
        raise


@shared_task(name='app.tasks.crawl_tasks.fetch_rss_updates', bind=True)
def fetch_rss_updates(self):
    """
    获取RSS订阅更新
    """
    logger.info("⏰ 定时任务启动: 检查RSS更新")
    
    total_processed = 0
    total_entities = 0
    total_relations = 0
    
    try:
        # 1. 解析所有RSS源
        articles = rss_parser.parse_all_feeds()
        
        for article in articles:
            try:
                # 检查是否已处理过(通过URL去重)
                existing = mongodb_conn.get_collection('crawled_articles').find_one({
                    'url': article['url']
                })
                
                if existing:
                    logger.info(f"⏭️ 跳过已处理文章: {article['title'][:50]}")
                    continue
                
                # 2. 提取实体和关系
                result = llm_processor.analyze_industry_chain(article['content'])
                entities = result.get('entities', {})
                relations = result.get('relations', [])
                
                # 3. 保存到图谱
                save_result = graph_service.save_analyzed_data(entities, relations)
                
                if save_result.get('success'):
                    total_entities += save_result.get('entities_count', 0)
                    total_relations += save_result.get('relations_count', 0)
                
                # 4. 保存到MongoDB
                article_doc = {
                    'title': article['title'],
                    'content': article['content'],
                    'source': article['source'],
                    'url': article.get('url', ''),
                    'entities': entities,
                    'relations': relations,
                    'published_at': article.get('published_at'),
                    'crawled_at': article.get('crawled_at', datetime.now()),
                    'processed_at': datetime.now()
                }
                
                mongodb_conn.get_collection('crawled_articles').insert_one(article_doc)
                total_processed += 1
                
                logger.info(f"✅ RSS文章处理成功: {article['title'][:50]}...")
                
            except Exception as e:
                logger.error(f"❌ 处理RSS文章失败: {e}")
                continue
        
        summary = {
            'task': 'fetch_rss_updates',
            'status': 'completed',
            'articles_processed': total_processed,
            'entities_extracted': total_entities,
            'relations_extracted': total_relations,
            'completed_at': datetime.now()
        }
        
        mongodb_conn.get_collection('task_history').insert_one(summary)
        
        logger.info(f"🎉 RSS更新完成! 处理 {total_processed} 篇新文章")
        
        # 返回不包含ObjectId的结果(避免JSON序列化错误)
        return {
            'task': 'fetch_rss_updates',
            'status': 'completed',
            'articles_processed': total_processed,
            'entities_extracted': total_entities,
            'relations_extracted': total_relations
        }
        
    except Exception as e:
        logger.error(f"💥 RSS更新失败: {e}", exc_info=True)
        raise


@shared_task(name='app.tasks.crawl_tasks.crawl_single_keyword')
def crawl_single_keyword(keyword: str):
    """
    爬取单个关键词的新闻(手动触发)
    
    Args:
        keyword: 搜索关键词
    """
    logger.info(f"🔍 手动爬取: {keyword}")
    
    try:
        articles = news_crawler.crawl_all_sources(keyword)
        processed_count = 0
        
        for article in articles:
            try:
                result = llm_processor.analyze_industry_chain(article['content'])
                entities = result.get('entities', {})
                relations = result.get('relations', [])
                
                graph_service.save_analyzed_data(entities, relations)
                
                article_doc = {
                    'title': article['title'],
                    'content': article['content'],
                    'source': article['source'],
                    'keyword': keyword,
                    'url': article.get('url', ''),
                    'entities': entities,
                    'relations': relations,
                    'crawled_at': article.get('crawled_at', datetime.now()),
                    'processed_at': datetime.now()
                }
                
                mongodb_conn.get_collection('crawled_articles').insert_one(article_doc)
                processed_count += 1
                
            except Exception as e:
                logger.error(f"处理文章失败: {e}")
                continue
        
        logger.info(f"✅ 关键词 '{keyword}' 处理完成: {processed_count} 篇文章")
        
        # 返回可JSON序列化的结果
        return {
            'keyword': keyword,
            'articles_processed': processed_count,
            'status': 'completed'
        }
        
    except Exception as e:
        logger.error(f"爬取失败: {e}", exc_info=True)
        raise
