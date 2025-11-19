# 智链机器人 - 大模型驱动的产业链图谱自动构建平台

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/docker-compose-blue.svg)](https://docs.docker.com/compose/)

## 📖 项目简介

智链机器人是一个基于大语言模型(DeepSeek)的产业链图谱自动构建与分析平台,专注于机器人及相关产业链的智能数据采集、NLP分析和知识图谱可视化。系统采用前后端分离架构,支持自动化数据采集、实时图谱构建和交互式可视化展示。

## ✨ 核心功能

### 1. 📊 数据管理
- **RSS订阅管理**: 支持多源RSS订阅配置与自动更新
- **智能数据采集**: 
  - 多源新闻爬取 (新浪财经、36氪、机器人行业网站)
  - RSS订阅自动更新 (IEEE、OFweek、TechNode等)
  - 定时任务调度 (Celery Beat)
- **批量操作**: 文章批量处理、删除、导出
- **任务监控**: 实时查看采集任务历史和状态
- **数据统计**: 可视化数据统计卡片和图表

### 2. 🤖 文本分析
- **大模型驱动**: 集成 DeepSeek API 进行智能文本分析
- **实体识别(NER)**: 自动识别企业、产品、技术、人物、地点等实体
- **关系抽取(RE)**: 提取供应链、合作、竞争、投资等关系
- **结果可视化**: 实体和关系的直观展示
- **保存到图谱**: 一键将分析结果保存到知识图谱

### 3. 🕸️ 产业链图谱
- **交互式可视化**: 基于 ECharts 的力导向图布局
- **公司关系查询**: 支持多层级关系查询 (1-4层)
- **全屏显示**: 支持全屏模式,提升查看体验
- **智能优化**: 
  - 自动去重重复关系边
  - 关系标签开关控制
  - 节点拖拽和缩放
- **图谱管理**: 支持图谱数据的保存、查询、清空

### 4. ⚙️ 自动化调度
- **定时任务**:
  - 每日 02:00 - 自动爬取全量新闻
  - 每 6 小时 - RSS订阅增量更新
  - 每周一 03:00 - 清理30天前的旧数据
- **任务监控**: Flower 可视化监控面板
- **异步处理**: Celery 分布式任务队列

## 🛠️ 技术栈

### 前端技术
- **框架**: React 18.x
- **UI组件**: Ant Design 5.x
- **图表**: ECharts 5.x
- **HTTP客户端**: Axios
- **路由**: React Router 6.x
- **构建工具**: Vite 5.x

### 后端技术
- **Web框架**: FastAPI 0.100+
- **NLP处理**: 
  - OpenAI SDK (DeepSeek API)
  - 传统NLP模块 (正则、规则匹配)
- **爬虫框架**: 
  - Scrapy 2.11+
  - Feedparser 6.0.10 (RSS解析)
- **任务队列**: Celery 5.3.4 + Redis
- **任务监控**: Flower 2.0+
- **Python版本**: 3.8+

### 数据存储
- **图数据库**: Neo4j 5.20 (知识图谱存储)
- **文档数据库**: MongoDB 8.0 (文章和RSS数据)
- **关系数据库**: MySQL 8.0 (任务和配置)
- **缓存/队列**: Redis 7-alpine (Celery broker)

### 容器化部署
- **容器编排**: Docker Compose
- **Web服务器**: Nginx (前端静态文件)
- **进程管理**: Celery Worker + Beat
- **监控服务**: Flower

## 📁 项目结构

```plaintext
zhilian-robot/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── api/            # FastAPI路由接口
│   │   │   ├── data_routes.py      # 数据管理接口
│   │   │   ├── nlp_routes.py       # 文本分析接口
│   │   │   └── graph_routes.py     # 图谱查询接口
│   │   ├── models/         # Pydantic数据模型
│   │   ├── services/       # 业务逻辑层
│   │   │   └── graph_service.py    # 图谱服务
│   │   ├── nlp/           # NLP处理模块
│   │   │   ├── llm.py              # DeepSeek大模型集成
│   │   │   ├── ner.py              # 实体识别
│   │   │   └── re.py               # 关系抽取
│   │   ├── crawler/       # 数据采集模块
│   │   │   ├── rss_parser.py       # RSS解析器
│   │   │   ├── news_crawler.py     # 新闻爬虫
│   │   │   └── pipelines.py        # 数据处理管道
│   │   ├── tasks/         # Celery异步任务
│   │   │   ├── celery_app.py       # Celery配置
│   │   │   ├── crawl_tasks.py      # 爬虫任务
│   │   │   └── data_tasks.py       # 数据处理任务
│   │   ├── database/      # 数据库连接
│   │   │   ├── neo4j.py            # Neo4j连接
│   │   │   ├── mongodb.py          # MongoDB连接
│   │   │   └── mysql.py            # MySQL连接
│   │   └── utils/         # 工具函数
│   ├── config/            # 配置文件
│   │   └── settings.py             # 环境配置
│   ├── main.py            # FastAPI应用入口
│   ├── requirements.txt   # Python依赖
│   └── .env              # 环境变量配置
├── frontend/              # 前端应用
│   ├── src/
│   │   ├── pages/        # 页面组件
│   │   │   ├── HomePage.jsx        # 首页
│   │   │   ├── DataManagePage.jsx  # 数据管理页
│   │   │   ├── AnalysisPage.jsx    # 文本分析页
│   │   │   └── GraphPage.jsx       # 图谱查询页
│   │   ├── components/   # 通用组件
│   │   │   ├── Layout.jsx          # 布局组件
│   │   │   └── GraphVisualization.jsx  # 图谱可视化
│   │   ├── services/     # API服务
│   │   │   └── api.js              # API封装
│   │   ├── App.jsx       # 应用根组件
│   │   └── main.jsx      # 应用入口
│   ├── package.json      # Node依赖
│   └── vite.config.js    # Vite配置
├── docs/                 # 项目文档
│   ├── 快速开始.md
│   ├── 开发文档.md
│   ├── 用户操作手册.md
│   └── 自动化数据采集指南.md
├── scripts/             # 部署脚本
│   ├── init.ps1         # 初始化脚本
│   └── start.ps1        # 启动脚本
├── docker-compose.yml   # Docker编排配置
└── README.md           # 项目说明
```

## 🚀 快速开始

### 环境要求

- **Docker Desktop** (推荐,支持 Windows/Mac/Linux)
- Docker Compose 2.0+
- 或 Python 3.8+ 和 Node.js 18+ (本地开发)

### 方式一: Docker 一键部署 (推荐) ⭐

```bash
# 1. 克隆项目
git clone https://github.com/Aspirin-s/zhilian-robot.git
cd zhilian-robot

# 2. 复制环境配置文件（首次部署必须）
cp backend/.env.example backend/.env  # Linux/Mac
# 或 Copy-Item backend\.env.example backend\.env  # Windows PowerShell

# 3. 编辑配置文件，设置 DeepSeek API 密钥
# 编辑 backend/.env 文件:
# OPENAI_API_KEY=sk-xxxxxxxxxxxxxx  # 替换为你的密钥

# 4. 启动所有服务
docker-compose up -d

# 5. 等待启动完成（约1-2分钟），查看容器状态
docker-compose ps
# 应看到9个容器全部显示 "Up" 状态

# 6. 验证后端服务
docker-compose logs --tail=20 backend
# 看到 "Application startup complete" 表示成功
```

**🎯 获取 DeepSeek API 密钥:**
1. 访问 https://platform.deepseek.com/
2. 注册/登录账号
3. 进入 "API Keys" 页面创建密钥
4. 复制密钥到 `backend/.env` 文件

### 方式二: PowerShell 脚本启动 (Windows)

```powershell
# 1. 初始化环境
.\scripts\init.ps1

# 2. 启动应用
.\scripts\start.ps1
# 选择选项3"同时启动前后端"
```

### 访问地址

启动成功后,访问以下地址:

| 服务 | 地址 | 用户名 | 密码 | 说明 |
|------|------|--------|------|------|
| **前端界面** | http://localhost | - | - | React前端应用 |
| **后端API** | http://localhost:8000 | - | - | FastAPI服务 |
| **API文档** | http://localhost:8000/docs | - | - | Swagger交互文档 |
| **任务监控** | http://localhost:5555 | - | - | Celery Flower |
| **Neo4j界面** | http://localhost:7474 | neo4j | password123 | 图数据库管理 |

### 快速验证

打开浏览器访问 http://localhost ，点击顶部导航栏：
1. **数据管理** → 点击"立即更新"采集RSS数据
2. **文本分析** → 点击"加载示例文本"→"分析文本"→"保存到图谱"
3. **图谱查询** → 输入"华为"→ 点击"查询"查看产业链图谱

### 详细文档

📖 更多详细信息请查看:
- [快速开始指南](./docs/快速开始.md) - 完整部署教程
- [用户操作手册](./docs/用户操作手册.md) - 功能使用说明
- [开发文档](./docs/开发文档.md) - 二次开发指南
- [DeepSeek配置](./docs/DeepSeek配置说明.md) - API配置详解
- **MySQL**: 用户名 `root`, 密码 `password123`

## 📖 使用指南

### 1. 数据管理

访问 http://localhost → 点击"数据管理"

- **RSS订阅管理**: 查看已配置的4个RSS源
- **立即更新**: 手动触发RSS数据采集
- **文章列表**: 查看已采集的文章,支持分页、搜索
- **批量操作**: 
  - 选中多篇文章进行批量处理
  - 批量删除不需要的文章
- **任务历史**: 查看采集任务的执行记录

### 2. 文本分析

访问 http://localhost → 点击"文本分析"

1. 输入或加载示例文本
2. 点击"分析文本"按钮,使用 DeepSeek 大模型分析
3. 查看提取的实体(企业、产品、技术、人物、地点)
4. 查看提取的关系(供应商、合作关系、投资等)
5. 点击"保存到图谱"将结果保存到 Neo4j

### 3. 产业链图谱

访问 http://localhost → 点击"图谱查询"

1. 输入公司名称(如"华为"、"特斯拉"、"小米")
2. 选择查询深度(1-4层)
3. 点击"查询"按钮
4. 查看交互式图谱:
   - 🖱️ 鼠标拖拽节点调整位置
   - 🔍 鼠标滚轮缩放图谱
   - 📱 点击全屏按钮进入全屏模式
   - 🏷️ 开关"显示关系标签"控制连线标签显示

### 4. 自动化任务

系统已配置自动化定时任务:

- **每日 02:00** - 自动爬取机器人行业新闻
- **每 6 小时** - 自动更新 RSS 订阅
- **每周一 03:00** - 清理 30 天前的旧数据

访问 http://localhost:5555 查看 Celery 任务执行状态

## 🔧 配置说明

### DeepSeek API 配置

编辑 `backend/.env` 文件:

```env
# DeepSeek API配置
OPENAI_API_KEY=your-deepseek-api-key
OPENAI_API_BASE=https://api.deepseek.com
OPENAI_MODEL=deepseek-chat
```

获取 API 密钥: https://platform.deepseek.com/api_keys

### 数据库配置

默认配置已在 `docker-compose.yml` 中设置,无需修改。如需自定义:

```env
# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password123

# MongoDB
MONGODB_URI=mongodb://admin:password123@localhost:27017/

# MySQL
MYSQL_HOST=localhost
MYSQL_PORT=3307
MYSQL_USER=root
MYSQL_PASSWORD=password123
MYSQL_DATABASE=zhilian_robot

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
```

## 📊 API 接口文档

### 数据管理 API

```bash
# 获取统计信息
GET /api/v1/data/statistics

# 手动触发爬取
POST /api/v1/data/crawl?keyword=工业机器人

# 更新RSS订阅
POST /api/v1/data/rss/update

# 获取文章列表
GET /api/v1/data/articles?skip=0&limit=10

# 获取任务历史
GET /api/v1/data/tasks/history?limit=20

# 批量处理文章
POST /api/v1/data/process/batch
Content-Type: application/json
{
  "article_ids": ["id1", "id2"]
}

# 批量删除文章
POST /api/v1/data/articles/delete/batch
Content-Type: application/json
{
  "article_ids": ["id1", "id2"]
}
```

### 文本分析 API

```bash
# DeepSeek大模型分析
POST /api/v1/nlp/analyze-llm
Content-Type: application/json
{
  "text": "华为与台积电合作..."
}

# 传统NLP分析
POST /api/v1/nlp/analyze
Content-Type: application/json
{
  "text": "小米发布新款机器人...",
  "extract_entities": true,
  "extract_relations": true
}
```

### 图谱管理 API

```bash
# 查询公司关系图谱
POST /api/v1/graph/query
Content-Type: application/json
{
  "company_name": "华为",
  "max_depth": 2
}

# 保存分析结果到图谱
POST /api/v1/graph/save
Content-Type: application/json
{
  "entities": {...},
  "relations": [...]
}

# 获取图谱统计
GET /api/v1/graph/statistics

# 清空图谱数据
DELETE /api/v1/graph/clear
```

完整 API 文档访问: http://localhost:8000/docs

## 🐳 Docker 容器说明

系统包含 9 个 Docker 容器:

| 容器名 | 镜像 | 端口 | 说明 |
|--------|------|------|------|
| zhilian-frontend | nginx:alpine | 80 | React前端 |
| zhilian-backend | zhilian-robot-backend | 8000 | FastAPI后端 |
| zhilian-celery-worker | zhilian-robot-celery-worker | - | 异步任务处理 |
| zhilian-celery-beat | zhilian-robot-celery-beat | - | 定时任务调度 |
| zhilian-flower | zhilian-robot-flower | 5555 | 任务监控 |
| zhilian-neo4j | neo4j:5.20 | 7474, 7687 | 图数据库 |
| zhilian-mongodb | mongo:8 | 27017 | 文档数据库 |
| zhilian-mysql | mysql:8 | 3307 | 关系数据库 |
| zhilian-redis | redis:7-alpine | 6379 | 缓存/队列 |

### 常用命令

```bash
# 查看所有容器状态
docker-compose ps

# 查看后端日志
docker-compose logs -f backend

# 查看 Celery Worker 日志
docker-compose logs -f celery-worker

# 重启单个服务
docker-compose restart frontend

# 停止所有服务
docker-compose down

# 停止并删除数据卷(慎用!)
docker-compose down -v

# 重新构建镜像
docker-compose build backend
```

## 💾 数据存储

### 数据卷占用

- **Neo4j 数据**: ~541 MB (图谱节点和关系)
- **MongoDB 数据**: ~222 MB (文章和RSS数据)
- **MySQL 数据**: ~218 MB (任务和配置)
- **Redis 数据**: ~284 KB (缓存和队列)
- **总计**: 约 1 GB

### 数据清理

```bash
# 清理30天前的旧文章(API)
DELETE /api/v1/data/cleanup?days=30

# 或使用命令行
docker exec zhilian-backend python -c "
from app.tasks.data_tasks import cleanup_old_data
cleanup_old_data(30)
"
```

## 🔍 故障排查

### 问题: 前端页面无法访问

```bash
# 检查容器状态
docker-compose ps

# 重启前端容器
docker-compose restart frontend

# 查看前端日志
docker-compose logs frontend
```

### 问题: 后端 API 报错

```bash
# 查看后端日志
docker-compose logs -f backend

# 检查环境变量配置
docker exec zhilian-backend env | grep OPENAI

# 重启后端
docker-compose restart backend
```

### 问题: Celery 任务不执行

```bash
# 检查 Celery Worker 状态
docker-compose logs -f celery-worker

# 检查 Redis 连接
docker exec zhilian-backend redis-cli -h redis ping

# 重启 Celery 服务
docker-compose restart celery-worker celery-beat
```

### 问题: 数据库连接失败

```bash
# Neo4j 连接测试
docker exec zhilian-neo4j cypher-shell -u neo4j -p password123 "RETURN 1"

# MongoDB 连接测试
docker exec zhilian-mongodb mongosh --eval "db.adminCommand('ping')" -u admin -p password123

# MySQL 连接测试
docker exec zhilian-mysql mysql -uroot -ppassword123 -e "SELECT 1"
```

## 🛣️ 开发路线图

### ✅ 已完成

- [x] 基础架构搭建 (FastAPI + React)
- [x] Neo4j 图数据库集成
- [x] MongoDB/MySQL 数据存储
- [x] RSS订阅自动采集
- [x] Celery 异步任务系统
- [x] DeepSeek 大模型集成
- [x] 实体识别和关系抽取
- [x] ECharts 图谱可视化
- [x] 批量数据处理
- [x] 图谱全屏显示
- [x] 关系边去重优化
- [x] 边标签开关控制

### 🚧 进行中

- [ ] 爬虫性能优化
- [ ] 更多数据源接入
- [ ] 图谱算法优化

### 📋 计划中

- [ ] 用户认证系统
- [ ] 数据导出功能 (Excel/CSV)
- [ ] 图谱历史版本管理
- [ ] 移动端适配
- [ ] 英文版界面

## 📚 文档导航

- [快速开始指南](./docs/快速开始.md) - 5分钟上手教程
- [开发文档](./docs/开发文档.md) - 详细开发指南
- [用户操作手册](./docs/用户操作手册.md) - 功能使用说明
- [自动化数据采集指南](./docs/自动化数据采集指南.md) - 爬虫系统使用手册
- [DeepSeek配置说明](./docs/DeepSeek配置说明.md) - API配置教程

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议!

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 👥 开发团队

浙江大学 - 智链机器人项目组

## 📄 许可证

MIT License

Copyright (c) 2024 智链机器人项目组

## 🙏 致谢

- [DeepSeek](https://www.deepseek.com/) - 大语言模型支持
- [FastAPI](https://fastapi.tiangolo.com/) - 现代化Web框架
- [React](https://react.dev/) - 前端框架
- [ECharts](https://echarts.apache.org/) - 数据可视化
- [Neo4j](https://neo4j.com/) - 图数据库
- [Celery](https://docs.celeryq.dev/) - 分布式任务队列

---

如有问题或建议,请提交 [Issue](https://github.com/Aspirin-s/zhilian-robot/issues) 或联系项目组。
