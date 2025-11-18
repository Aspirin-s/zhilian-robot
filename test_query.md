# 图谱查询问题排查

## 当前问题
- 前端查询"华为"返回空数据
- 后端返回 200 OK 但数据为空
- Neo4j 中有 9 个节点和 36 个关系

## 已确认
✅ 数据库中有数据 (9 nodes, 36 relations)  
✅ 后端服务正常运行  
✅ API 端点可访问  

## 可能原因
1. **Neo4j 查询返回的数据格式问题** - execute_query 方法处理 Neo4j 节点对象有问题
2. **关系路径匹配问题** - MATCH path 语句可能没有正确匹配
3. **数据格式化问题** - _format_graph_data 无法正确解析 relationships(path)

## 修复方案
已修改:
1. ✅ neo4j_db.py - 改进 execute_query 处理 Neo4j 对象
2. ✅ graph_service.py - 添加详细日志,改进数据格式化
3. 🔄 正在重新构建后端

## 测试步骤
构建完成后:
1. 启动后端: `docker-compose up -d backend`
2. 查看日志: `docker-compose logs -f backend`
3. 测试查询: 访问 http://localhost:8000/api/v1/graph/company/华为?depth=2
4. 查看日志输出,确认:
   - "查询企业: 华为, 深度: 2"
   - "查询返回 X 条记录"  
   - "第一条记录: {...}"
   - "格式化结果: X 个节点, X 条边"

## 备用方案
如果仍不行,直接在 Neo4j 浏览器中测试:
1. 访问 http://localhost:7474
2. 登录: neo4j / password123
3. 运行查询:
```cypher
MATCH (n:Entity)  
WHERE n.name CONTAINS '华为'
RETURN n
```
