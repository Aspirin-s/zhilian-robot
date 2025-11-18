import React, { useState } from 'react'
import { Card, Input, Button, Select, message, Space, Spin } from 'antd'
import { SearchOutlined } from '@ant-design/icons'
import GraphVisualization from '../components/GraphVisualization'
import { graphService } from '../services/api'

const { Search } = Input

const GraphPage = () => {
  const [loading, setLoading] = useState(false)
  const [graphData, setGraphData] = useState({ nodes: [], edges: [] })
  const [depth, setDepth] = useState(2)

  const handleSearch = async (companyName) => {
    if (!companyName.trim()) {
      message.warning('请输入企业名称')
      return
    }

    setLoading(true)
    try {
      const data = await graphService.getCompanyRelations(companyName, depth)
      setGraphData(data)
      
      if (data.nodes.length === 0) {
        message.info('未找到相关数据,请尝试其他企业或先进行文本分析建立图谱')
      } else {
        message.success(`成功加载 ${data.nodes.length} 个节点, ${data.edges.length} 条关系`)
      }
    } catch (error) {
      message.error('查询失败: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <Card style={{ marginBottom: 16 }}>
        <Space direction="vertical" style={{ width: '100%' }} size="large">
          <div>
            <h2><SearchOutlined /> 产业链图谱查询</h2>
            <p>输入企业名称,查询其在产业链中的上下游关系</p>
          </div>
          
          <Space.Compact style={{ width: '100%' }}>
            <Select
              value={depth}
              onChange={setDepth}
              style={{ width: 150 }}
            >
              <Select.Option value={1}>深度: 1层</Select.Option>
              <Select.Option value={2}>深度: 2层</Select.Option>
              <Select.Option value={3}>深度: 3层</Select.Option>
              <Select.Option value={4}>深度: 4层</Select.Option>
            </Select>
            <Search
              placeholder="请输入企业名称,如: 华为、小米、特斯拉"
              enterButton="查询"
              size="large"
              onSearch={handleSearch}
              loading={loading}
            />
          </Space.Compact>

          <Space>
            <Button onClick={() => handleSearch('特斯拉')}>示例: 特斯拉</Button>
            <Button onClick={() => handleSearch('华为')}>示例: 华为</Button>
            <Button onClick={() => handleSearch('小米')}>示例: 小米</Button>
          </Space>
        </Space>
      </Card>

      <Spin spinning={loading}>
        <GraphVisualization data={graphData} />
      </Spin>
    </div>
  )
}

export default GraphPage
