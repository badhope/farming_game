import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Card, Input, Button, Typography, Space, message, Segmented, Collapse, FloatButton } from 'antd';
import { PlayCircleOutlined, FlagOutlined, MailOutlined, GithubOutlined, StarOutlined, TrophyOutlined, ThunderboltOutlined, HeartOutlined, SmileOutlined } from '@ant-design/icons';
import { useGame } from '../store/GameContext';
import styles from './Home.module.css';

const { Title, Text, Paragraph } = Typography;

const difficulties = [
  { value: 'easy', label: '简单', icon: '🌟' },
  { value: 'normal', label: '普通', icon: '⚔️' },
  { value: 'hard', label: '困难', icon: '🔥' },
];

const features = [
  {
    icon: '🌾',
    title: '真实农场经营',
    description: '种植、浇水、施肥、收获，体验完整的农场生活'
  },
  {
    icon: '🤖',
    title: 'AI 智能助手',
    description: '内置 AI 助手，提供种植建议和市场分析'
  },
  {
    icon: '🎮',
    title: '三种难度模式',
    description: '休闲、标准、硬核，满足不同玩家需求'
  },
  {
    icon: '📱',
    title: '随时随地游玩',
    description: '响应式网页设计，电脑手机都能玩'
  },
  {
    icon: '🏆',
    title: '成就系统',
    description: '丰富的成就挑战，解锁专属荣誉'
  },
  {
    icon: '💰',
    title: '经济系统',
    description: '买卖作物、购买道具，合理规划经营策略'
  }
];

const guideSteps = [
  {
    title: '创建角色',
    description: '输入你的名字，选择游戏难度',
    icon: '👤'
  },
  {
    title: '开始经营',
    description: '在农田种植作物，定期浇水施肥',
    icon: '🌱'
  },
  {
    title: '收获出售',
    description: '作物成熟后收获，出售换取金币',
    icon: '💰'
  },
  {
    title: '升级扩张',
    description: '用赚来的金币购买更多种子和道具',
    icon: '📈'
  }
];

