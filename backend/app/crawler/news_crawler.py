"""
新闻爬虫 - 爬取产业新闻
"""
import asyncio
import logging
from typing import List, Dict
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from urllib.parse import quote
import json

logger = logging.getLogger(__name__)


class IndustryNewsCrawler:
    """产业新闻爬虫"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    
    def crawl_sina_finance(self, keyword: str, max_results: int = 10) -> List[Dict]:
        """
        爬取新浪财经新闻 - 使用新浪新闻API
        
        Args:
            keyword: 搜索关键词
            max_results: 最大结果数
            
        Returns:
            新闻列表
        """
        try:
            logger.info(f"开始爬取新浪财经: {keyword}")
            
            # 使用新浪新闻搜索接口
            url = f"https://interface.sina.cn/news/wap/search.d.json?keyword={quote(keyword)}&type=all&page=1&pagesize={max_results}"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code != 200:
                logger.warning(f"新浪接口返回状态码: {response.status_code}")
                return []
            
            data = response.json()
            results = []
            
            items = data.get('data', {}).get('feed', [])
            for item in items[:max_results]:
                try:
                    title = item.get('title', '').strip()
                    content = item.get('intro', '').strip() or item.get('summary', '').strip()
                    
                    if not title or len(content) < 30:
                        continue
                    
                    results.append({
                        'title': title,
                        'content': content,
                        'source': 'sina_finance',
                        'keyword': keyword,
                        'url': item.get('url', ''),
                        'published_at': item.get('ctime', ''),
                        'crawled_at': datetime.now()
                    })
                except Exception as e:
                    logger.warning(f"解析单条新闻失败: {e}")
                    continue
            
            logger.info(f"新浪财经爬取完成: {len(results)} 条")
            return results
            
        except Exception as e:
            logger.error(f"爬取新浪财经失败: {e}")
            return []
    
    def crawl_36kr(self, keyword: str, max_results: int = 10) -> List[Dict]:
        """
        爬取36氪科技新闻 - 使用百度新闻搜索(site:36kr.com)
        
        Args:
            keyword: 搜索关键词
            max_results: 最大结果数
            
        Returns:
            新闻列表
        """
        try:
            logger.info(f"开始爬取36氪: {keyword}")
            
            # 使用搜狗微信搜索的36kr内容
            url = f"https://www.toutiao.com/api/search/content/?keyword={quote(keyword + ' 36氪')}&offset=0&format=json&count={max_results}"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code != 200:
                logger.warning(f"搜索接口返回状态码: {response.status_code}")
                return []
            
            try:
                data = response.json()
            except:
                logger.warning("无法解析JSON响应")
                return []
            
            results = []
            items = data.get('data', [])
            
            for item in items[:max_results]:
                try:
                    title = item.get('title', '').strip()
                    content = item.get('abstract', '').strip()
                    
                    if not title or len(content) < 30:
                        continue
                    
                    results.append({
                        'title': title,
                        'content': content,
                        'source': '36kr',
                        'keyword': keyword,
                        'url': item.get('article_url', ''),
                        'published_at': item.get('datetime', ''),
                        'crawled_at': datetime.now()
                    })
                except Exception as e:
                    logger.warning(f"解析单条新闻失败: {e}")
                    continue
            
            logger.info(f"36氪爬取完成: {len(results)} 条")
            return results
            
        except Exception as e:
            logger.error(f"爬取36氪失败: {e}")
            return []
    
    def crawl_robot_news(self, keyword: str, max_results: int = 10) -> List[Dict]:
        """
        爬取机器人行业新闻 - 使用百度新闻搜索
        
        Args:
            keyword: 搜索关键词
            max_results: 最大结果数
            
        Returns:
            新闻列表
        """
        try:
            logger.info(f"开始爬取机器人网新闻: {keyword}")
            
            # 使用百度新闻搜索API
            url = f"https://www.baidu.com/s?tn=news&rtt=1&bsst=1&cl=2&wd={quote(keyword)}&pn=0"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            # 百度新闻结果通常在 div.result 中
            articles = soup.find_all('div', class_='result', limit=max_results)
            
            results = []
            for article in articles:
                try:
                    # 标题通常在 h3 > a 中
                    title_elem = article.find('h3')
                    if not title_elem:
                        continue
                    
                    title_link = title_elem.find('a')
                    if not title_link:
                        continue
                    
                    title = title_link.get_text(strip=True)
                    
                    # 内容摘要通常在 class 包含 'c-span' 或 'content' 的元素中
                    content_elem = article.find('span', class_=lambda x: x and ('abstract' in str(x) or 'content' in str(x)))
                    if not content_elem:
                        content_elem = article.find('div', class_=lambda x: x and 'content' in str(x))
                    
                    content = content_elem.get_text(strip=True) if content_elem else title
                    
                    if not title or len(content) < 20:
                        continue
                    
                    results.append({
                        'title': title,
                        'content': content,
                        'source': 'baidu_news',
                        'keyword': keyword,
                        'url': title_link.get('href', ''),
                        'crawled_at': datetime.now()
                    })
                except Exception as e:
                    logger.warning(f"解析单条新闻失败: {e}")
                    continue
            
            logger.info(f"百度新闻爬取完成: {len(results)} 条")
            return results
            
        except Exception as e:
            logger.error(f"爬取百度新闻失败: {e}")
            return []
    
    def crawl_all_sources(self, keyword: str) -> List[Dict]:
        """
        从所有数据源爬取新闻
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            所有新闻列表
        """
        all_news = []
        
        # 爬取新浪财经
        all_news.extend(self.crawl_sina_finance(keyword, max_results=5))
        
        # 爬取36氪
        all_news.extend(self.crawl_36kr(keyword, max_results=5))
        
        # 爬取机器人网
        all_news.extend(self.crawl_robot_news(keyword, max_results=5))
        
        logger.info(f"关键词 '{keyword}' 总共爬取: {len(all_news)} 条新闻")
        return all_news


# 全局爬虫实例
news_crawler = IndustryNewsCrawler()
