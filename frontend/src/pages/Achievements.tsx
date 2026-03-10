import React, { useEffect, useState } from 'react';
import { Card, Typography, List, Tag, Progress, Empty } from 'antd';
import { TrophyOutlined, LockOutlined, CheckCircleOutlined } from '@ant-design/icons';
import { apiClient } from '../api/client';
import type { Achievement } from '../types';
import styles from './Achievements.module.css';

const { Title, Text } = Typography;

const Achievements: React.FC = () => {
  const [achievements, setAchievements] = useState<Achievement[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAchievements();
  }, []);

  const loadAchievements = async () => {
    try {
      const data = await apiClient.getAchievements();
      setAchievements(data);
    } catch (error) {
      console.error('加载成就失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const getIcon = (unlocked: boolean) => {
    return unlocked ? <CheckCircleOutlined /> : <LockOutlined />;
  };

  const getTagColor = (unlocked: boolean) => {
    return unlocked ? 'success' : 'default';
  };

  return (
    <div>
      <Title level={2}>
        <TrophyOutlined /> 成就
      </Title>
      
      {achievements.length === 0 ? (
        <Card>
          <Empty description="暂无成就数据" />
        </Card>
      ) : (
        <Card>
          <List
            dataSource={achievements}
            renderItem={(item) => (
              <List.Item
                className={item.unlocked ? styles.unlocked : styles.locked}
              >
                <List.Item.Meta
                  avatar={
                    <div className={styles.avatar}>
                      {getIcon(item.unlocked)}
                    </div>
                  }
                  title={
                    <div className={styles.titleRow}>
                      <Text strong>{item.name}</Text>
                      <Tag color={getTagColor(item.unlocked)}>
                        {item.unlocked ? '已解锁' : '未解锁'}
                      </Tag>
                    </div>
                  }
                  description={
                    <div>
                      <Text type="secondary">{item.description}</Text>
                      {item.progress > 0 && !item.unlocked && (
                        <Progress 
                          percent={Math.round((item.progress / item.target) * 100)} 
                          size="small"
                          className={styles.progress}
                        />
                      )}
                      <Text type="secondary" className={styles.reward}>
                        {item.reward_text}
                      </Text>
                    </div>
                  }
                />
              </List.Item>
            )}
          />
        </Card>
      )}
    </div>
  );
};

export default Achievements;
