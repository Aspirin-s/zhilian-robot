import apiClient from '../utils/api'

// NLP分析相关API
export const nlpService = {
  // 分析文本
  analyzeText: (data) => {
    return apiClient.post('/api/v1/nlp/analyze', data)
  },

  // 使用大模型分析文本
  analyzeTextWithLLM: (data) => {
    return apiClient.post('/api/v1/nlp/analyze-llm', data)
  },

  // 获取实体类别
  getEntityCategories: () => {
    return apiClient.get('/api/v1/nlp/entities/categories')
  },

  // 获取关系类型
  getRelationTypes: () => {
    return apiClient.get('/api/v1/nlp/relations/types')
  }
}

// 图谱相关API
export const graphService = {
  // 构建图谱(从文本重新分析)
  buildGraph: (text, useLLM = false) => {
    return apiClient.post('/api/v1/graph/build', null, {
      params: { text, use_llm: useLLM }
    })
  },

  // 保存已分析的数据到图谱
  saveToGraph: (entities, relations) => {
    return apiClient.post('/api/v1/graph/save', {
      entities,
      relations
    })
  },

  // 查询产业链
  queryIndustryChain: (data) => {
    return apiClient.post('/api/v1/graph/query', data)
  },

  // 获取企业关系
  getCompanyRelations: (companyName, depth = 2) => {
    return apiClient.get(`/api/v1/graph/company/${encodeURIComponent(companyName)}`, {
      params: { depth }
    })
  },

  // 获取统计信息
  getStatistics: () => {
    return apiClient.get('/api/v1/graph/statistics')
  },

  // 清空图谱
  clearGraph: () => {
    return apiClient.delete('/api/v1/graph/clear')
  }
}
