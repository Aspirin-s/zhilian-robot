import React, { useEffect, useRef } from 'react'
import * as echarts from 'echarts'
import { Card } from 'antd'

const GraphVisualization = ({ data }) => {
  const chartRef = useRef(null)
  const chartInstance = useRef(null)

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

    const edges = (data.edges || []).map(edge => ({
      source: edge.source,
      target: edge.target,
      label: {
        show: true,
        formatter: edge.relation,
        fontSize: 12,
        color: '#333',
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        padding: [4, 8],
        borderRadius: 4,
        position: 'middle'  // 标签位置在边的中间
      },
      lineStyle: {
        curveness: 0.3
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
            return `${params.data.name}<br/>类型: ${params.data.category}`
          } else if (params.dataType === 'edge') {
            return `${params.data.source} → ${params.data.target}`
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
        draggable: true,  // 启用节点拖拽
        label: {
          show: true,
          position: 'right',
          formatter: '{b}'
        },
        edgeLabel: {
          show: true,
          fontSize: 12,
          color: '#333',
          position: 'middle'  // 边标签固定在边的中点
        },
        labelLayout: {
          hideOverlap: false
        },
        scaleLimit: {
          min: 0.4,
          max: 2
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
  }, [data])

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
    <Card>
      <div 
        ref={chartRef} 
        style={{ width: '100%', height: '600px' }}
      />
    </Card>
  )
}

export default GraphVisualization