const faqItems = [
  {
    key: '1',
    label: '这个游戏需要付费吗？',
    children: <Paragraph>农场模拟器是一款完全免费的网页游戏，无需下载安装，打开浏览器即可游玩。</Paragraph>
  },
  {
    key: '2',
    label: '如何开始游戏？',
    children: <Paragraph>在首页输入你的名字，选择难度后点击"开始游戏"按钮即可进入游戏。</Paragraph>
  },
  {
    key: '3',
    label: '游戏支持手机吗？',
    children: <Paragraph>支持！我们的游戏采用响应式设计，可以在手机、平板、电脑等设备上流畅运行。</Paragraph>
  },
  {
    key: '4',
    label: '作物生长需要多长时间？',
    children: <Paragraph>不同作物生长时间不同：胡萝卜2天、白菜3天、番茄5天等。浇水可以加速生长。</Paragraph>
  },
  {
    key: '5',
    label: '如何获得更多金币？',
    children: <Paragraph>种植高价值作物（如番茄、草莓）、及时收获成熟作物、完成游戏内成就都可以获得金币奖励。</Paragraph>
  },
  {
    key: '6',
    label: 'AI 助手能做什么？',
    children: <Paragraph>AI 助手可以提供种植建议、市场行情分析、作物种植策略等帮助，是你的虚拟农场顾问。</Paragraph>
  }
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

  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className={styles.landingPage}>
      <nav className={styles.navbar}>
        <div className={styles.navContent}>
          <div className={styles.logo} onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
            <span className={styles.logoEmoji}>🌾</span>
            <span className={styles.logoText}>农场模拟器</span>
          </div>
          <div className={styles.navLinks}>
            <Button type="text" onClick={() => scrollToSection('features')}>特色功能</Button>
            <Button type="text" onClick={() => scrollToSection('guide')}>游戏指南</Button>
            <Button type="text" onClick={() => scrollToSection('faq')}>常见问题</Button>
            <Button type="primary" onClick={() => scrollToSection('start')}>开始游戏</Button>
          </div>
        </div>
      </nav>

      <section className={styles.hero}>
        <div className={styles.heroBackground}>
          <div className={styles.heroSun}>☀️</div>
          <div className={styles.heroCloud} style={{ top: '10%', left: '5%' }}>☁️</div>
          <div className={styles.heroCloud} style={{ top: '20%', right: '10%' }}>☁️</div>
          <div className={styles.heroCloud} style={{ top: '30%', left: '40%' }}>☁️</div>
        </div>
        <div className={styles.heroContent}>
          <Title className={styles.heroTitle}>
            <span className={styles.heroEmoji}>🌾</span> 农场模拟器
          </Title>
          <Paragraph className={styles.heroSubtitle}>
            AI 驱动的农场经营游戏 · 体验真实的农场生活
          </Paragraph>
          <Space size="large" className={styles.heroButtons}>
            <Button type="primary" size="large" icon={<PlayCircleOutlined />} onClick={() => scrollToSection('start')}>
              立即开始
            </Button>
            <Button size="large" onClick={() => scrollToSection('guide')}>
              了解更多
            </Button>
          </Space>
          <div className={styles.heroStats}>
            <div className={styles.heroStat}>
              <StarOutlined /> <span>免费游玩</span>
            </div>
            <div className={styles.heroStat}>
              <SmileOutlined /> <span>无需下载</span>
            </div>
            <div className={styles.heroStat}>
              <HeartOutlined /> <span>休闲乐趣</span>
            </div>
          </div>
        </div>
      </section>

      <section id="features" className={styles.features}>
        <div className={styles.container}>
          <Title className={styles.sectionTitle}>🎯 核心特色</Title>
          <Paragraph className={styles.sectionSubtitle}>
            丰富的游戏内容，带给你沉浸式的农场体验
          </Paragraph>
          <div className={styles.featuresGrid}>
            {features.map((feature, index) => (
              <div key={index} className={styles.featureCard}>
                <div className={styles.featureIcon}>{feature.icon}</div>
                <Title level={4}>{feature.title}</Title>
                <Text type="secondary">{feature.description}</Text>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="guide" className={styles.guide}>
        <div className={styles.container}>
          <Title className={styles.sectionTitle}>📖 游戏指南</Title>
          <Paragraph className={styles.sectionSubtitle}>
            四个简单步骤，开启你的农场之旅
          </Paragraph>
          <div className={styles.guideSteps}>
            {guideSteps.map((step, index) => (
              <div key={index} className={styles.guideStep}>
                <div className={styles.stepNumber}>{index + 1}</div>
                <div className={styles.stepIcon}>{step.icon}</div>
                <Title level={4}>{step.title}</Title>
                <Text type="secondary">{step.description}</Text>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="start" className={styles.register}>
        <div className={styles.container}>
          <Title className={styles.sectionTitle}>🚀 开始游戏</Title>
          <Paragraph className={styles.sectionSubtitle}>
            创建你的农场，成为最优秀的农场主
          </Paragraph>
          <Card className={styles.registerCard} bordered={false}>
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
                className={styles.startButton}
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
          </Card>
        </div>
      </section>

      <section id="faq" className={styles.faq}>
        <div className={styles.container}>
          <Title className={styles.sectionTitle}>❓ 常见问题</Title>
          <Paragraph className={styles.sectionSubtitle}>
            解答你关心的问题
          </Paragraph>
          <div className={styles.faqContainer}>
            <Collapse 
              items={faqItems} 
              bordered={false}
                expandIconPosition="end"
              className={styles.faqCollapse}
            />
          </div>
        </div>
      </section>

      <footer className={styles.footer}>
        <div className={styles.container}>
          <div className={styles.footerContent}>
            <div className={styles.footerSection}>
              <Title level={4}>🌾 农场模拟器</Title>
              <Text type="secondary">AI 驱动的农场经营游戏</Text>
            </div>
            <div className={styles.footerSection}>
              <Title level={5}>快速链接</Title>
              <div className={styles.footerLinks}>
                <Link to="/download"><Button type="link">下载中心</Button></Link>
                <Button type="link" onClick={() => scrollToSection('features')}>特色功能</Button>
                <Button type="link" onClick={() => scrollToSection('guide')}>游戏指南</Button>
                <Button type="link" onClick={() => scrollToSection('faq')}>常见问题</Button>
              </div>
            </div>
            <div className={styles.footerSection}>
              <Title level={5}>联系我们</Title>
              <div className={styles.footerLinks}>
                <Button type="link" icon={<MailOutlined />}>反馈建议</Button>
                <Button type="link" icon={<GithubOutlined />}>GitHub</Button>
              </div>
            </div>
          </div>
          <div className={styles.footerBottom}>
            <Text type="secondary">© 2024 农场模拟器 · 让游戏更有趣</Text>
          </div>
        </div>
      </footer>

      <FloatButton.BackTop />
    </div>
  );
};

export default Home;
