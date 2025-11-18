"""
NLP模块 - 关系抽取(RE)
"""
from transformers import AutoTokenizer, AutoModel
from config.settings import settings
import logging
import torch
from typing import List, Dict, Tuple

logger = logging.getLogger(__name__)


class REProcessor:
    """关系抽取处理器"""
    
    def __init__(self):
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
        
        Args:
            text: 输入文本
            entities: 已识别的实体列表
            
        Returns:
            关系三元组列表 [(subject, relation, object), ...]
        """
        if not self.model:
            self.load_model()
        
        relations = []
        
        # 对每对实体进行关系判断
        for i, entity1 in enumerate(entities):
            for entity2 in entities[i+1:]:
                relation = self._predict_relation(text, entity1, entity2)
                if relation:
                    relations.append({
                        "subject": entity1["text"],
                        "relation": relation,
                        "object": entity2["text"],
                        "confidence": 0.8  # TODO: 实际置信度计算
                    })
        
        return relations
    
    def _predict_relation(self, text: str, entity1: Dict, entity2: Dict) -> str:
        """
        预测两个实体之间的关系
        
        Args:
            text: 原文本
            entity1: 实体1
            entity2: 实体2
            
        Returns:
            关系类型或None
        """
        # TODO: 实现基于大模型的关系分类
        # 这里使用规则匹配作为临时方案
        
        e1_text = entity1["text"]
        e2_text = entity2["text"]
        
        # 简单的规则匹配
        if "供应" in text or "提供" in text:
            return "供应商"
        elif "合作" in text:
            return "合作伙伴"
        elif "竞争" in text:
            return "竞争对手"
        elif "投资" in text:
            return "投资方"
        elif "子公司" in text or "全资" in text:
            return "子公司"
        
        return None
    
    def extract_supply_chain_relations(self, text: str, entities: Dict) -> List[Dict]:
        """
        提取产业链上下游关系
        
        Args:
            text: 输入文本
            entities: 分类后的实体字典
            
        Returns:
            产业链关系列表
        """
        relations = []
        companies = entities.get("companies", [])
        
        # 提取公司间的关系
        for i, company1 in enumerate(companies):
            for company2 in companies[i+1:]:
                # 检查上下游关系
                if self._is_upstream(text, company1, company2):
                    relations.append({
                        "upstream": company1,
                        "downstream": company2,
                        "relation_type": "supply_chain"
                    })
                elif self._is_upstream(text, company2, company1):
                    relations.append({
                        "upstream": company2,
                        "downstream": company1,
                        "relation_type": "supply_chain"
                    })
        
        return relations
    
    def _is_upstream(self, text: str, company1: str, company2: str) -> bool:
        """判断company1是否是company2的上游"""
        # 简化的规则判断
        keywords = ["供应", "提供", "零部件", "原材料", "芯片"]
        context = text[max(0, text.find(company1)-50):min(len(text), text.find(company2)+50)]
        return any(keyword in context for keyword in keywords)


# 全局RE处理器实例
re_processor = REProcessor()
