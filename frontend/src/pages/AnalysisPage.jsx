import React, { useState } from 'react'
import { 
  Card, 
  Input, 
  Button, 
  message, 
  Spin, 
  Tag, 
  Table,
  Space,
  Divider 
} from 'antd'
import { 
  FileTextOutlined, 
  ThunderboltOutlined,
  SaveOutlined 
} from '@ant-design/icons'
import { nlpService, graphService } from '../services/api'

const { TextArea } = Input

const AnalysisPage = () => {
  const [loading, setLoading] = useState(false)
  const [text, setText] = useState('')
  const [entities, setEntities] = useState({})
  const [relations, setRelations] = useState([])

  const handleAnalyze = async () => {
    if (!text.trim()) {
      message.warning('请输入要分析的文本')
      return
    }

    setLoading(true)
    try {
      // 使用 DeepSeek LLM 分析
      const data = await nlpService.analyzeTextWithLLM({
        text: text
      })

      setEntities(data.entities || {})
      setRelations(data.relations || [])
      message.success(data.summary || '分析完成')
    } catch (error) {
      message.error('分析失败: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  const handleBuildGraph = async () => {
    if (Object.keys(entities).length === 0) {
      message.warning('请先分析文本')
      return
    }

    setLoading(true)
    try {
      // 直接传递已分析的实体和关系数据,避免重复分析
      const result = await graphService.saveToGraph(entities, relations)
      if (result.success) {
        message.success(`图谱构建成功! 保存了 ${result.entities_count} 个实体, ${result.relations_count} 个关系`)
      } else {
        message.error('图谱构建失败: ' + result.error)
      }
    } catch (error) {
      message.error('图谱构建失败: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  const relationColumns = [
    {
      title: '主体',
      dataIndex: 'subject',
      key: 'subject',
    },
    {
      title: '关系',
      dataIndex: 'relation',
      key: 'relation',
      render: (text) => <Tag color="blue">{text}</Tag>
    },
    {
      title: '客体',
      dataIndex: 'object',
      key: 'object',
    },
    {
      title: '置信度',
      dataIndex: 'confidence',
      key: 'confidence',
      render: (val) => (val * 100).toFixed(0) + '%'
    }
  ]

  const sampleText = `
华为技术有限公司是一家领先的全球信息与通信技术解决方案供应商。
该公司与台积电合作,采购先进的芯片制造服务。华为的主要产品包括智能手机、
通信设备和云计算解决方案。在机器人领域,华为与ABB、库卡等公司建立合作关系,
共同推进工业机器人的智能化发展。
  `.trim()

  return (
    <div>
      <Card style={{ marginBottom: 16 }}>
        <Space direction="vertical" style={{ width: '100%' }} size="large">
          <div>
            <h2><FileTextOutlined /> 文本分析</h2>
            <p>输入产业相关文本,自动提取实体和关系,并构建知识图谱</p>
          </div>

          <div>
            <div style={{ marginBottom: 8 }}>
              <Button size="small" onClick={() => setText(sampleText)}>
                加载示例文本
              </Button>
            </div>
            <TextArea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="请输入要分析的文本内容,如行业报告、新闻资讯等..."
              rows={8}
            />
          </div>

          <Space>
            <Button 
              type="primary" 
              icon={<ThunderboltOutlined />}
              onClick={handleAnalyze}
              loading={loading}
            >
              分析文本
            </Button>
            <Button 
              icon={<SaveOutlined />}
              onClick={handleBuildGraph}
              loading={loading}
              disabled={Object.keys(entities).length === 0}
            >
              保存到图谱
            </Button>
          </Space>
        </Space>
      </Card>

      <Spin spinning={loading}>
        {Object.keys(entities).length > 0 && (
          <Card title="提取的实体" style={{ marginBottom: 16 }}>
            <Space direction="vertical" style={{ width: '100%' }}>
              {Object.entries(entities).map(([category, items]) => (
                items.length > 0 && (
                  <div key={category}>
                    <strong>{getCategoryLabel(category)}:</strong>
                    <div style={{ marginTop: 8 }}>
                      {items.map((item, idx) => (
                        <Tag key={idx} color="geekblue" style={{ margin: 4 }}>
                          {item}
                        </Tag>
                      ))}
                    </div>
                  </div>
                )
              ))}
            </Space>
          </Card>
        )}

        {relations.length > 0 && (
          <Card title="提取的关系">
            <Table 
              columns={relationColumns} 
              dataSource={relations.map((r, idx) => ({ ...r, key: idx }))}
              pagination={{ pageSize: 10 }}
            />
          </Card>
        )}
      </Spin>
    </div>
  )
}

const getCategoryLabel = (category) => {
  const labels = {
    companies: '企业',
    products: '产品',
    technologies: '技术',
    persons: '人物',
    locations: '地点',
    organizations: '组织'
  }
  return labels[category] || category
}

export default AnalysisPage
