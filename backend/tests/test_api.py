"""
API测试
"""
import pytest

def test_health_check(client):
    """测试健康检查接口"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_root_endpoint(client):
    """测试根路由"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data

def test_analyze_text(client, sample_text):
    """测试文本分析接口"""
    response = client.post(
        "/api/v1/nlp/analyze",
        json={
            "text": sample_text,
            "extract_entities": True,
            "extract_relations": True
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "entities" in data
    assert "relations" in data

def test_get_entity_categories(client):
    """测试获取实体类别"""
    response = client.get("/api/v1/nlp/entities/categories")
    assert response.status_code == 200
    data = response.json()
    assert "categories" in data
    assert len(data["categories"]) > 0
