# API 密钥配置指南

## ⚠️ 安全警告

**永远不要在以下位置暴露您的 API 密钥:**
- 终端命令行
- Git 提交记录
- 公开的代码仓库
- 聊天记录或截图

## 配置步骤

### 1. 获取 OpenAI API 密钥

1. 访问 [OpenAI Platform](https://platform.openai.com/api-keys)
2. 登录您的账户
3. 点击 "Create new secret key"
4. 复制生成的密钥(格式: `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)
5. **立即保存到安全位置** - 密钥只显示一次

### 2. 配置环境变量

编辑 `backend\.env` 文件:

```bash
# 使用文本编辑器打开
notepad backend\.env
```

在文件中找到 `OPENAI_API_KEY` 行,填入您的密钥:

```env
# OpenAI配置
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
```

### 3. 验证配置

确保 `.env` 文件已被 `.gitignore` 排除:

```bash
# 检查 .gitignore
cat .gitignore | Select-String ".env"
```

应该看到:
```
.env
*.env
```

### 4. Docker 环境变量

如果使用 Docker Compose 运行,密钥会自动从 `.env` 文件加载:

```yaml
# docker-compose.yml 中的配置
backend:
  environment:
    - OPENAI_API_KEY=${OPENAI_API_KEY}
```

## 密钥安全最佳实践

### ✅ 正确做法

1. **使用环境变量**
   ```python
   import os
   api_key = os.getenv("OPENAI_API_KEY")
   ```

2. **使用 .env 文件** (已配置在 .gitignore)
   ```env
   OPENAI_API_KEY=sk-xxxxx
   ```

3. **为不同环境使用不同密钥**
   - 开发环境: `.env.development`
   - 生产环境: `.env.production`

### ❌ 错误做法

1. **硬编码在代码中**
   ```python
   # 危险!不要这样做
   api_key = "sk-08266faa1d184709878869666545ea9a"
   ```

2. **在终端直接输入**
   ```bash
   # 危险!不要这样做
   docker run -e OPENAI_API_KEY=sk-xxxxx
   ```

3. **提交到 Git 仓库**
   ```bash
   git add .env  # 危险!
   ```

## 如果密钥泄露怎么办?

### 立即行动清单

1. **撤销泄露的密钥**
   - 访问 [OpenAI API Keys](https://platform.openai.com/api-keys)
   - 找到泄露的密钥
   - 点击 "Revoke" 删除

2. **生成新密钥**
   - 创建新的 API 密钥
   - 更新 `backend\.env` 文件

3. **检查使用记录**
   - 查看 [Usage Dashboard](https://platform.openai.com/usage)
   - 确认是否有异常调用

4. **清理历史记录** (如果已提交到 Git)
   ```bash
   # 从 Git 历史中移除敏感文件
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch backend/.env" \
     --prune-empty --tag-name-filter cat -- --all
   ```

## 测试配置

启动后端服务后,访问:
```
http://localhost:8000/docs
```

尝试调用 `/api/v1/nlp/analyze-llm` 端点:
- 如果配置正确: 返回实体和关系提取结果
- 如果密钥无效: 返回 401 或 403 错误

## 成本管理

### 设置使用限额

1. 访问 [Billing Settings](https://platform.openai.com/account/billing/limits)
2. 设置每月预算上限
3. 启用邮件通知

### 监控使用情况

```python
# 在代码中记录 token 使用量
from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(...)
print(f"Tokens used: {response.usage.total_tokens}")
```

## 相关文档

- [OpenAI API 文档](https://platform.openai.com/docs/api-reference)
- [环境变量最佳实践](https://12factor.net/config)
- [项目开发文档](./开发文档.md)

---

**提示**: 如果您在配置过程中遇到问题,请参考 `docs/快速开始.md` 中的故障排除部分。
