# 智链机器人 - 大模型驱动的产业链图谱自动构建平台

## 项目简介

智链机器人是一个基于大语言模型的产业链图谱自动构建平台,专注于机器人产业链的智能分析与可视化。

## 核心功能

- **智能实体识别(NER)**: 自动识别产业链中的企业、产品、技术等关键实体
- **关系抽取(RE)**: 提取上下游关系、合作关系、竞争关系
- **知识图谱构建**: 基于Neo4j的图数据库存储与查询
- **动态可视化**: 基于ECharts的交互式产业链图谱展示
- **多源数据采集**: 支持新闻、报告、专利等多源文本数据爬取

## 技术栈

### 前端
- React.js 18.x
- ECharts 5.x
- Axios

### 后端
- Python 3.8+
- FastAPI
- Hugging Face Transformers 4.45+
- Scrapy 2.11+

### 数据库
- Neo4j 5.20+ (图数据库)
- MongoDB 8.x (文档存储)
- Redis 7.x+ (缓存)
- MySQL 8.x (关系型数据库)

## 项目结构

```
zhilian-robot/
├── backend/           # 后端服务
│   ├── app/
│   │   ├── api/      # API接口
│   │   ├── models/   # 数据模型
│   │   ├── services/ # 业务逻辑
│   │   ├── nlp/      # NLP处理模块
│   │   ├── crawler/  # 爬虫模块
│   │   ├── database/ # 数据库连接
│   │   └── utils/    # 工具函数
│   ├── config/       # 配置文件
│   └── tests/        # 测试代码
├── frontend/         # 前端应用
├── docs/            # 项目文档
└── scripts/         # 部署脚本
```

## 快速开始

### 🚀 一键启动(推荐)

```powershell
# 初始化环境
.\scripts\init.ps1

# 启动应用
.\scripts\start.ps1
```

选择选项3"同时启动前后端",即可快速开始使用!

详细步骤请查看 [快速开始指南](./docs/快速开始.md)

### 🐳 Docker启动

```bash
docker-compose up -d
```

访问:
- 前端: <http://localhost>
- 后端: <http://localhost:8000>
- API文档: <http://localhost:8000/docs>

### 📖 文档导航

- [快速开始指南](./docs/快速开始.md) - 5分钟上手教程
- [开发文档](./docs/开发文档.md) - 详细开发指南
- [用户操作手册](./docs/用户操作手册.md) - 功能使用说明
- [项目计划](./docs/项目计划.md) - 开发路线图

## 开发团队

浙江大学 - 智链机器人项目组

## 许可证

MIT License
