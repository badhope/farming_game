import React, { useState, useEffect } from 'react';
import { Card, Button, Space, Typography, message, Modal, Grid, Spin, Empty, Progress } from 'antd';
import { useGame } from '../store/GameContext';
import { apiClient } from '../api/client';
import styles from './Farm.module.css';

const { Text } = Typography;
const { useBreakpoint } = Grid;

interface PlotData {
  row: number;
  col: number;
  has_crop: boolean;
  crop_name: string;
  crop_emoji: string;
  growth_stage: number;
  growth_progress: number;
  needs_water: boolean;
  days_since_planted: number;
  is_mature: boolean;
}

interface CropOption {
  name: string;
  emoji: string;
  price: number;
  sell_price: number;
  grow_days: number;
  description?: string;
}

interface TimeStatus {
  year: number;
  day: number;
  season: string;
  weather: string;
  tomorrow_weather: string | null;
  date_string: string;
  season_progress: number;
  year_progress: number;
  total_days: number;
}

const seasonEmojis: Record<string, string> = {
  '春': '🌸',
  '夏': '☀️',
  '秋': '🍂',
  '冬': '❄️',
};

const weatherEmojis: Record<string, string> = {
  '晴天': '☀️',
  '多云': '☁️',
  '雨天': '🌧️',
  '暴风雨': '⛈️',
  'sunny': '☀️',
  'cloudy': '☁️',
  'rainy': '🌧️',
  'stormy': '⛈️',
  '大风': '💨',
  '雪': '❄️',
  'fog': '🌫️',
};

