"""
NLP模块 - 关系抽取(RE)
"""
try:
    from transformers import AutoTokenizer, AutoModel
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

from config.settings import settings
import logging
from typing import List, Dict, Tuple

logger = logging.getLogger(__name__)

if not TRANSFORMERS_AVAILABLE:
    logger.info("transformers/torch 未安装，关系抽取功能将被禁用。项目将使用 DeepSeek LLM 进行关系抽取。")


class REProcessor:
    """关系抽取处理器"""
    
    def __init__(self):
        if not TRANSFORMERS_AVAILABLE:
            self.model_name = None
            self.tokenizer = None
            self.model = None
            self.relation_types = []
            return
            
        self.model_name = settings.RE_MODEL
        self.tokenizer = None
        self.model = None
        
        # 预定义的产业链关系类型
        self.relation_types = [
            "供应商",      # supplier
            "客户",        # customer
            "合作伙伴",    # partner
            "竞争对手",    # competitor
            "投资方",      # investor
            "子公司",      # subsidiary
            "母公司",      # parent_company
            "技术提供方",  # technology_provider
            "产品使用方"   # product_user
        ]
    
    def load_model(self):
        """加载关系抽取模型"""
        if not TRANSFORMERS_AVAILABLE:
            logger.warning("跳过 RE 模型加载：transformers 未安装")
            return
            
        try:
            logger.info(f"正在加载RE模型: {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModel.from_pretrained(self.model_name)
            logger.info("RE模型加载成功")
        except Exception as e:
            logger.error(f"RE模型加载失败: {str(e)}")
            raise
    
    def extract_relations(self, text: str, entities: List[Dict]) -> List[Dict]:
        """
        从文本中提取实体间关系
        
        如果 transformers 未安装，返回空列表
        """
        if not TRANSFORMERS_AVAILABLE:
            logger.debug("RE功能未启用，返回空结果。请使用 DeepSeek LLM 进行关系抽取。")
            return []
        
        try:
            if len(entities) < 2:
                return []
            
            relations = []
            # 简化版关系抽取逻辑
            # 实际应该使用更复杂的模型
            for i, entity1 in enumerate(entities):
                for entity2 in entities[i+1:]:
                    relation = self._predict_relation(text, entity1, entity2)
                    if relation:
                        relations.append(relation)
            
            return relations
        except Exception as e:
            logger.error(f"关系抽取失败: {str(e)}")
            return []
    
    def _predict_relation(self, text: str, entity1: Dict, entity2: Dict) -> Dict:
        """
        预测两个实体之间的关系
        
        这是一个简化版实现,实际应该使用训练好的模型
        """
        if not TRANSFORMERS_AVAILABLE:
            return None
            
        # 这里应该是实际的模型预测逻辑
        # 为了简化,返回基于规则的关系
        
        # 基于文本中的关键词判断关系
        relation_keywords = {
            "供应商": ["供应", "提供", "采购自"],
            "客户": ["客户", "销售给", "服务"],
            "合作伙伴": ["合作", "联合", "共同"],
            "竞争对手": ["竞争", "对手"],
            "投资方": ["投资", "注资", "股东"],
            "子公司": ["子公司", "全资", "控股"],
            "母公司": ["母公司", "总部"],
        }
        
        entity1_text = entity1.get('text', '')
        entity2_text = entity2.get('text', '')
        
        for rel_type, keywords in relation_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    # 检查实体是否在关键词附近
                    if entity1_text in text and entity2_text in text:
                        return {
                            'head': entity1_text,
                            'relation': rel_type,
                            'tail': entity2_text,
                            'confidence': 0.5  # 规则based的置信度较低
                        }
        
        return None


# 全局实例
re_processor = REProcessor()
