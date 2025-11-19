# DeepSeek API 配置说明

## 1. 概述

智链机器人使用 **DeepSeek API** 作为核心 LLM 服务,用于文本分析、实体提取和关系抽取。DeepSeek 是一个高性能、成本效益极高的大语言模型 API,完全兼容 OpenAI API 接口。

## 2. 获取 API 密钥

### 2.1 注册账号

1. 访问 DeepSeek 官网: https://platform.deepseek.com/
2. 点击 **"注册"** 按钮
3. 使用邮箱或手机号完成注册
4. 登录后进入控制台

### 2.2 创建 API 密钥

1. 在控制台点击 **"API Keys"**
2. 点击 **"Create API Key"** 按钮
3. 输入密钥名称(如: `zhilian-robot`)
4. 复制生成的密钥(格式: `sk-xxxxxxxxxxxxxx`)

**重要**: 密钥只显示一次,请妥善保存!

## 3. 配置项目

### 3.1 编辑环境变量

编辑 `backend/.env` 文件:

```env
# DeepSeek API 配置(兼容 OpenAI 接口格式)
OPENAI_API_KEY=sk-xxxxxxxxxxxxxx      # 替换为你的密钥
OPENAI_API_BASE=https://api.deepseek.com
OPENAI_MODEL=deepseek-chat
```

### 3.2 重启后端服务

```bash
# 在项目根目录执行
docker-compose restart backend

# 查看后端日志,确认配置加载成功
docker-compose logs backend
```

## 4. 支持的模型

### 4.1 deepseek-chat (默认推荐)

**特点:**
- 通用对话和文本生成
- 上下文长度: 64K tokens
- 中文支持优秀
- 适合本项目的所有 NLP 任务

**定价:**
- 输入: $0.14 / 1M tokens
- 输出: $0.28 / 1M tokens

**使用场景:**
- 实体提取(企业、产品、技术、人物、地点)
- 关系抽取(供应、合作、竞争关系)
- 文本摘要和分类

### 4.2 deepseek-coder

**特点:**
- 代码生成和理解
- 上下文长度: 64K tokens
- 支持多种编程语言

**定价:**
- 输入: $0.14 / 1M tokens
- 输出: $0.28 / 1M tokens

**切换方法:**
编辑 `backend/.env`:
```env
OPENAI_MODEL=deepseek-coder
```

## 5. 成本优势

### 5.1 价格对比

| 模型 | 输入价格 | 输出价格 | 性能 | 中文支持 |
|------|---------|---------|------|---------|
| OpenAI GPT-4 | $30/1M | $60/1M | 优秀 | 良好 |
| DeepSeek Chat | $0.14/1M | $0.28/1M | 优秀 | 优秀 |

**成本节省**: DeepSeek 约为 GPT-4 的 **1%** 💡

### 5.2 使用量估算

假设每天处理 100 篇文章:
- 每篇文章平均 1000 tokens 输入
- 每篇文章平均 500 tokens 输出

**每日成本:**
- 输入: 100 × 1000 × $0.14 / 1,000,000 = $0.014
- 输出: 100 × 500 × $0.28 / 1,000,000 = $0.014
- **总计**: $0.028/天 ≈ **$0.84/月**

使用 GPT-4 的话,同样工作量约为 **$84/月**。

## 6. API 使用示例

### 6.1 Python 代码示例

```python
from openai import OpenAI

# 初始化客户端
client = OpenAI(
    api_key="sk-xxxxxxxxxxxxxx",
    base_url="https://api.deepseek.com"
)

# 实体提取示例
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {
            "role": "system", 
            "content": "你是一个产业链分析助手,专门从文本中提取企业、产品、技术等实体。"
        },
        {
            "role": "user", 
            "content": "华为发布了新款Mate60手机,搭载麒麟9000S芯片。"
        }
    ],
    temperature=0.7,
    max_tokens=2000
)

print(response.choices[0].message.content)
```

### 6.2 API 参数说明

**常用参数:**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| model | string | - | 模型名称(deepseek-chat) |
| messages | array | - | 对话消息列表 |
| temperature | float | 1.0 | 随机性(0-2),越低越确定 |
| max_tokens | int | 4096 | 最大输出长度 |
| top_p | float | 1.0 | 核采样参数 |
| stream | bool | false | 是否流式输出 |

