"""
Scrapy Item定义
"""
import scrapy


class NewsItem(scrapy.Item):
    """新闻条目"""
    title = scrapy.Field()          # 标题
    content = scrapy.Field()        # 内容
    url = scrapy.Field()            # 来源URL
    publish_date = scrapy.Field()   # 发布日期
    source = scrapy.Field()         # 来源网站
    author = scrapy.Field()         # 作者
    tags = scrapy.Field()           # 标签
    crawl_time = scrapy.Field()     # 爬取时间


class ReportItem(scrapy.Item):
    """研究报告条目"""
    title = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    report_type = scrapy.Field()    # 报告类型
    publish_date = scrapy.Field()
    organization = scrapy.Field()   # 发布机构
    industry = scrapy.Field()       # 行业
    crawl_time = scrapy.Field()


class CompanyItem(scrapy.Item):
    """企业信息条目"""
    name = scrapy.Field()           # 企业名称
    description = scrapy.Field()    # 企业描述
    industry = scrapy.Field()       # 所属行业
    products = scrapy.Field()       # 主要产品
    url = scrapy.Field()            # 来源URL
    crawl_time = scrapy.Field()
