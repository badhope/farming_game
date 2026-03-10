import React, { useState, useEffect } from 'react';
import { Card, Tabs, Button, InputNumber, message, Tag, Spin, Empty, Typography, Grid, Badge } from 'antd';
import { ShoppingCartOutlined, HistoryOutlined, PlusOutlined, MinusOutlined } from '@ant-design/icons';
import { useGame } from '../store/GameContext';
import { apiClient } from '../api/client';
import type { ShopItem } from '../types';
import styles from './Shop.module.css';

const { Text } = Typography;
const { useBreakpoint } = Grid;

const categoryEmojis: Record<string, string> = {
  seed: '🌱',
  fertilizer: '🧪',
  tool: '🔧',
  decoration: '🎃',
  building: '🏗️',
};

const categoryColors: Record<string, string> = {
  seed: 'green',
  fertilizer: 'blue',
  tool: 'purple',
  decoration: 'orange',
  building: 'red',
};

const Shop: React.FC = () => {
  const { state, dispatch } = useGame();
  const [items, setItems] = useState<ShopItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [buying, setBuying] = useState<string | null>(null);
  const [quantities, setQuantities] = useState<Record<string, number>>({});
  const [activeTab, setActiveTab] = useState('all');
  const screens = useBreakpoint();

  useEffect(() => {
    loadItems();
  }, []);

  const loadItems = async () => {
    setLoading(true);
    try {
      const data = await apiClient.getShopItems();
      setItems(data);
      const initialQuantities: Record<string, number> = {};
      data.forEach((item) => {
        initialQuantities[item.id] = 1;
      });
      setQuantities(initialQuantities);
    } catch (error) {
      message.error('加载商店失败');
    } finally {
      setLoading(false);
    }
  };

  const handleBuy = async (item: ShopItem) => {
    const quantity = quantities[item.id] || 1;
    const totalPrice = item.price * quantity;
    const playerGold = state.player?.gold ?? state.gameState?.gold ?? 0;

    if (playerGold < totalPrice) {
      message.error('金币不足!');
      return;
    }

    setBuying(item.id);
    try {
      const result = await apiClient.buyItem(item.id, quantity);
      if (result.success) {
        message.success(result.message);
        dispatch({ 
          type: 'UPDATE_PLAYER', 
          payload: { ...state.player, gold: result.remaining_gold } as any 
        });
      }
    } catch (error: any) {
      message.error(error.response?.data?.detail || '购买失败');
    } finally {
      setBuying(null);
    }
  };

  const updateQuantity = (itemId: string, delta: number) => {
    setQuantities((prev) => ({
      ...prev,
      [itemId]: Math.max(1, Math.min(99, (prev[itemId] || 1) + delta)),
    }));
  };

  const filteredItems = activeTab === 'all' 
    ? items 
    : items.filter((item) => item.category === activeTab);

  const playerGold = state.player?.gold ?? state.gameState?.gold ?? 0;

  const tabItems = [
    { key: 'all', label: '全部' },
    { key: 'seed', label: '🌱 种子' },
    { key: 'fertilizer', label: '🧪 肥料' },
    { key: 'tool', label: '🔧 工具' },
    { key: 'building', label: '🏗️ 建筑' },
    { key: 'decoration', label: '🎃 装饰' },
  ];

  if (loading) {
    return (
      <div className={styles.loadingContainer}>
        <Spin size="large" />
        <Text type="secondary">加载商店...</Text>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <Card className={styles.header}>
        <div className={styles.headerContent}>
          <div className={styles.shopTitle}>
            <ShoppingCartOutlined className={styles.shopIcon} />
            <Text strong className={styles.titleText}>农场商店</Text>
          </div>
          <Badge 
            count={`💰 ${playerGold}`} 
            className={styles.goldBadge}
            style={{ backgroundColor: '#faad14' }}
          />
        </div>
      </Card>

      <Tabs
        activeKey={activeTab}
        onChange={setActiveTab}
        items={tabItems}
        className={styles.tabs}
        size={screens.md ? 'default' : 'small'}
      />

      {filteredItems.length === 0 ? (
        <Empty description="该分类暂无商品" />
      ) : (
        <div 
          className={styles.itemsGrid}
          style={{ 
            gridTemplateColumns: screens.lg ? 'repeat(3, 1fr)' : screens.md ? 'repeat(2, 1fr)' : '1fr'
          }}
        >
          {filteredItems.map((item) => {
            const quantity = quantities[item.id] || 1;
            const totalPrice = item.price * quantity;
            const canAfford = playerGold >= totalPrice;

            return (
              <Card 
                key={item.id} 
                className={`${styles.itemCard} ${!canAfford ? styles.cantAfford : ''}`}
                hoverable
              >
                <div className={styles.itemHeader}>
                  <span className={styles.itemEmoji}>{item.emoji}</span>
                  <Tag color={categoryColors[item.category]}>
                    {categoryEmojis[item.category]} {item.category}
                  </Tag>
                </div>
                <div className={styles.itemInfo}>
                  <Text strong className={styles.itemName}>{item.name}</Text>
                  <Text type="secondary" className={styles.itemDesc}>{item.description}</Text>
                </div>
                <div className={styles.itemFooter}>
                  <div className={styles.priceSection}>
                    <Text className={styles.price}>💰 {item.price}</Text>
                    {quantity > 1 && (
                      <Text type="secondary" className={styles.totalPrice}>
                        ×{quantity} = {totalPrice}
                      </Text>
                    )}
                  </div>
                  <div className={styles.quantityControl}>
                    <Button 
                      size="small" 
                      icon={<MinusOutlined />} 
                      onClick={(e) => { e.stopPropagation(); updateQuantity(item.id, -1); }}
                      disabled={quantity <= 1}
                    />
                    <InputNumber
                      min={1}
                      max={99}
                      value={quantity}
                      onChange={(val) => setQuantities((prev) => ({ ...prev, [item.id]: val || 1 }))}
                      size="small"
                      className={styles.quantityInput}
                    />
                    <Button 
                      size="small" 
                      icon={<PlusOutlined />} 
                      onClick={(e) => { e.stopPropagation(); updateQuantity(item.id, 1); }}
                      disabled={quantity >= 99}
                    />
                  </div>
                </div>
                <Button
                  type="primary"
                  block
                  className={styles.buyButton}
                  onClick={(e) => { e.stopPropagation(); handleBuy(item); }}
                  loading={buying === item.id}
                  disabled={!canAfford}
                >
                  {canAfford ? '购买' : '金币不足'}
                </Button>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default Shop;