**推荐配置:**
- 实体提取: `temperature=0.3` (需要准确性)
- 文本生成: `temperature=0.7` (需要创造性)
- 关系抽取: `temperature=0.5` (平衡准确性和多样性)

## 7. 本项目的集成方式

### 7.1 服务封装

项目在 `backend/app/services/deepseek_service.py` 封装了 DeepSeek API:

```python
class DeepSeekService:
    def __init__(self):
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_API_BASE
        )
    
    async def extract_entities(self, text: str) -> dict:
        """从文本中提取实体"""
        # 调用 DeepSeek API
        response = await self.client.chat.completions.create(...)
        return parsed_result
    
    async def extract_relations(self, text: str, entities: list) -> list:
        """从文本中提取关系"""
        # 调用 DeepSeek API
        response = await self.client.chat.completions.create(...)
        return relations
```

### 7.2 API 端点

前端通过以下 API 使用 DeepSeek:

**POST /api/v1/analysis/analyze**
- 输入: 文本内容
- 输出: 提取的实体和关系

**POST /api/v1/analysis/save**
- 输入: 实体和关系数据
- 输出: 保存到 Neo4j 的结果

### 7.3 提示词工程

项目使用结构化提示词确保输出格式一致:

```python
ENTITY_EXTRACTION_PROMPT = """
你是一个产业链分析专家。请从以下文本中提取实体:

1. 企业(companies): 公司、组织名称
2. 产品(products): 产品、服务名称
3. 技术(technologies): 技术、算法、标准
4. 人物(persons): 关键人物、高管
5. 地点(locations): 地理位置

请以JSON格式返回,例如:
{
  "companies": ["华为", "小米"],
  "products": ["Mate60"],
  "technologies": ["麒麟9000S"],
  "persons": [],
  "locations": ["深圳"]
}

文本内容:
{text}
"""
```

## 8. 故障排查

### 问题1: API 密钥无效

**错误信息:**
```
AuthenticationError: Invalid API key
```

**解决方法:**
1. 检查 `backend/.env` 中的密钥格式
2. 确认密钥以 `sk-` 开头
3. 登录 DeepSeek 控制台验证密钥状态
4. 重新创建密钥并更新配置

### 问题2: 请求超时

**错误信息:**
```
TimeoutError: Request timeout
```

**解决方法:**
1. 检查网络连接
2. 增加超时时间(在 `deepseek_service.py` 中配置)
3. 减少 `max_tokens` 参数
4. 使用更短的输入文本

### 问题3: 输出格式错误

**错误信息:**
```
JSONDecodeError: Expecting value
```

**解决方法:**
1. 降低 `temperature` 参数(如 0.3)
2. 在提示词中强调 JSON 格式要求
3. 添加输出验证和错误重试逻辑

### 问题4: 速率限制

**错误信息:**
```
RateLimitError: Rate limit exceeded
```

**解决方法:**
1. 降低请求频率
2. 使用 Celery 队列控制并发
3. 升级 DeepSeek 套餐(如有)
4. 添加请求间隔(如 0.5秒)

## 9. 最佳实践

### 9.1 提示词优化

- 明确任务目标和输出格式
- 提供少量示例(few-shot learning)
- 使用结构化输出(JSON/YAML)
- 测试不同的 temperature 值

### 9.2 错误处理

```python
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
async def call_deepseek_api(text: str):
    """带重试机制的 API 调用"""
    try:
        response = await client.chat.completions.create(...)
        return response
    except Exception as e:
        logger.error(f"DeepSeek API 错误: {e}")
        raise
```

### 9.3 成本控制

- 设置 `max_tokens` 上限(如 2000)
- 对长文本进行分段处理
- 缓存常见查询结果
- 使用批量处理减少请求次数

## 10. 相关资源

- **DeepSeek 官网**: https://www.deepseek.com/
- **API 文档**: https://platform.deepseek.com/docs
- **定价说明**: https://platform.deepseek.com/pricing
- **社区支持**: https://github.com/deepseek-ai

---

**版本**: v1.0  
**更新日期**: 2025-01-19
