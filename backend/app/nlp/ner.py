"""
NLP模块 - 命名实体识别(NER)
"""
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from config.settings import settings
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


class NERProcessor:
    """命名实体识别处理器"""
    
    def __init__(self):
        self.model_name = settings.NER_MODEL
        self.tokenizer = None
        self.model = None
        self.ner_pipeline = None
    
    def load_model(self):
        """加载NER模型"""
        try:
            logger.info(f"正在加载NER模型: {self.model_name}")
            logger.warning("⚠️ 首次加载可能需要10-15分钟下载模型文件,请耐心等待...")
            
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                timeout=300  # 5分钟超时
            )
            self.model = AutoModelForTokenClassification.from_pretrained(
                self.model_name,
                timeout=300
            )
            self.ner_pipeline = pipeline(
                "ner",
                model=self.model,
                tokenizer=self.tokenizer,
                aggregation_strategy="simple"
            )
            logger.info("✅ NER模型加载成功")
        except Exception as e:
            error_msg = f"❌ NER模型加载失败: {str(e)}\n"
            error_msg += "💡 建议: 1) 勾选'使用大模型分析'使用DeepSeek API (快速且准确)\n"
            error_msg += "       2) 或配置HuggingFace镜像: export HF_ENDPOINT=https://hf-mirror.com"
            logger.error(error_msg)
            raise RuntimeError(error_msg) from e
    
    def extract_entities(self, text: str) -> List[Dict]:
        """
        从文本中提取实体
        
        Args:
            text: 输入文本
            
        Returns:
            实体列表,每个实体包含entity_group、word、score等信息
        """
        if not self.ner_pipeline:
            self.load_model()
        
        try:
            entities = self.ner_pipeline(text)
            return self._process_entities(entities)
        except Exception as e:
            logger.error(f"实体提取失败: {str(e)}")
            return []
    
    def _process_entities(self, raw_entities: List[Dict]) -> List[Dict]:
        """
        处理原始实体结果
        
        Args:
            raw_entities: 模型输出的原始实体
            
        Returns:
            处理后的实体列表
        """
        processed = []
        for entity in raw_entities:
            processed.append({
                "text": entity.get("word", ""),
                "label": entity.get("entity_group", ""),
                "score": entity.get("score", 0.0),
                "start": entity.get("start", 0),
                "end": entity.get("end", 0)
            })
        return processed
    
    def extract_industry_entities(self, text: str) -> Dict[str, List[str]]:
        """
        提取产业链相关实体(企业、产品、技术等)
        
        Args:
            text: 输入文本
            
        Returns:
            分类后的实体字典
        """
        entities = self.extract_entities(text)
        
        # 分类实体
        categorized = {
            "companies": [],      # 企业
            "products": [],       # 产品
            "technologies": [],   # 技术
            "persons": [],        # 人物
            "locations": [],      # 地点
            "organizations": []   # 组织机构
        }
        
        for entity in entities:
            label = entity["label"].upper()
            text = entity["text"]
            
            if "ORG" in label or "COMPANY" in label:
                categorized["companies"].append(text)
            elif "PRODUCT" in label:
                categorized["products"].append(text)
            elif "TECH" in label:
                categorized["technologies"].append(text)
            elif "PER" in label:
                categorized["persons"].append(text)
            elif "LOC" in label or "GPE" in label:
                categorized["locations"].append(text)
        
        # 去重
        for key in categorized:
            categorized[key] = list(set(categorized[key]))
        
        return categorized


# 全局NER处理器实例
ner_processor = NERProcessor()
