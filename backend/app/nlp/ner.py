"""
NLP模块 - 命名实体识别(NER)
"""
try:
    from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

from config.settings import settings
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

if not TRANSFORMERS_AVAILABLE:
    logger.info("transformers 未安装，NER 功能将被禁用。项目将使用 DeepSeek LLM 进行实体提取。")


class NERProcessor:
    """命名实体识别处理器"""
    
    def __init__(self):
        if not TRANSFORMERS_AVAILABLE:
            self.model_name = None
            self.tokenizer = None
            self.model = None
            self.ner_pipeline = None
            return
            
        self.model_name = settings.NER_MODEL
        self.tokenizer = None
        self.model = None
        self.ner_pipeline = None
    
    def load_model(self):
        """加载NER模型"""
        if not TRANSFORMERS_AVAILABLE:
            logger.warning("跳过 NER 模型加载：transformers 未安装")
            return
            
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
        从文本中提取命名实体
        
        如果 transformers 未安装，返回空列表
        """
        if not TRANSFORMERS_AVAILABLE:
            logger.debug("NER功能未启用，返回空结果。请使用 DeepSeek LLM 进行实体提取。")
            return []
        
        if self.ner_pipeline is None:
            logger.warning("NER模型未加载，尝试加载...")
            self.load_model()
            if self.ner_pipeline is None:
                return []
        
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
            raw_entities: pipeline输出的原始实体列表
            
        Returns:
            格式化后的实体列表
        """
        processed = []
        for entity in raw_entities:
            entity_type = entity.get('entity_group', 'UNKNOWN')
            word = entity.get('word', '')
            score = entity.get('score', 0.0)
            
            # 映射实体类型到中文
            type_mapping = {
                'PER': 'person',
                'ORG': 'organization',
                'LOC': 'location',
                'MISC': 'misc'
            }
            
            processed.append({
                'text': word.strip(),
                'type': type_mapping.get(entity_type, entity_type.lower()),
                'confidence': float(score)
            })
        
        return processed


# 全局实例
ner_processor = NERProcessor()
