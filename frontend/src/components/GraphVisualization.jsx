import React, { useEffect, useRef, useState } from 'react'
import * as echarts from 'echarts'
import { Card, Button, Tooltip, Switch, Space } from 'antd'
import { FullscreenOutlined, FullscreenExitOutlined } from '@ant-design/icons'

const GraphVisualization = ({ data }) => {
  const chartRef = useRef(null)
  const chartInstance = useRef(null)
  const containerRef = useRef(null)
  const [isFullscreen, setIsFullscreen] = useState(false)
  const [showEdgeLabels, setShowEdgeLabels] = useState(true)  // 控制边标签显示

  // 处理全屏切换
  const toggleFullscreen = () => {
    if (!containerRef.current) return

    if (!document.fullscreenElement) {
      containerRef.current.requestFullscreen().then(() => {
        setIsFullscreen(true)
        // 全屏后调整图表大小
        setTimeout(() => chartInstance.current?.resize(), 100)
      }).catch(err => {
        console.error('无法进入全屏:', err)
      })
    } else {
      document.exitFullscreen().then(() => {
        setIsFullscreen(false)
        // 退出全屏后调整图表大小
        setTimeout(() => chartInstance.current?.resize(), 100)
      })
    }
  }

  // 监听全屏状态变化
  useEffect(() => {
    const handleFullscreenChange = () => {
      setIsFullscreen(!!document.fullscreenElement)
      // 调整图表大小
      setTimeout(() => chartInstance.current?.resize(), 100)
    }

    document.addEventListener('fullscreenchange', handleFullscreenChange)
    return () => {
      document.removeEventListener('fullscreenchange', handleFullscreenChange)
    }
  }, [])

  useEffect(() => {
    if (!chartRef.current) return

    // 初始化图表
    if (!chartInstance.current) {
      chartInstance.current = echarts.init(chartRef.current)
    }

    // 转换数据格式
    const nodes = (data.nodes || []).map(node => ({
      id: node.id,
      name: node.name,
      symbolSize: 50,
      category: node.type,
      itemStyle: {
        color: getColorByType(node.type)
      }
    }))

    // 去重边 - 如果两个节点间有相同关系的多条边,只保留一条
    // 同时处理双向边(A→B 和 B→A 被视为相同)
    const edgeMap = new Map()
    ;(data.edges || []).forEach(edge => {
      // 创建规范化的键:小的id在前,大的id在后,确保双向边使用同一个键
      const sortedNodes = [edge.source, edge.target].sort()
      const key = `${sortedNodes[0]}-${sortedNodes[1]}-${edge.relation}`
      if (!edgeMap.has(key)) {
        edgeMap.set(key, edge)
      }
    })

    const edges = Array.from(edgeMap.values()).map(edge => ({
      source: edge.source,
      target: edge.target,
      value: edge.relation,  // 存储关系名
      lineStyle: {
        curveness: 0.3
      },
      label: {
        show: showEdgeLabels,  // 根据开关控制显示
        formatter: edge.relation,
        position: 'middle',  // 定位在连线中间
        fontSize: 11,
        color: '#666',
        backgroundColor: 'rgba(255, 255, 255, 0.85)',
        padding: [3, 6],
        borderRadius: 3
      }
    }))

    // 提取分类
    const categories = [...new Set(nodes.map(n => n.category))].map(cat => ({
      name: cat
    }))

    // 配置图表选项
    const option = {
      title: {
        text: '产业链图谱',
        left: 'center'
      },
      tooltip: {
        formatter: (params) => {
          if (params.dataType === 'node') {
            return `<strong>${params.data.name}</strong><br/>类型: ${params.data.category}`
          } else if (params.dataType === 'edge') {
            return `<strong>${params.data.source}</strong> → <strong>${params.data.target}</strong><br/>关系: <span style="color:#1890ff">${params.data.value || '关联'}</span>`
          }
        }
      },
      legend: [{
        data: categories.map(cat => cat.name),
        orient: 'vertical',
        left: 'left'
      }],
      series: [{
        type: 'graph',
        layout: 'force',
        data: nodes,
        links: edges,
        categories: categories,
        roam: true,
        draggable: true,
        zoom: 1,
        label: {
          show: true,
          position: 'right',
          formatter: '{b}',
          fontSize: 14
        },
        edgeLabel: {
          show: false  // 禁用 series 级别的边标签,使用每条边自己的 label 配置
        },
        labelLayout: {
          hideOverlap: true,
          moveOverlap: 'shiftY'
        },
        scaleLimit: {
          min: 0.3,  // 允许更小的缩放
          max: 3     // 允许更大的缩放
        },
        force: {
          repulsion: 1000,
          gravity: 0.1,
          edgeLength: 150,
          layoutAnimation: true
        },
        lineStyle: {
          color: 'source',
          curveness: 0.3
        },
        emphasis: {
          focus: 'adjacency',
          lineStyle: {
            width: 3
          },
          label: {
            show: true
          }
        }
      }]
    }

    chartInstance.current.setOption(option)

    // 响应式调整
    const resizeObserver = new ResizeObserver(() => {
      chartInstance.current?.resize()
    })
    resizeObserver.observe(chartRef.current)

    return () => {
      resizeObserver.disconnect()
    }
  }, [data, showEdgeLabels])  // 添加 showEdgeLabels 依赖

  // 根据类型返回颜色
  const getColorByType = (type) => {
    const colorMap = {
      'companies': '#5470c6',
      'products': '#91cc75',
      'technologies': '#fac858',
      'persons': '#ee6666',
      'locations': '#73c0de',
      'organizations': '#3ba272'
    }
    return colorMap[type] || '#9a60b4'
  }

  return (
    <Card
      ref={containerRef}
      style={isFullscreen ? {
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        zIndex: 9999,
        margin: 0,
        borderRadius: 0
      } : {}}
      extra={
        <Space>
          <span style={{ fontSize: '14px', color: '#666' }}>显示关系标签</span>
          <Switch 
            checked={showEdgeLabels} 
            onChange={setShowEdgeLabels}
            size="small"
          />
          <Tooltip title={isFullscreen ? "退出全屏" : "全屏显示"}>
            <Button
              type="text"
              icon={isFullscreen ? <FullscreenExitOutlined /> : <FullscreenOutlined />}
              onClick={toggleFullscreen}
            />
          </Tooltip>
        </Space>
      }
    >
      <div 
        ref={chartRef} 
        style={{ 
          width: '100%', 
          height: isFullscreen ? 'calc(100vh - 80px)' : '600px' 
        }}
      />
    </Card>
  )
}

export default GraphVisualization
