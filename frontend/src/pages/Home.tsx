import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Input, Button, Typography, Space, message, Segmented } from 'antd';
import { PlayCircleOutlined, CloudOutlined, TrophyOutlined, ThunderboltOutlined, FlagOutlined, SunOutlined } from '@ant-design/icons';
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
      easy: { money: '1000', stamina: '150', desc: '作物生长快，金币多，暴风雨少，适合休闲玩家' },
      normal: { money: '500', stamina: '100', desc: '标准难度体验，考验你的经营策略' },
      hard: { money: '200', stamina: '80', desc: '极具挑战性，老玩家专用' },
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
        <div className={styles.sun}><SunOutlined /></div>
        <div className={styles.cloud1}><CloudOutlined /></div>
        <div className={styles.cloud2}><CloudOutlined /></div>
        <div className={styles.cloud3}><CloudOutlined /></div>
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
              <Text strong style={{ fontSize: 15 }}>输入你的名字</Text>
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
              <Text strong style={{ fontSize: 15 }}><FlagOutlined /> 选择难度</Text>
              <Segmented
                value={difficulty}
                onChange={(val) => setDifficulty(val as string)}
                options={difficulties}
                block
                className={styles.difficultySelector}
              />
              <div className={styles.difficultyInfo}>
                <span className={styles.difficultyInfoTitle}>{difficulties.find(d => d.value === difficulty)?.label} 模式</span>
                <div className={styles.stats}>
                  <div className={styles.stat}>
                    <ThunderboltOutlined style={{ color: '#52c41a' }} />
                    <span className={styles.statLabel}>初始金币:</span>
                    <span className={styles.statValue}>{getDifficultyInfo(difficulty).money}</span>
                  </div>
                  <div className={styles.stat}>
                    <TrophyOutlined style={{ color: '#52c41a' }} />
                    <span className={styles.statLabel}>初始体力:</span>
                    <span className={styles.statValue}>{getDifficultyInfo(difficulty).stamina}</span>
                  </div>
                </div>
                <div className={styles.description}>{getDifficultyInfo(difficulty).desc}</div>
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
                className={styles.continueButton}
              >
                继续游戏
              </Button>
            )}
          </Space>
        </div>

        <div className={styles.features}>
          <span className={styles.feature}>🌱 种植作物</span>
          <span className={styles.feature}>💧 浇水施肥</span>
          <span className={styles.feature}>🌾 收获出售</span>
          <span className={styles.feature}>🤖 AI 助手</span>
        </div>
      </Card>
    </div>
  );
};

export default Home;