const Farm: React.FC = () => {
  const { state, plantCrop, waterCrop, harvestCrop, advanceDay } = useGame();
  const [plots, setPlots] = useState<PlotData[]>([]);
  const [crops, setCrops] = useState<CropOption[]>([]);
  const [loading, setLoading] = useState(false);
  const [planting, setPlanting] = useState(false);
  const [plantModalVisible, setPlantModalVisible] = useState(false);
  const [selectedPlot, setSelectedPlot] = useState<{ row: number; col: number } | null>(null);
  const [hasGame, setHasGame] = useState(true);
  const [timeStatus, setTimeStatus] = useState<TimeStatus | null>(null);
  const screens = useBreakpoint();

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setPlanting(true);
    try {
      const status = await apiClient.getGameStatus();
      if (!status.has_game) {
        setHasGame(false);
        setPlots([]);
        setCrops([]);
        setTimeStatus(null);
        setPlanting(false);
        return;
      }
      setHasGame(true);
      
      const [plotsData, cropsData, timeData] = await Promise.all([
        apiClient.getPlots(),
        apiClient.getCrops(),
        apiClient.getTimeStatus(),
      ]);
      setPlots(plotsData);
      setCrops(cropsData as unknown as CropOption[]);
      setTimeStatus(timeData);
    } catch (error: any) {
      console.error('加载数据失败:', error);
      if (error.response?.status === 400) {
        setHasGame(false);
      } else {
        message.error('加载数据失败');
      }
    } finally {
      setPlanting(false);
    }
  };

  const handlePlotClick = async (plot: PlotData) => {
    if (plot.has_crop) {
      if (plot.is_mature) {
        setLoading(true);
        const success = await harvestCrop(plot.row, plot.col);
        if (success) {
          message.success(`收获了 ${plot.crop_emoji} ${plot.crop_name}!`);
          await loadData();
        }
        setLoading(false);
      } else if (plot.needs_water) {
        setLoading(true);
        const success = await waterCrop(plot.row, plot.col);
        if (success) {
          message.success('浇水成功!');
          await loadData();
        }
        setLoading(false);
      } else {
        message.info('作物正在生长中...');
      }
    } else {
      setSelectedPlot({ row: plot.row, col: plot.col });
      setPlantModalVisible(true);
    }
  };

  const handlePlant = async (crop: CropOption) => {
    if (!selectedPlot) return;
    
    const playerGold = state.player?.gold ?? 0;
    if (playerGold < crop.price) {
      message.error('金币不足!');
      return;
    }

    setLoading(true);
    const success = await plantCrop(selectedPlot.row, selectedPlot.col, crop.name);
    if (success) {
      message.success(`种植了 ${crop.emoji} ${crop.name}!`);
      setPlantModalVisible(false);
      await loadData();
    }
    setLoading(false);
  };

  const handleAdvanceDay = async () => {
    setLoading(true);
    const success = await advanceDay();
    if (success) {
      message.success('新的一天开始了!');
      await loadData();
    }
    setLoading(false);
  };

  const getPlotClass = (plot: PlotData): string => {
    const classes = [styles.plot];
    if (plot.is_mature) classes.push(styles.mature);
    else if (plot.needs_water) classes.push(styles.needsWater);
    return classes.join(' ');
  };

  const getGrowthStageClass = (stage: number): string => {
    return `crop-stage-${stage}`;
  };

  const gridSize = screens.lg ? 3 : screens.md ? 3 : 2;

  if (planting) {
    return (
      <div className={styles.loadingContainer}>
        <Spin size="large" />
        <Text type="secondary">加载农田数据...</Text>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      {timeStatus && (
        <div className={styles.timePanel}>
          <div className={styles.timeMain}>
            <span className={styles.seasonEmoji}>{seasonEmojis[timeStatus.season] || '🌸'}</span>
            <span className={styles.dateText}>{timeStatus.date_string}</span>
          </div>
          <div className={styles.weatherInfo}>
            <span className={styles.weatherCurrent}>
              {weatherEmojis[timeStatus.weather] || '☀️'}
              <span>{timeStatus.weather}</span>
            </span>
            <span className={styles.weatherTomorrow}>
              明天: {timeStatus.tomorrow_weather ? (
                <>
                  {weatherEmojis[timeStatus.tomorrow_weather] || '☀️'}
                  <span>{timeStatus.tomorrow_weather}</span>
                </>
              ) : '-'}
            </span>
          </div>
          <div className={styles.progressInfo}>
            <div className={styles.progressItem}>
              <span className={styles.progressLabel}>季节</span>
              <Progress 
                percent={Math.round(timeStatus.season_progress * 100)} 
                size="small" 
                showInfo={false}
                strokeColor="#52c41a"
                className={styles.progressBar}
              />
            </div>
          </div>
        </div>
      )}
      
      <Card className={styles.controls}>
        <Space wrap>
          <Button
            className={styles.advanceButton}
            onClick={handleAdvanceDay}
            loading={loading}
            size="large"
          >
            ⏰ 推进时间 (休息)
          </Button>
          <Text type="secondary">
            休息到下一天，作物会生长
          </Text>
        </Space>
      </Card>

      {planting ? (
        <Card>
          <Empty description="请先创建游戏或加载存档">
            <Button type="primary" onClick={() => window.location.href = '/'}>
              返回首页
            </Button>
          </Empty>
        </Card>
      ) : !hasGame ? (
        <Card>
          <Empty description="请先创建游戏或加载存档">
            <Button type="primary" onClick={() => window.location.href = '/'}>
              返回首页
            </Button>
          </Empty>
        </Card>
      ) : plots.length === 0 ? (
        <Card>
          <Empty description="还没有农田数据">
            <Button type="primary" onClick={loadData}>
              刷新数据
            </Button>
          </Empty>
        </Card>
      ) : (
        <div 
          className={styles.farmGrid}
          style={{ 
            gridTemplateColumns: `repeat(${gridSize}, 1fr)`,
            maxWidth: `${gridSize * 120}px`
          }}
        >
          {plots.map((plot, index) => (
            <div
              key={index}
              className={getPlotClass(plot)}
              onClick={() => !loading && handlePlotClick(plot)}
            >
              {plot.has_crop ? (
                <>
                  <span className={`${styles.cropEmoji} ${getGrowthStageClass(plot.growth_stage)}`}>
                    {plot.crop_emoji}
                  </span>
                  <span className={styles.cropName}>
                    {plot.crop_name}
                  </span>
                  <div className={styles.growthBar}>
                    <div 
                      className={styles.growthFill}
                      style={{ width: `${(plot.growth_stage / 4) * 100}%` }}
                    />
                  </div>
                  <div className={styles.plotInfo}>
                    <Text type="secondary" className={styles.days}>
                      {plot.days_since_planted}天
                    </Text>
                    {plot.needs_water && <span className={styles.waterIcon}>💧</span>}
                    {plot.is_mature && <span className={styles.matureIcon}>✨</span>}
                  </div>
                </>
              ) : (
                <span className={styles.emptyText}>点击种植</span>
              )}
            </div>
          ))}
        </div>
      )}

      <Modal
        title="选择作物"
        open={plantModalVisible}
        onCancel={() => setPlantModalVisible(false)}
        footer={null}
        width={450}
      >
        <div className={styles.cropList}>
          {crops.map((crop) => {
            const canAfford = (state.player?.gold ?? 0) >= crop.price;
            return (
              <div
                key={crop.name}
                className={`${styles.cropItem} ${!canAfford ? styles.cropDisabled : ''}`}
                onClick={() => canAfford && handlePlant(crop)}
              >
                <span className={styles.cropEmojiLarge}>{crop.emoji}</span>
                <div className={styles.cropInfo}>
                  <Text strong>{crop.name}</Text>
                  <Text type="secondary">
                    💰 种子: {crop.price} | 📈 售价: {crop.sell_price}
                  </Text>
                  <Text type="secondary">
                    🌱 生长: {crop.grow_days}天
                  </Text>
                </div>
                {!canAfford && (
                  <Text type="secondary" className={styles.noGold}>
                    金币不足
                  </Text>
                )}
              </div>
            );
          })}
        </div>
      </Modal>
    </div>
  );
};

export default Farm;
