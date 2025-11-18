"""
NLP模块 - 大语言模型集成
"""
from typing import List, Dict, Optional
import logging
from config.settings import settings

logger = logging.getLogger(__name__)

# 尝试导入OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI库未安装,部分功能将不可用")


class LLMProcessor:
    """大语言模型处理器"""
    
    def __init__(self):
        self.client = None
        self.model = settings.OPENAI_MODEL
        
        if OPENAI_AVAILABLE and settings.OPENAI_API_KEY:
            # 使用 DeepSeek API (兼容 OpenAI 接口)
            self.client = OpenAI(
                api_key=settings.OPENAI_API_KEY,
                base_url=settings.OPENAI_API_BASE
            )
    
    def extract_entities_with_llm(self, text: str) -> Dict:
        """
        使用大模型提取实体
        
        Args:
            text: 输入文本
            
        Returns:
            提取的实体信息
        """
        if not self.client:
            logger.error("OpenAI客户端未初始化")
            return {}
        
        prompt = f"""
        请从以下文本中提取机器人产业链相关的实体信息:
        
        文本: {text}
        
        请提取以下类型的实体:
        1. 企业名称
        2. 产品名称
        3. 技术名称
        4. 关键人物
        5. 地点
        
        以JSON格式返回,格式如下:
        {{
            "companies": ["企业1", "企业2"],
            "products": ["产品1", "产品2"],
            "technologies": ["技术1", "技术2"],
            "persons": ["人物1", "人物2"],
            "locations": ["地点1", "地点2"]
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的产业链分析助手,擅长从文本中提取实体信息。只返回JSON,不要包含任何其他文本或Markdown标记。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            result = response.choices[0].message.content
            # 清理可能的Markdown代码块标记
            import json
            result = result.strip()
            if result.startswith("```"):
                # 移除 ```json 或 ``` 开头
                result = result.split('\n', 1)[1] if '\n' in result else result
            if result.endswith("```"):
                # 移除 ``` 结尾
                result = result.rsplit('\n', 1)[0] if '\n' in result else result
            result = result.strip()
            
            logger.info(f"LLM实体提取结果: {result[:200]}...")
            return json.loads(result)
        except Exception as e:
            logger.error(f"LLM实体提取失败: {str(e)}, 原始响应: {response.choices[0].message.content if 'response' in locals() else 'N/A'}")
            return {}
    
    def extract_relations_with_llm(self, text: str, entities: Dict) -> List[Dict]:
        """
        使用大模型提取关系
        
        Args:
            text: 输入文本
            entities: 已提取的实体
            
        Returns:
            关系列表
        """
        if not self.client:
            logger.error("OpenAI客户端未初始化")
            return []
        
        prompt = f"""
        基于以下文本和已识别的实体,请提取它们之间的产业链关系:
        
        文本: {text}
        
        实体: {entities}
        
        请识别以下类型的关系:
        - 供应关系(供应商-客户)
        - 合作关系
        - 竞争关系
        - 投资关系
        - 上下游关系
        
        以JSON格式返回关系列表,格式如下:
        [
            {{
                "subject": "实体1",
                "relation": "关系类型",
                "object": "实体2",
                "confidence": 0.9
            }}
        ]
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的产业链关系分析专家。只返回JSON数组,不要包含任何其他文本或Markdown标记。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            result = response.choices[0].message.content
            # 清理可能的Markdown代码块标记
            import json
            result = result.strip()
            if result.startswith("```"):
                result = result.split('\n', 1)[1] if '\n' in result else result
            if result.endswith("```"):
                result = result.rsplit('\n', 1)[0] if '\n' in result else result
            result = result.strip()
            
            logger.info(f"LLM关系提取结果: {result[:200]}...")
            return json.loads(result)
        except Exception as e:
            logger.error(f"LLM关系提取失败: {str(e)}, 原始响应: {response.choices[0].message.content if 'response' in locals() else 'N/A'}")
            return []
    
    def analyze_industry_chain(self, text: str) -> Dict:
        """
        综合分析产业链结构
        
        Args:
            text: 输入文本
            
        Returns:
            产业链分析结果
        """
        entities = self.extract_entities_with_llm(text)
        relations = self.extract_relations_with_llm(text, entities)
        
        return {
            "entities": entities,
            "relations": relations,
            "summary": self._generate_summary(entities, relations)
        }
    
    def _generate_summary(self, entities: Dict, relations: List[Dict]) -> str:
        """生成分析摘要"""
        company_count = len(entities.get("companies", []))
        relation_count = len(relations)
        
        return f"识别到{company_count}家企业,发现{relation_count}个关系"


# 全局LLM处理器实例
llm_processor = LLMProcessor()
