import React, { useState, useEffect } from 'react'
import { Card, Row, Col, Statistic, Typography, Button, Space } from 'antd'
import { 
  DeploymentUnitOutlined, 
  LinkOutlined, 
  FileTextOutlined,
  RocketOutlined 
} from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { graphService } from '../services/api'

const { Title, Paragraph } = Typography

const HomePage = () => {
  const navigate = useNavigate()
  const [stats, setStats] = useState({ node_count: 0, relation_count: 0 })

  useEffect(() => {
    loadStatistics()
  }, [])

  const loadStatistics = async () => {
    try {
      const data = await graphService.getStatistics()
      setStats(data)
    } catch (error) {
      console.error('加载统计信息失败:', error)
    }
  }

  return (
    <div>
      <Card style={{ marginBottom: 24, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
        <Row align="middle">
          <Col flex="auto">
            <Title level={2} style={{ color: 'white', margin: 0 }}>
              <RocketOutlined /> 智链机器人
            </Title>
            <Title level={4} style={{ color: 'rgba(255,255,255,0.9)', fontWeight: 'normal', marginTop: 8 }}>
              大模型驱动的产业链图谱自动构建平台
            </Title>
            <Paragraph style={{ color: 'rgba(255,255,255,0.8)', marginTop: 16, fontSize: '16px' }}>
              利用先进的大语言模型技术,自动从多源文本中提取产业链实体与关系,
              构建可视化的知识图谱,助力产业研究与决策分析
            </Paragraph>
          </Col>
        </Row>
      </Card>

      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={12}>
          <Card>
            <Statistic
              title="图谱节点总数"
              value={stats.node_count}
              prefix={<DeploymentUnitOutlined />}
              valueStyle={{ color: '#3f8600' }}
            />
          </Card>
        </Col>
        <Col span={12}>
          <Card>
            <Statistic
              title="关系边数量"
              value={stats.relation_count}
              prefix={<LinkOutlined />}
              valueStyle={{ color: '#cf1322' }}
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={16}>
        <Col span={8}>
          <Card 
            hoverable
            style={{ height: '100%' }}
          >
            <DeploymentUnitOutlined style={{ fontSize: 48, color: '#1890ff' }} />
            <Title level={4} style={{ marginTop: 16 }}>图谱查询</Title>
            <Paragraph>
              查询企业的产业链上下游关系,探索复杂的产业网络结构
            </Paragraph>
            <Button type="primary" onClick={() => navigate('/graph')}>
              开始查询
            </Button>
          </Card>
        </Col>
        <Col span={8}>
          <Card 
            hoverable
            style={{ height: '100%' }}
          >
            <FileTextOutlined style={{ fontSize: 48, color: '#52c41a' }} />
            <Title level={4} style={{ marginTop: 16 }}>文本分析</Title>
            <Paragraph>
              从行业报告、新闻等文本中自动提取实体和关系信息
            </Paragraph>
            <Button type="primary" onClick={() => navigate('/analysis')}>
              开始分析
            </Button>
          </Card>
        </Col>
        <Col span={8}>
          <Card 
            hoverable
            style={{ height: '100%' }}
          >
            <RocketOutlined style={{ fontSize: 48, color: '#faad14' }} />
            <Title level={4} style={{ marginTop: 16 }}>核心功能</Title>
            <Paragraph>
              • 智能实体识别(NER)<br/>
              • 关系抽取(RE)<br/>
              • 知识图谱构建<br/>
              • 动态可视化
            </Paragraph>
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default HomePage
