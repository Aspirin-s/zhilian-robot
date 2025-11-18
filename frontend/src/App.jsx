import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { ConfigProvider } from 'antd'
import zhCN from 'antd/locale/zh_CN'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import GraphPage from './pages/GraphPage'
import AnalysisPage from './pages/AnalysisPage'

function App() {
  return (
    <ConfigProvider locale={zhCN}>
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/graph" element={<GraphPage />} />
            <Route path="/analysis" element={<AnalysisPage />} />
          </Routes>
        </Layout>
      </Router>
    </ConfigProvider>
  )
}

export default App
