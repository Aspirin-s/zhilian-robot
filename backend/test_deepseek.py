"""
DeepSeek API 连接测试脚本
"""
import sys
sys.path.append('.')

from openai import OpenAI

# DeepSeek API 配置
API_KEY = "sk-08266faa1d184709878869666545ea9a"
BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-chat"

def test_connection():
    """测试 DeepSeek API 连接"""
    print("=" * 60)
    print("🔍 测试 DeepSeek API 连接...")
    print("=" * 60)
    
    try:
        client = OpenAI(
            api_key=API_KEY,
            base_url=BASE_URL,
            timeout=30.0
        )
        
        print("\n📤 发送测试请求...")
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "你是一个专业的产业链分析助手"
                },
                {
                    "role": "user",
                    "content": "请简单介绍一下你的能力"
                }
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        print("\n✅ API 连接成功!")
        print("\n📊 响应信息:")
        print(f"  模型: {response.model}")
        print(f"  Token 使用: {response.usage.total_tokens} tokens")
        print(f"    - 提示词: {response.usage.prompt_tokens}")
        print(f"    - 生成: {response.usage.completion_tokens}")
        
        print("\n💬 模型回复:")
        print("-" * 60)
        print(response.choices[0].message.content)
        print("-" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ API 连接失败!")
        print(f"错误信息: {str(e)}")
        print("\n🔧 排查建议:")
        print("  1. 检查网络连接")
        print("  2. 确认 API Key 是否正确")
        print("  3. 检查 DeepSeek 账户余额")
        print("  4. 查看 API 限流状态")
        return False


def test_entity_extraction():
    """测试实体提取功能"""
    print("\n" + "=" * 60)
    print("🔍 测试产业链实体提取功能...")
    print("=" * 60)
    
    test_text = """
    特斯拉公司在上海建立了超级工厂,主要生产Model 3和Model Y车型。
    工厂采用了先进的自动化生产线和机器人技术,大幅提升了生产效率。
    """
    
    try:
        client = OpenAI(
            api_key=API_KEY,
            base_url=BASE_URL,
            timeout=30.0
        )
        
        prompt = f"""
请从以下文本中提取产业链相关的实体信息:

文本: {test_text.strip()}

请提取以下类型的实体:
1. 企业名称
2. 产品名称
3. 技术名称
4. 地点

以JSON格式返回,格式如下:
{{
    "companies": ["企业1", "企业2"],
    "products": ["产品1", "产品2"],
    "technologies": ["技术1", "技术2"],
    "locations": ["地点1", "地点2"]
}}
"""
        
        print(f"\n📄 测试文本:\n{test_text}")
        print("\n📤 发送提取请求...")
        
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "你是一个专业的产业链分析助手,擅长从文本中提取实体信息。请以JSON格式返回结果。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        print("\n✅ 实体提取成功!")
        print(f"\n📊 Token 使用: {response.usage.total_tokens} tokens")
        
        print("\n📋 提取结果:")
        print("-" * 60)
        print(response.choices[0].message.content)
        print("-" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ 实体提取失败!")
        print(f"错误信息: {str(e)}")
        return False


if __name__ == "__main__":
    print("\n🚀 DeepSeek API 测试开始\n")
    
    # 测试 1: 基础连接
    test1 = test_connection()
    
    if test1:
        # 测试 2: 实体提取
        test2 = test_entity_extraction()
        
        print("\n" + "=" * 60)
        print("📊 测试总结")
        print("=" * 60)
        print(f"  基础连接测试: {'✅ 通过' if test1 else '❌ 失败'}")
        print(f"  实体提取测试: {'✅ 通过' if test2 else '❌ 失败'}")
        
        if test1 and test2:
            print("\n🎉 所有测试通过! DeepSeek API 配置成功!")
            print("\n下一步:")
            print("  1. 启动 Docker 服务: docker-compose up -d")
            print("  2. 访问前端: http://localhost:3000")
            print("  3. 访问 API 文档: http://localhost:8000/docs")
        else:
            print("\n⚠️ 部分测试未通过,请检查配置")
    else:
        print("\n⚠️ 基础连接测试失败,跳过后续测试")
    
    print("\n" + "=" * 60 + "\n")
