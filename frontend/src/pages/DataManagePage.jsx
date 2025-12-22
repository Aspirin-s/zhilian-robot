import React, { useState, useEffect } from 'react'
import { 
  Card, 
  Table, 
  Button, 
  Tag, 
  Space, 
  Statistic, 
  Row, 
  Col, 
  Input,
  message,
  Modal,
  Tooltip,
  Tabs,
  Typography,
  Alert,
  InputNumber,
  Select,
  Progress
} from 'antd'
import {
  ReloadOutlined,
  RobotOutlined,
  CloudDownloadOutlined,
  DeleteOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  ExclamationCircleOutlined,
  FileTextOutlined,
  DatabaseOutlined
} from '@ant-design/icons'
import { dataService } from '../services/api'

const { Search } = Input
const { Title, Text } = Typography
const { confirm } = Modal

const DataManagePage = () => {
  const [loading, setLoading] = useState(false)
  const [articles, setArticles] = useState([])
  const [statistics, setStatistics] = useState(null)
  const [taskHistory, setTaskHistory] = useState([])
  const [pagination, setPagination] = useState({ current: 1, pageSize: 10, total: 0 })
  const [activeTab, setActiveTab] = useState('articles')
  const [selectedRowKeys, setSelectedRowKeys] = useState([])
  const [cleanupModalVisible, setCleanupModalVisible] = useState(false)
  const [cleanupDays, setCleanupDays] = useState(30)
  const [batchProcessing, setBatchProcessing] = useState(false)
  const [batchProgress, setBatchProgress] = useState(0)

  // 加载数据统计
  const loadStatistics = async () => {
    try {
      const response = await dataService.getDataStatistics()
      setStatistics(response)
    } catch (error) {
      message.error('加载统计数据失败: ' + error.message)
    }
  }

  // 加载文章列表
  const loadArticles = async (page = 1, pageSize = 10) => {
    setLoading(true)
    try {
      const response = await dataService.getArticles({
        skip: (page - 1) * pageSize,
        limit: pageSize
      })
      setArticles(response.articles || [])
      setPagination({
        current: page,
        pageSize: pageSize,
        total: response.total || 0
      })
    } catch (error) {
      message.error('加载文章列表失败: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  // 加载任务历史
  const loadTaskHistory = async () => {
    try {
      const response = await dataService.getTaskHistory({ limit: 20 })
      setTaskHistory(response.tasks || [])
    } catch (error) {
      message.error('加载任务历史失败: ' + error.message)
    }
  }

  useEffect(() => {
    // 优先加载统计数据
    loadStatistics()
    
    // 延迟加载文章列表和任务历史，避免并发请求过多
    const timer1 = setTimeout(() => {
      if (activeTab === 'articles') {
        loadArticles()
      }
    }, 100)
    
    const timer2 = setTimeout(() => {
      if (activeTab === 'tasks') {
        loadTaskHistory()
      }
    }, 200)
    
    return () => {
      clearTimeout(timer1)
      clearTimeout(timer2)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  // 手动触发关键词爬取
  const handleCrawlKeyword = async (keyword) => {
    if (!keyword || !keyword.trim()) {
      message.warning('请输入关键词')
      return
    }
    
    setLoading(true)
    try {
      const response = await dataService.crawlKeyword(keyword.trim())
      message.success(`爬取任务已提交: ${response.task_id}`)
      setTimeout(() => {
        loadStatistics()
        loadArticles()
        loadTaskHistory()
      }, 2000)
    } catch (error) {
      message.error('爬取失败: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  // 手动触发RSS更新
  const handleUpdateRss = async () => {
    setLoading(true)
    try {
      const response = await dataService.updateRss()
      message.success(`RSS更新任务已提交: ${response.task_id}`)
      setTimeout(() => {
        loadStatistics()
        loadArticles()
        loadTaskHistory()
      }, 2000)
    } catch (error) {
      message.error('RSS更新失败: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  // 处理文章(提取实体关系)
  const handleProcessArticle = async (articleId) => {
    setLoading(true)
    try {
      const response = await dataService.processArticle(articleId)
      message.success(`处理成功! 提取了 ${response.entities_count} 个实体和 ${response.relations_count} 个关系`)
      loadArticles(pagination.current, pagination.pageSize)
    } catch (error) {
      message.error('处理失败: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  // 清理旧数据
  const handleCleanup = () => {
    setCleanupModalVisible(true)
  }

  // 执行清理
  const executeCleanup = async () => {
    try {
      const response = await dataService.cleanupOldData(cleanupDays)
      message.success(`清理完成! 删除了 ${response.deleted_count} 条数据`)
      setCleanupModalVisible(false)
      loadStatistics()
      loadArticles()
    } catch (error) {
      message.error('清理失败: ' + error.message)
    }
  }

  // 批量处理文章
  const handleBatchProcess = async () => {
    if (selectedRowKeys.length === 0) {
      message.warning('请先选择要处理的文章')
      return
    }

    Modal.confirm({
      title: '批量处理文章',
      icon: <ExclamationCircleOutlined />,
      content: `确认处理选中的 ${selectedRowKeys.length} 篇文章吗?这将提取实体和关系并保存到图谱。`,
      okText: '确认',
      cancelText: '取消',
      onOk: async () => {
        setBatchProcessing(true)
        setBatchProgress(0)
        
        try {
          const response = await dataService.batchProcessArticles(selectedRowKeys)
          
          // 显示实体和关系提取统计
          const entitiesTotal = response.entities_extracted || 0
          const relationsTotal = response.relations_extracted || 0
          const statsMsg = (entitiesTotal > 0 || relationsTotal > 0)
            ? `，总计提取了 ${entitiesTotal} 个实体和 ${relationsTotal} 个关系`
            : ''

          message.success(
            `批量处理完成! 成功: ${response.success}, 失败: ${response.failed}, 跳过: ${response.skipped}${statsMsg}`,
            8
          )
          
          setSelectedRowKeys([])
          loadArticles(pagination.current, pagination.pageSize)
          loadStatistics()
        } catch (error) {
          message.error('批量处理失败: ' + error.message)
        } finally {
          setBatchProcessing(false)
          setBatchProgress(0)
        }
      }
    })
  }

  // 删除单篇文章
  const handleDeleteArticle = async (articleId) => {
    Modal.confirm({
      title: '确认删除',
      icon: <ExclamationCircleOutlined />,
      content: '确认删除这篇文章吗?此操作不可恢复。',
      okText: '确认删除',
      okType: 'danger',
      cancelText: '取消',
      onOk: async () => {
        try {
          await dataService.deleteArticle(articleId)
          message.success('文章删除成功')
          loadArticles(pagination.current, pagination.pageSize)
          loadStatistics()
        } catch (error) {
          message.error('删除失败: ' + error.message)
        }
      }
    })
  }

  // 批量删除文章
  const handleBatchDelete = async () => {
    if (selectedRowKeys.length === 0) {
      message.warning('请先选择要删除的文章')
      return
    }

    Modal.confirm({
      title: '批量删除文章',
      icon: <ExclamationCircleOutlined />,
      content: `确认删除选中的 ${selectedRowKeys.length} 篇文章吗?此操作不可恢复。`,
      okText: '确认删除',
      okType: 'danger',
      cancelText: '取消',
      onOk: async () => {
        try {
          const response = await dataService.batchDeleteArticles(selectedRowKeys)
          message.success(`批量删除完成! 已删除 ${response.deleted_count} 篇文章`)
          
          setSelectedRowKeys([])
          loadArticles(pagination.current, pagination.pageSize)
          loadStatistics()
        } catch (error) {
          message.error('批量删除失败: ' + error.message)
        }
      }
    })
  }

  // 文章列表列定义
  const articleColumns = [
    {
      title: '标题',
      dataIndex: 'title',
      key: 'title',
      width: '30%',
      ellipsis: true,
      render: (text, record) => (
        <Tooltip title={text}>
          <a href={record.url} target="_blank" rel="noopener noreferrer">
            {text}
          </a>
        </Tooltip>
      )
    },
    {
      title: '来源',
      dataIndex: 'source',
      key: 'source',
      width: '15%',
      render: (source) => {
        const colorMap = {
          'sina_finance': 'blue',
          '36kr': 'green',
          'robot_china': 'orange',
          'rss_ithome': 'purple',
          'rss_cnbeta': 'cyan',
          'rss_hacker_news': 'red',
          'rss_reddit': 'magenta',
          'crawler_sina': 'blue',
          'crawler_36kr': 'green',
          'crawler_baidu': 'cyan',
          'crawler_ofweek': 'orange'
        }
        return <Tag color={colorMap[source] || 'default'}>{source}</Tag>
      }
    },
    {
      title: '发布时间',
      dataIndex: 'published_at',
      key: 'published_at',
      width: '15%',
      render: (date) => date ? new Date(date).toLocaleString('zh-CN') : '-'
    },
    {
      title: '采集时间',
      dataIndex: 'crawled_at',
      key: 'crawled_at',
      width: '15%',
      render: (date) => date ? new Date(date).toLocaleString('zh-CN') : '-'
    },
    {
      title: '状态',
      dataIndex: 'processed',
      key: 'processed',
      width: '10%',
      render: (processed) => processed ? 
        <Tag color="success" icon={<CheckCircleOutlined />}>已处理</Tag> : 
        <Tag color="default" icon={<ClockCircleOutlined />}>未处理</Tag>
    },
    {
      title: '操作',
      key: 'action',
      width: '18%',
      render: (_, record) => (
        <Space>
          {!record.processed && (
            <Button 
              type="primary" 
              size="small" 
              icon={<RobotOutlined />}
              onClick={() => handleProcessArticle(record._id)}
            >
              处理
            </Button>
          )}
          <Button 
            type="link" 
            size="small"
            href={record.url}
            target="_blank"
          >
            查看
          </Button>
          <Button 
            danger
            type="link"
            size="small"
            icon={<DeleteOutlined />}
            onClick={() => handleDeleteArticle(record._id)}
          >
            删除
          </Button>
        </Space>
      )
    }
  ]

  // 任务历史列定义
  const taskColumns = [
    {
      title: '任务类型',
      dataIndex: 'task',
      key: 'task',
      width: '20%',
      render: (task) => {
        const typeMap = {
          'fetch_rss_updates': 'RSS更新',
          'crawl_all_news': '新闻爬取',
          'cleanup_old_crawl_data': '数据清理',
          'crawl_single_keyword': '关键词爬取'
        }
        return <Tag color="blue">{typeMap[task] || task}</Tag>
      }
    },
    {
      title: '处理文章数',
      dataIndex: 'articles_processed',
      key: 'articles_processed',
      width: '12%',
      render: (count) => count || 0
    },
    {
      title: '提取实体数',
      dataIndex: 'entities_extracted',
      key: 'entities_extracted',
      width: '12%',
      render: (count) => count || 0
    },
    {
      title: '提取关系数',
      dataIndex: 'relations_extracted',
      key: 'relations_extracted',
      width: '12%',
      render: (count) => count || 0
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: '12%',
      render: (status) => {
        const statusMap = {
          'completed': { color: 'success', icon: <CheckCircleOutlined />, text: '成功' },
          'failed': { color: 'error', icon: <ExclamationCircleOutlined />, text: '失败' },
          'running': { color: 'processing', icon: <ClockCircleOutlined />, text: '运行中' }
        }
        const config = statusMap[status] || statusMap['running']
        return <Tag color={config.color} icon={config.icon}>{config.text}</Tag>
      }
    },
    {
      title: '完成时间',
      dataIndex: 'completed_at',
      key: 'completed_at',
      width: '20%',
      render: (date) => date ? new Date(date).toLocaleString('zh-CN') : '-'
    },
    {
      title: '错误信息',
      dataIndex: 'error',
      key: 'error',
      width: '12%',
      ellipsis: true,
      render: (error) => error ? (
        <Tooltip title={error}>
          <Text type="danger">查看错误</Text>
        </Tooltip>
      ) : '-'
    }
  ]

  return (
    <div style={{ padding: '24px' }}>
      <Title level={2}>
        <DatabaseOutlined /> 数据采集管理 
      </Title>

      {/* 数据统计卡片 */}
      {statistics && (
        <Row gutter={16} style={{ marginBottom: 24 }}>
          <Col span={6}>
            <Card>
              <Statistic
                title="文章总数"
                value={statistics.total_articles}
                prefix={<FileTextOutlined />}
                valueStyle={{ color: '#3f8600' }}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="最近24小时"
                value={statistics.recent_articles}
                prefix={<ClockCircleOutlined />}
                valueStyle={{ color: '#1890ff' }}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="数据源数量"
                value={statistics.source_stats?.length || 0}
                prefix={<CloudDownloadOutlined />}
                valueStyle={{ color: '#cf1322' }}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="任务总数"
                value={statistics.recent_tasks?.length || 0}
                prefix={<RobotOutlined />}
                valueStyle={{ color: '#722ed1' }}
              />
            </Card>
          </Col>
        </Row>
      )}

      {/* 操作按钮 */}
      <Card style={{ marginBottom: 24 }}>
        <Space wrap>
          <Search
            placeholder="输入关键词"
            enterButton="开始爬取"
            size="large"
            onSearch={handleCrawlKeyword}
            style={{ width: 300 }}
            loading={loading}
          />
          <Button 
            type="primary" 
            icon={<CloudDownloadOutlined />} 
            size="large"
            onClick={handleUpdateRss}
            loading={loading}
          >
            更新RSS订阅 (推荐)
          </Button>
          <Button 
            icon={<ReloadOutlined />} 
            size="large"
            onClick={() => {
              loadStatistics()
              loadArticles()
              loadTaskHistory()
            }}
          >
            刷新数据
          </Button>
          <Button 
            danger
            icon={<DeleteOutlined />} 
            size="large"
            onClick={handleCleanup}
          >
            清理旧数据
          </Button>
        </Space>
      </Card>

      {/* 标签页 */}
      <Card>
        <Tabs
          activeKey={activeTab}
          onChange={setActiveTab}
          items={[
            {
              key: 'articles',
              label: '文章列表',
              children: (
                <>
                  {selectedRowKeys.length > 0 && (
                    <Alert
                      message={`已选择 ${selectedRowKeys.length} 篇文章`}
                      type="info"
                      showIcon
                      style={{ marginBottom: 16 }}
                      action={
                        <Space>
                          <Button 
                            type="primary" 
                            size="small"
                            onClick={handleBatchProcess}
                            loading={batchProcessing}
                          >
                            批量处理
                          </Button>
                          <Button 
                            danger
                            size="small"
                            icon={<DeleteOutlined />}
                            onClick={handleBatchDelete}
                          >
                            批量删除
                          </Button>
                          <Button 
                            size="small" 
                            onClick={() => setSelectedRowKeys([])}
                          >
                            取消选择
                          </Button>
                        </Space>
                      }
                    />
                  )}
                  {batchProcessing && (
                    <Progress 
                      percent={batchProgress} 
                      status="active" 
                      style={{ marginBottom: 16 }}
                    />
                  )}
                  <Table
                    columns={articleColumns}
                    dataSource={articles}
                    rowKey="_id"
                    loading={loading}
                    rowSelection={{
                      selectedRowKeys,
                      onChange: setSelectedRowKeys
                      // 移除 getCheckboxProps,允许选择所有文章(包括已处理的)进行删除
                    }}
                    pagination={{
                      ...pagination,
                      showSizeChanger: true,
                      showTotal: (total) => `共 ${total} 条数据`,
                      onChange: (page, pageSize) => loadArticles(page, pageSize)
                    }}
                  />
                </>
              )
            },
            {
              key: 'tasks',
              label: '任务历史',
              children: (
                <Table
                  columns={taskColumns}
                  dataSource={taskHistory}
                  rowKey="_id"
                  pagination={{
                    pageSize: 10,
                    showTotal: (total) => `共 ${total} 条任务`
                  }}
                />
              )
            },
            {
              key: 'sources',
              label: '数据源统计',
              children: statistics?.source_stats && (
                <Table
                  columns={[
                    {
                      title: '数据源',
                      dataIndex: '_id',
                      key: 'source',
                      render: (source) => <Tag color="blue">{source}</Tag>
                    },
                    {
                      title: '文章数量',
                      dataIndex: 'count',
                      key: 'count',
                      sorter: (a, b) => b.count - a.count
                    }
                  ]}
                  dataSource={statistics.source_stats}
                  rowKey="_id"
                  pagination={false}
                />
              )
            }
          ]}
        />
      </Card>

      {/* 清理数据弹窗 */}
      <Modal
        title="清理旧数据"
        open={cleanupModalVisible}
        onOk={executeCleanup}
        onCancel={() => setCleanupModalVisible(false)}
        okText="确认清理"
        cancelText="取消"
        okButtonProps={{ danger: true }}
      >
        <Space direction="vertical" style={{ width: '100%' }}>
          <Alert
            message="警告"
            description="此操作将永久删除选定天数之前的文章数据，且不可恢复！"
            type="warning"
            showIcon
          />
          <div style={{ marginTop: 16 }}>
            <Text>保留最近</Text>
            <InputNumber
              min={1}
              max={365}
              value={cleanupDays}
              onChange={setCleanupDays}
              style={{ margin: '0 8px' }}
            />
            <Text>天的数据</Text>
          </div>
          <div>
            <Text type="secondary">
              快速选择: 
              <Button type="link" size="small" onClick={() => setCleanupDays(1)}>1天</Button>
              <Button type="link" size="small" onClick={() => setCleanupDays(7)}>7天</Button>
              <Button type="link" size="small" onClick={() => setCleanupDays(30)}>30天</Button>
              <Button type="link" size="small" onClick={() => setCleanupDays(90)}>90天</Button>
            </Text>
          </div>
        </Space>
      </Modal>
    </div>
  )
}

export default DataManagePage
