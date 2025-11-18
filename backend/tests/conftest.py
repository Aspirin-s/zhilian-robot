"""
测试配置
"""
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    """测试客户端"""
    return TestClient(app)

@pytest.fixture
def sample_text():
    """示例文本"""
    return """
    华为技术有限公司是全球领先的ICT解决方案供应商。
    公司与台积电合作,采购先进芯片。华为的5G技术处于行业领先地位。
    """
