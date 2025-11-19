import React, { useState } from 'react'
import { Layout as AntLayout, Menu } from 'antd'
import { 
  HomeOutlined, 
  DeploymentUnitOutlined, 
  BarChartOutlined,
  RobotOutlined,
  DatabaseOutlined
} from '@ant-design/icons'
import { useNavigate, useLocation } from 'react-router-dom'

const { Header, Content, Footer } = AntLayout

const Layout = ({ children }) => {
  const navigate = useNavigate()
  const location = useLocation()

  const menuItems = [
    {
      key: '/',
      icon: <HomeOutlined />,
      label: '首页',
    },
    {
      key: '/graph',
      icon: <DeploymentUnitOutlined />,
      label: '图谱查询',
    },
    {
      key: '/analysis',
      icon: <BarChartOutlined />,
      label: '文本分析',
    },
    {
      key: '/data',
      icon: <DatabaseOutlined />,
      label: '数据管理',
    },
  ]

  const handleMenuClick = ({ key }) => {
    navigate(key)
  }

  return (
    <AntLayout style={{ minHeight: '100vh' }}>
      <Header style={{ 
        display: 'flex', 
        alignItems: 'center',
        background: '#001529'
      }}>
        <div style={{ 
          color: 'white', 
          fontSize: '20px', 
          marginRight: '50px',
          display: 'flex',
          alignItems: 'center',
          gap: '10px'
        }}>
          <RobotOutlined style={{ fontSize: '24px' }} />
          智链机器人
        </div>
        <Menu
          theme="dark"
          mode="horizontal"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={handleMenuClick}
          style={{ flex: 1, minWidth: 0 }}
        />
      </Header>
      <Content style={{ padding: '24px', background: '#f0f2f5' }}>
        {children}
      </Content>
      <Footer style={{ textAlign: 'center' }}>
        智链机器人 ©2025 - 大模型驱动的产业链图谱自动构建平台
      </Footer>
    </AntLayout>
  )
}

export default Layout
