import React, { useState, useEffect } from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { Layout, Menu, Button, Space, Typography, Dropdown, List, Modal, Input, message, Drawer } from 'antd';
import {
  HomeOutlined,
  ShopOutlined,
  TrophyOutlined,
  RobotOutlined,
  BarChartOutlined,
  SaveOutlined,
  FolderOpenOutlined,
  ArrowLeftOutlined,
  SettingOutlined,
  MenuOutlined,
  FlagOutlined,
  PlayCircleOutlined,
  ReloadOutlined,
} from '@ant-design/icons';
import { useGame } from '../store/GameContext';
import { apiClient } from '../api/client';
import styles from './GameLayout.module.css';

const { Header, Sider, Content } = Layout;
const { Text } = Typography;

interface MenuItem {
  key: string;
  icon: React.ReactNode;
  label: string;
}

const GameLayout: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { state, saveGame, loadGame, resetGame } = useGame();
  const [saveModalVisible, setSaveModalVisible] = useState(false);
  const [loadModalVisible, setLoadModalVisible] = useState(false);
  const [settingsVisible, setSettingsVisible] = useState(false);
  const [saveName, setSaveName] = useState('');
  const [saves, setSaves] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [mobileMenuVisible, setMobileMenuVisible] = useState(false);
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  const menuItems: MenuItem[] = [
    { key: '/game/farm', icon: <HomeOutlined />, label: '农场' },
    { key: '/game/shop', icon: <ShopOutlined />, label: '商店' },
    { key: '/game/achievements', icon: <TrophyOutlined />, label: '成就' },
    { key: '/game/statistics', icon: <BarChartOutlined />, label: '统计' },
    { key: '/game/ai', icon: <RobotOutlined />, label: 'AI助手' },
  ];

  const handleMenuClick = (key: string) => {
    navigate(key);
    setMobileMenuVisible(false);
  };

  const handleSave = async () => {
    const name = saveName.trim() || `存档_${Date.now()}`;
    setLoading(true);
    const success = await saveGame(name);
    setLoading(false);
    if (success) {
      message.success('游戏已保存');
      setSaveModalVisible(false);
      setSaveName('');
    }
  };

  const handleLoad = async (name: string) => {
    setLoading(true);
    const success = await loadGame(name);
    setLoading(false);
    if (success) {
      message.success('游戏已加载');
      setLoadModalVisible(false);
      navigate('/game/farm');
    }
  };

  const handleResetGame = () => {
    Modal.confirm({
      title: '重新开始',
      content: '确定要重新开始游戏吗？所有进度将会丢失！',
      okText: '确定',
      cancelText: '取消',
      onOk: async () => {
        const success = await resetGame();
        if (success) {
          message.success('游戏已重置');
          navigate('/');
        }
      },
    });
  };

  const handleNewGamePlus = () => {
    Modal.confirm({
      title: '新游戏+',
      content: '开始新游戏+会继承：\n• 已解锁的成就\n• 总游戏次数\n• 玩家名称\n\n将重置：\n• 金币和体力\n• 农田和背包\n• 季节和时间',
      okText: '开始新游戏+',
      cancelText: '取消',
      onOk: async () => {
        try {
          const result = await apiClient.startNewGamePlus();
          if (result.success) {
            message.success(result.message);
            navigate('/game/farm');
          }
        } catch (error) {
          message.error('新游戏+失败');
        }
      },
    });
  };

  const openSaveModal = () => {
    setSaveName(`存档_${new Date().toLocaleDateString()}`);
    setSaveModalVisible(true);
  };

  const openLoadModal = async () => {
    try {
      const data = await apiClient.getSaves();
      setSaves(data.saves);
      setLoadModalVisible(true);
    } catch (error) {
      message.error('获取存档列表失败');
    }
  };

  const saveMenuItems = [
    { key: 'save', icon: <SaveOutlined />, label: '保存游戏', onClick: openSaveModal },
    { key: 'load', icon: <FolderOpenOutlined />, label: '加载游戏', onClick: openLoadModal },
    { type: 'divider' as const },
    { key: 'newgameplus', icon: <PlayCircleOutlined />, label: '新游戏+', onClick: handleNewGamePlus },
    { key: 'reset', icon: <FlagOutlined />, label: '重新开始', danger: true, onClick: handleResetGame },
    { type: 'divider' as const },
    { key: 'settings', icon: <SettingOutlined />, label: '设置', onClick: () => setSettingsVisible(true) },
  ];

  const renderMenu = () => (
    <Menu
      mode="inline"
      selectedKeys={[location.pathname]}
      items={menuItems as any}
      onClick={({ key }) => handleMenuClick(key)}
      className={styles.menu}
      style={isMobile ? { width: 200 } : {}}
    />
  );

  return (
    <Layout className={styles.layout}>
      {isMobile ? (
        <>
          <Header className={styles.header}>
            <div className={styles.headerLeft}>
              <Button
                type="text"
                icon={<MenuOutlined />}
                onClick={() => setMobileMenuVisible(true)}
                className={styles.menuButton}
              />
              <div className={styles.gameInfo}>
                <Text strong className={styles.playerName}>
                  {state.player?.name || '农夫'}
                </Text>
              </div>
            </div>
            <div className={styles.headerRight}>
              <Space>
                <Text>💰{state.player?.gold ?? state.gameState?.gold ?? 0}</Text>
                <Text>⚡{state.player?.stamina ?? 100}</Text>
                <Dropdown menu={{ items: saveMenuItems }} placement="bottomRight">
                  <Button icon={<SettingOutlined />} className={styles.iconButton} />
                </Dropdown>
              </Space>
            </div>
          </Header>
          <Drawer
            title="导航菜单"
            placement="left"
            onClose={() => setMobileMenuVisible(false)}
            open={mobileMenuVisible}
            width={250}
          >
            {renderMenu()}
          </Drawer>
        </>
      ) : (
        <Header className={styles.header}>
          <div className={styles.headerLeft}>
            <Button
              type="text"
              icon={<ArrowLeftOutlined />}
              onClick={() => navigate('/')}
              className={styles.backButton}
            >
              退出
            </Button>
            <div className={styles.gameInfo}>
              <Text strong className={styles.playerName}>
                {state.player?.name || '农夫'}
              </Text>
              <Text className={styles.seasonInfo}>
                {state.status.season} {state.status.day}日 · {state.status.year}年
              </Text>
            </div>
          </div>
          <div className={styles.headerRight}>
            <Space>
              <Text>💰 {state.player?.gold ?? state.gameState?.gold ?? 0}</Text>
              <Text>⚡ {state.player?.stamina ?? 100}/{state.player?.max_stamina ?? 100}</Text>
              <Text>📅 第{state.status.day}天</Text>
              <Text>{getWeatherIcon(state.status.weather)}</Text>
              <Dropdown menu={{ items: saveMenuItems }} placement="bottomRight">
                <Button icon={<SettingOutlined />} className={styles.saveButton}>
                  设置
                </Button>
              </Dropdown>
            </Space>
          </div>
        </Header>
      )}
      <Layout>
        {!isMobile && (
          <Sider width={200} className={styles.sider} collapsible={true}>
            {renderMenu()}
          </Sider>
        )}
        <Content className={styles.content}>
          <Outlet />
        </Content>
      </Layout>

      <Modal
        title="保存游戏"
        open={saveModalVisible}
        onOk={handleSave}
        onCancel={() => setSaveModalVisible(false)}
        confirmLoading={loading}
      >
        <Input
          placeholder="输入存档名称"
          value={saveName}
          onChange={(e) => setSaveName(e.target.value)}
          onPressEnter={handleSave}
        />
      </Modal>

      <Modal
        title="加载游戏"
        open={loadModalVisible}
        onCancel={() => setLoadModalVisible(false)}
        footer={null}
        width={400}
      >
        {saves.length === 0 ? (
          <Text type="secondary">暂无存档</Text>
        ) : (
          <List
            dataSource={saves}
            renderItem={(item) => (
              <List.Item
                actions={[
                  <Button 
                    key="load" 
                    type="primary" 
                    size="small"
                    icon={<ReloadOutlined />}
                    onClick={() => handleLoad(item)}
                  >
                    加载
                  </Button>
                ]}
              >
                {item}
              </List.Item>
            )}
          />
        )}
      </Modal>

      <Drawer
        title="游戏设置"
        placement="right"
        onClose={() => setSettingsVisible(false)}
        open={settingsVisible}
        width={320}
      >
        <div className={styles.settingsContent}>
          <div className={styles.settingsSection}>
            <h4>快捷操作</h4>
            <Space direction="vertical" style={{ width: '100%' }}>
              <Button block icon={<SaveOutlined />} onClick={openSaveModal}>
                保存游戏
              </Button>
              <Button block icon={<FolderOpenOutlined />} onClick={openLoadModal}>
                加载游戏
              </Button>
            </Space>
          </div>
          <div className={styles.settingsSection}>
            <h4>游戏状态</h4>
            <div className={styles.statusGrid}>
              <div className={styles.statusItem}>
                <span>💰 金币</span>
                <Text strong>{state.player?.gold ?? state.gameState?.gold ?? 0}</Text>
              </div>
              <div className={styles.statusItem}>
                <span>⚡ 体力</span>
                <Text strong>{state.player?.stamina ?? 100}/{state.player?.max_stamina ?? 100}</Text>
              </div>
              <div className={styles.statusItem}>
                <span>📅 天数</span>
                <Text strong>第{state.status.day}天</Text>
              </div>
              <div className={styles.statusItem}>
                <span>🌤️ 天气</span>
                <Text strong>{getWeatherIcon(state.status.weather)} {state.status.weather}</Text>
              </div>
            </div>
          </div>
        </div>
      </Drawer>
    </Layout>
  );
};

function getWeatherIcon(weather: string): string {
  const icons: Record<string, string> = {
    '晴天': '☀️',
    '雨天': '🌧️',
    '风暴': '⛈️',
    '雪天': '❄️',
  };
  return icons[weather] || '☀️';
}

export default GameLayout;
