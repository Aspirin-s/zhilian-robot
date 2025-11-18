# Scrapy settings for zhilian_crawler project

BOT_NAME = 'zhilian_crawler'

SPIDER_MODULES = ['app.crawler.spiders']
NEWSPIDER_MODULE = 'app.crawler.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests
CONCURRENT_REQUESTS = 5

# Configure a delay for requests
DOWNLOAD_DELAY = 2

# Disable cookies
COOKIES_ENABLED = False

# Override the default request headers
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    'app.crawler.middlewares.RandomUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}

# Configure item pipelines
ITEM_PIPELINES = {
    'app.crawler.pipelines.TextCleaningPipeline': 300,
    'app.crawler.pipelines.MongoDBPipeline': 400,
}

# Enable and configure HTTP caching
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'

# Log level
LOG_LEVEL = 'INFO'
