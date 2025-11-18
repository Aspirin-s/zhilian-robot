# Git初始化脚本

Write-Host "初始化Git仓库..." -ForegroundColor Cyan

# 初始化Git仓库
git init

# 添加所有文件
git add .

# 首次提交
git commit -m "feat: 初始化智链机器人项目

- ✅ 完整的前后端框架搭建
- ✅ Neo4j/MongoDB/Redis/MySQL数据库集成
- ✅ NLP模块(NER/RE/LLM)
- ✅ Scrapy爬虫框架
- ✅ React前端与ECharts可视化
- ✅ RESTful API接口
- ✅ Docker容器化配置
- ✅ 完整项目文档

项目技术栈:
- 后端: Python 3.8+ FastAPI
- 前端: React 18 + Vite + ECharts
- 数据库: Neo4j + MongoDB + Redis + MySQL
- AI: Hugging Face Transformers + OpenAI
- 爬虫: Scrapy 2.11+
"

Write-Host "✓ Git仓库初始化完成" -ForegroundColor Green
Write-Host "`n后续步骤:" -ForegroundColor Yellow
Write-Host "1. 创建GitHub/GitLab远程仓库"
Write-Host "2. 添加远程仓库: git remote add origin <url>"
Write-Host "3. 推送代码: git push -u origin main"
