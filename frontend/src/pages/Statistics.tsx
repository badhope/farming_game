import React, { useEffect, useState } from 'react';
import { Card, Typography, Statistic, Row, Col, Progress, Table } from 'antd';
import { DollarOutlined, HomeOutlined, RiseOutlined, TrophyOutlined } from '@ant-design/icons';
import { apiClient } from '../api/client';
import type { PlayerStats } from '../types';
import styles from './Statistics.module.css';

const { Title, Text } = Typography;

const Statistics: React.FC = () => {
  const [stats, setStats] = useState<PlayerStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const data = await apiClient.getPlayerStats();
      setStats(data);
    } catch (error) {
      console.error('加载统计失败:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <Title level={2}>📊 农场统计</Title>
      
      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="金币"
              value={stats?.gold || 0}
              prefix={<DollarOutlined />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="等级"
              value={stats?.level || 1}
              prefix={<RiseOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="已种植"
              value={stats?.planted_plots || 0}
              suffix={`/ ${stats?.total_plots || 9}`}
              prefix={<HomeOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="已收获"
              value={stats?.mature_plots || 0}
              prefix={<TrophyOutlined />}
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
        <Col xs={24} lg={12}>
          <Card title="农田使用情况">
            <div className={styles.progressItem}>
              <Text>已种植</Text>
              <Progress 
                percent={stats ? Math.round((stats.planted_plots / stats.total_plots) * 100) : 0}
                status="active"
                strokeColor="#52c41a"
              />
            </div>
            <div className={styles.progressItem}>
              <Text>已成熟</Text>
              <Progress 
                percent={stats ? Math.round((stats.mature_plots / stats.total_plots) * 100) : 0}
                status="success"
                strokeColor="#73d13d"
              />
            </div>
            <div className={styles.progressItem}>
              <Text>需要浇水</Text>
              <Progress 
                percent={stats ? Math.round((stats.needs_water / stats.total_plots) * 100) : 0}
                status="exception"
                strokeColor="#faad14"
              />
            </div>
          </Card>
        </Col>
        <Col xs={24} lg={12}>
          <Card title="农田详情">
            <Row gutter={16}>
              <Col span={12}>
                <div className={styles.statItem}>
                  <Text type="secondary">总地块</Text>
                  <Title level={3}>{stats?.total_plots || 0}</Title>
                </div>
              </Col>
              <Col span={12}>
                <div className={styles.statItem}>
                  <Text type="secondary">空地块</Text>
                  <Title level={3}>{stats?.empty_plots || 0}</Title>
                </div>
              </Col>
              <Col span={12}>
                <div className={styles.statItem}>
                  <Text type="secondary">已种植</Text>
                  <Title level={3}>{stats?.planted_plots || 0}</Title>
                </div>
              </Col>
              <Col span={12}>
                <div className={styles.statItem}>
                  <Text type="secondary">已成熟</Text>
                  <Title level={3}>{stats?.mature_plots || 0}</Title>
                </div>
              </Col>
            </Row>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Statistics;
