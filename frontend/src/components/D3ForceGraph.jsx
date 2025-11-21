import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { Card, Switch, Space, Tooltip, Button } from 'antd';
import { FullscreenOutlined, FullscreenExitOutlined } from '@ant-design/icons';

const D3ForceGraph = ({ data, onNodeClick }) => {
  const svgRef = useRef(null);
  const wrapperRef = useRef(null);
  const containerRef = useRef(null);
  const [dimensions, setDimensions] = useState({ width: 800, height: 600 });
  const [showEdgeLabels, setShowEdgeLabels] = useState(true);
  const [isFullscreen, setIsFullscreen] = useState(false);

  const COLOR_MAP = {
    'companies': '#3b82f6',
    'products': '#10b981',
    'technologies': '#f59e0b',
    'persons': '#ef4444',
    'locations': '#06b6d4',
    'organizations': '#8b5cf6',
    'unknown': '#94a3b8'
  };

  // 处理全屏切换
  const toggleFullscreen = () => {
    if (!containerRef.current) return;

    if (!document.fullscreenElement) {
      containerRef.current.requestFullscreen().then(() => {
        setIsFullscreen(true);
        setTimeout(() => updateDimensions(), 100);
      }).catch(err => console.error('无法进入全屏:', err));
    } else {
      document.exitFullscreen().then(() => {
        setIsFullscreen(false);
        setTimeout(() => updateDimensions(), 100);
      });
    }
  };

  // 监听全屏变化
  useEffect(() => {
    const handleFullscreenChange = () => {
      setIsFullscreen(!!document.fullscreenElement);
      setTimeout(() => updateDimensions(), 100);
    };
    document.addEventListener('fullscreenchange', handleFullscreenChange);
    return () => document.removeEventListener('fullscreenchange', handleFullscreenChange);
  }, []);

  const updateDimensions = () => {
    if (wrapperRef.current) {
      setDimensions({
        width: wrapperRef.current.clientWidth,
        height: wrapperRef.current.clientHeight
      });
    }
  };

  useEffect(() => {
    window.addEventListener('resize', updateDimensions);
    updateDimensions();
    return () => window.removeEventListener('resize', updateDimensions);
  }, []);

  useEffect(() => {
    if (!data || !svgRef.current || !data.nodes || data.nodes.length === 0) return;

    // 深拷贝数据
    const nodes = data.nodes.map(d => ({ ...d }));
    const links = data.edges ? data.edges.map(d => ({ ...d })) : [];

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();

    const { width, height } = dimensions;

    // 创建主组
    const g = svg.append("g");

    // 缩放行为
    const zoom = d3.zoom()
      .scaleExtent([0.1, 4])
      .on("zoom", (event) => {
        g.attr("transform", event.transform);
      });
    svg.call(zoom);

    // 力导向模拟
    const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links)
        .id(d => d.id)
        .distance(200))
      .force("charge", d3.forceManyBody().strength(-800))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collide", d3.forceCollide().radius(40));

    // 箭头标记
    svg.append("defs").selectAll("marker")
      .data(["end"])
      .enter().append("marker")
      .attr("id", "arrow")
      .attr("viewBox", "0 -5 10 10")
      .attr("refX", 30)
      .attr("refY", 0)
      .attr("markerWidth", 8)
      .attr("markerHeight", 8)
      .attr("orient", "auto")
      .append("path")
      .attr("d", "M0,-5L10,0L0,5")
      .attr("fill", "#64748b");

    // 渲染连线
    const link = g.append("g")
      .selectAll("line")
      .data(links)
      .join("line")
      .attr("stroke", "#475569")
      .attr("stroke-opacity", 0.6)
      .attr("stroke-width", 2)
      .attr("marker-end", "url(#arrow)");

    // 连线标签
    const linkLabel = g.append("g")
      .selectAll("text")
      .data(links)
      .join("text")
      .attr("dy", -8)
      .attr("text-anchor", "middle")
      .attr("fill", "#94a3b8")
      .attr("font-size", "11px")
      .attr("opacity", showEdgeLabels ? 1 : 0)
      .text(d => d.relation || d.relationship || '');

    // 渲染节点
    const node = g.append("g")
      .selectAll("g")
      .data(nodes)
      .join("g")
      .call(d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended))
      .on("click", (event, d) => {
        if (onNodeClick) onNodeClick(d);
      });

    // 节点圆圈
    node.append("circle")
      .attr("r", d => (d.value || 10) * 2 + 10)
      .attr("fill", d => COLOR_MAP[d.type] || COLOR_MAP.unknown)
      .attr("stroke", "#fff")
      .attr("stroke-width", 2)
      .attr("cursor", "pointer")
      .on("mouseover", function() {
        d3.select(this)
          .transition()
          .duration(200)
          .attr("r", d => (d.value || 10) * 2 + 15);
      })
      .on("mouseout", function() {
        d3.select(this)
          .transition()
          .duration(200)
          .attr("r", d => (d.value || 10) * 2 + 10);
      });

    // 节点标签
    node.append("text")
      .attr("dy", "0.31em")
      .attr("x", d => (d.value || 10) * 2 + 15)
      .attr("text-anchor", "start")
      .attr("fill", "#e2e8f0")
      .attr("font-size", "13px")
      .attr("font-weight", "500")
      .text(d => d.name);

    // 模拟更新
    simulation.on("tick", () => {
      link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

      linkLabel
        .attr("x", d => (d.source.x + d.target.x) / 2)
        .attr("y", d => (d.source.y + d.target.y) / 2);

      node.attr("transform", d => `translate(${d.x},${d.y})`);
    });

    // 拖拽函数
    function dragstarted(event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event, d) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragended(event, d) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

    return () => {
      simulation.stop();
    };
  }, [data, dimensions, showEdgeLabels, onNodeClick]);

  return (
    <Card
      ref={containerRef}
      className="d3-graph-card"
      style={isFullscreen ? {
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        zIndex: 9999,
        margin: 0,
        borderRadius: 0,
        background: '#0f172a'
      } : {
        background: 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)',
        border: '1px solid #334155'
      }}
      extra={
        <Space>
          <span style={{ fontSize: '13px', color: '#94a3b8' }}>显示关系标签</span>
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
              style={{ color: '#94a3b8' }}
            />
          </Tooltip>
        </Space>
      }
    >
      <div 
        ref={wrapperRef}
        style={{ 
          width: '100%', 
          height: isFullscreen ? 'calc(100vh - 80px)' : '600px',
          borderRadius: '8px',
          overflow: 'hidden'
        }}
      >
        <svg 
          ref={svgRef} 
          width={dimensions.width} 
          height={dimensions.height}
          style={{ background: 'transparent', cursor: 'grab' }}
        />
      </div>
    </Card>
  );
};

export default D3ForceGraph;
