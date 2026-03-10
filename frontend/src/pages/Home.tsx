import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Input, Button, Typography, Space, message, Segmented } from 'antd';
import { PlayCircleOutlined, CloudOutlined, TrophyOutlined, ThunderboltOutlined, FlagOutlined } from '@ant-design/icons';
import { useGame } from '../store/GameContext';
import styles from './Home.module.css';

const { Title, Text } = Typography;

const difficulties = [
  { value: 'easy', label: '简单', icon: '🌟' },
  { value: 'normal', label: '普通', icon: '⚔️' },
  { value: 'hard', label: '困难', icon: '🔥' },
];

const Home: React.FC = () => {
  const navigate = useNavigate();
  const { createGame, state } = useGame();
  const [playerName, setPlayerName] = useState('农夫');
  const [difficulty, setDifficulty] = useState('normal');
  const [loading, setLoading] = useState(false);

  const getDifficultyInfo = (diff: string) => {
    const info: Record<string, { money: string; stamina: string; desc: string }> = {
      easy: { money: '1000', stamina: '150', desc: '作物生长快，金币多，暴风雨少' },
      normal: { money: '500', stamina: '100', desc: '标准难度' },
      hard: { money: '200', stamina: '80', desc: '作物生长慢，金币少，暴风雨多' },
    };
    return info[diff] || info.normal;
  };

  const handleStartGame = async () => {
    if (!playerName.trim()) {
      message.warning('请输入你的名字');
      return;
    }
    setLoading(true);
    const success = await createGame(playerName.trim(), difficulty);
    setLoading(false);
    if (success) {
      message.success('游戏开始！');
      navigate('/game/farm');
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.background}>
        <div className={styles.cloud1}>
          <CloudOutlined />
        </div>
        <div className={styles.cloud2}>
          <CloudOutlined />
        </div>
      </div>
      
      <Card className={styles.card} bordered={false}>
        <div className={styles.logo}>
          <span className={styles.emoji}>🌾</span>
          <Title level={1} className={styles.title}>农场模拟器</Title>
          <Text className={styles.subtitle}>AI 驱动的农场经营游戏</Text>
        </div>

        <div className={styles.form}>
          <Space direction="vertical" size="large" style={{ width: '100%' }}>
            <div>
              <Text strong>输入你的名字</Text>
              <Input
                size="large"
                placeholder="农夫"
                value={playerName}
                onChange={(e) => setPlayerName(e.target.value)}
                onPressEnter={handleStartGame}
                maxLength={20}
                className={styles.input}
              />
            </div>

            <div>
              <Text strong><FlagOutlined /> 选择难度</Text>
              <Segmented
                value={difficulty}
                onChange={(val) => setDifficulty(val as string)}
                options={difficulties}
                block
                className={styles.difficultySelector}
              />
              <div style={{ marginTop: 8, padding: '8px 12px', background: '#f5f5f5', borderRadius: 6 }}>
                <Space>
                  <Text><ThunderboltOutlined /> 初始金币: {getDifficultyInfo(difficulty).money}</Text>
                  <Text><TrophyOutlined /> 初始体力: {getDifficultyInfo(difficulty).stamina}</Text>
                </Space>
                <div style={{ marginTop: 4 }}>
                  <Text type="secondary">{getDifficultyInfo(difficulty).desc}</Text>
                </div>
              </div>
            </div>

            <Button
              type="primary"
              size="large"
              icon={<PlayCircleOutlined />}
              onClick={handleStartGame}
              loading={loading}
              block
              className={styles.button}
            >
              开始游戏
            </Button>

            {state.status.has_game && (
              <Button
                size="large"
                onClick={() => navigate('/game/farm')}
                block
              >
                继续游戏
              </Button>
            )}
          </Space>
        </div>

        <div className={styles.features}>
          <Text type="secondary">
            🌱 种植作物 &nbsp; 💧 浇水施肥 &nbsp; 🌾 收获出售 &nbsp; 🤖 AI 助手
          </Text>
        </div>
      </Card>
    </div>
  );
};

export default Home;
