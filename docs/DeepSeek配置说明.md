# DeepSeek API 配置说明

## 📖 概述

本项目已配置为使用 DeepSeek API,这是一个高性能、成本效益高的大语言模型 API 服务,完全兼容 OpenAI API 接口。

## 🔑 API 密钥配置

### 当前配置

项目已配置您的 DeepSeek API 密钥:
- **API Key**: `sk-08266faa1d184709878869666545ea9a`
- **Base URL**: `https://api.deepseek.com`
- **模型**: `deepseek-chat`

### 配置文件位置

环境变量配置在 `backend\.env`:

```env
# DeepSeek API (Compatible with OpenAI interface)
OPENAI_API_KEY=sk-08266faa1d184709878869666545ea9a
OPENAI_API_BASE=https://api.deepseek.com
OPENAI_MODEL=deepseek-chat
```

## 🎯 支持的功能

### 1. 实体提取
使用 DeepSeek 从文本中提取产业链相关实体:
- 企业名称
- 产品名称
- 技术名称
- 关键人物
- 地点信息

### 2. 关系抽取
识别实体之间的关系:
- 供应关系
- 合作关系
- 竞争关系
- 上下游关系

### 3. 知识图谱构建
基于提取的实体和关系构建产业链知识图谱

## 💰 成本优势

DeepSeek 相比 OpenAI 的优势:

| 项目 | OpenAI GPT-4 | DeepSeek Chat |
|------|--------------|---------------|
| 输入价格 | $30/1M tokens | $0.14/1M tokens |
| 输出价格 | $60/1M tokens | $0.28/1M tokens |
| 性能 | 优秀 | 优秀 |
| 中文支持 | 良好 | 优秀 |

**成本节省**: 约为 GPT-4 的 **1%** 💡

## 🚀 可用模型

### 推荐模型

1. **deepseek-chat** (默认)
   - 用途: 对话、文本生成、信息提取
   - 上下文: 64K tokens
   - 推荐场景: 本项目的所有 NLP 任务

2. **deepseek-coder**
   - 用途: 代码生成、代码理解
   - 上下文: 64K tokens
   - 推荐场景: 如需处理代码相关内容

### 切换模型

修改 `backend\.env`:
```env
OPENAI_MODEL=deepseek-coder  # 切换到代码模型
```

## 📝 API 使用示例

### Python 代码示例

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-08266faa1d184709878869666545ea9a",
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个产业链分析助手"},
        {"role": "user", "content": "分析机器人产业链"}
    ]
)

print(response.choices[0].message.content)
```

### 项目中的使用

在 `backend/app/nlp/llm.py` 中已配置:

```python
class LLMProcessor:
    def __init__(self):
        # 自动使用 DeepSeek API
        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_API_BASE
        )
        self.model = settings.OPENAI_MODEL  # deepseek-chat
```

## 🔧 测试 API

### 1. 使用 curl 测试

```bash
curl https://api.deepseek.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-08266faa1d184709878869666545ea9a" \
  -d '{
    "model": "deepseek-chat",
    "messages": [
      {"role": "user", "content": "你好"}
    ]
  }'
```

### 2. 使用 Python 测试

创建测试文件 `test_deepseek.py`:

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-08266faa1d184709878869666545ea9a",
    base_url="https://api.deepseek.com"
)

try:
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": "你好,请介绍一下你自己"}],
    )
    print("✅ API 连接成功!")
    print(f"回复: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ API 连接失败: {e}")
```

运行测试:
```bash
cd backend
python test_deepseek.py
```

## 📊 监控使用情况

### 查看用量

访问 DeepSeek 控制台:
- 网址: https://platform.deepseek.com
- 登录后查看 Usage Dashboard

### 设置用量提醒

在 DeepSeek 平台可以设置:
- 每日用量限制
- 余额预警
- 邮件通知

## ⚠️ 注意事项

### 1. API 限流
- 免费用户: 60 请求/分钟
- 付费用户: 更高限制

### 2. 上下文长度
- 最大: 64K tokens
- 建议: 保持在 32K 以内以获得最佳性能

### 3. 超时设置
```python
client = OpenAI(
    api_key="sk-08266faa1d184709878869666545ea9a",
    base_url="https://api.deepseek.com",
    timeout=30.0  # 30秒超时
)
```

## 🔄 如需切换回 OpenAI

如果将来想切换回 OpenAI,只需修改 `backend\.env`:

```env
# OpenAI API
OPENAI_API_KEY=sk-your-openai-key
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL=gpt-4
```

代码无需修改,完全兼容!

## 📚 相关资源

- [DeepSeek 官网](https://www.deepseek.com)
- [DeepSeek 平台](https://platform.deepseek.com)
- [API 文档](https://platform.deepseek.com/api-docs)
- [定价信息](https://platform.deepseek.com/pricing)

## 🆘 常见问题

### Q: API 调用失败怎么办?
A: 检查以下内容:
1. API Key 是否正确
2. 网络连接是否正常
3. 是否超过使用限额
4. Base URL 是否正确设置

### Q: 如何查看 API 调用日志?
A: 查看项目日志文件 `backend/logs/app.log`

### Q: 支持流式输出吗?
A: 支持,设置 `stream=True`:
```python
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[...],
    stream=True
)
```

---

**配置完成!** 现在您可以使用 DeepSeek API 进行产业链知识图谱构建了 🎉
