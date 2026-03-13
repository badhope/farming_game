import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import {
  Player,
  Identity,
  IDENTITIES,
  Company,
  STRATEGIES,
  Strategy,
  SHOP_ITEMS,
  ShopItem,
  CITIES,
  City,
  createPlayer,
  work,
  study,
  rest,
  createCompany,
  dailyOperation,
  buyItem,
  getMarketIntelligence,
  checkClassPromotion,
  calculateNetWorth,
  formatMoney,
} from '../game/gameLogic';

interface GameState {
  player: Player | null;
  selectedIdentity: Identity | null;
  company: Company | null;
  strategies: Strategy[];
  currentCity: City | null;
  gameStarted: boolean;
  gameEnded: boolean;
  endReason?: string;
}

interface GameContextType extends GameState {
  selectIdentity: (identity: Identity) => void;
  startGame: (playerName?: string) => void;
  handleWork: () => number;
  handleStudy: () => void;
  handleRest: () => number;
  handleCreateCompany: (name: string, type: string) => void;
  handleDailyOperation: () => number;
  handleBuyItem: (item: ShopItem) => void;
  selectStrategy: (strategy: Strategy) => void;
  changeCity: (city: City) => void;
  saveGame: () => void;
  loadGame: () => boolean;
  resetGame: () => void;
}

const GameContext = createContext<GameContextType | undefined>(undefined);

const STORAGE_KEY = 'chinese_millionaire_save';

export function GameProvider({ children }: { children: ReactNode }) {
  const [gameState, setGameState] = useState<GameState>({
    player: null,
    selectedIdentity: null,
    company: null,
    strategies: [],
    currentCity: CITIES[0], // 默认广州
    gameStarted: false,
    gameEnded: false,
  });

  // 选择身份
  const selectIdentity = useCallback((identity: Identity) => {
    setGameState(prev => ({ ...prev, selectedIdentity: identity }));
  }, []);

  // 开始游戏
  const startGame = useCallback((playerName: string = '玩家') => {
    if (!gameState.selectedIdentity) return;
    
    const player = createPlayer(gameState.selectedIdentity, playerName);
    setGameState(prev => ({
      ...prev,
      player,
      gameStarted: true,
      gameEnded: false,
    }));
  }, [gameState.selectedIdentity]);

  // 工作
  const handleWork = useCallback(() => {
    if (!gameState.player) return 0;
    
    const { income, newPlayer } = work(gameState.player);
    const promotedPlayer = checkClassPromotion(newPlayer);
    
    setGameState(prev => ({
      ...prev,
      player: promotedPlayer,
    }));
    
    return income;
  }, [gameState.player]);

  // 学习
  const handleStudy = useCallback(() => {
    if (!gameState.player) return;
    
    const newPlayer = study(gameState.player);
    const promotedPlayer = checkClassPromotion(newPlayer);
    
    setGameState(prev => ({
      ...prev,
      player: promotedPlayer,
    }));
  }, [gameState.player]);

  // 休息
  const handleRest = useCallback(() => {
    if (!gameState.player) return 0;
    
    const { recovered, newPlayer } = rest(gameState.player);
    const promotedPlayer = checkClassPromotion(newPlayer);
    
    setGameState(prev => ({
      ...prev,
      player: promotedPlayer,
    }));
    
    return recovered;
  }, [gameState.player]);

  // 创建公司
  const handleCreateCompany = useCallback((name: string, type: string) => {
    if (!gameState.player) return;
    
    const company = createCompany(name, type, gameState.player);
    const newPlayer = {
      ...gameState.player,
      company,
      cash: gameState.player.cash - 50000, // 创建公司成本
    };
    
    setGameState(prev => ({
      ...prev,
      player: newPlayer,
      company,
    }));
  }, [gameState.player]);

  // 公司日常经营
  const handleDailyOperation = useCallback(() => {
    if (!gameState.company) return 0;
    
    const profit = dailyOperation(gameState.company);
    const newPlayer = gameState.player 
      ? { ...gameState.player, cash: gameState.player.cash + profit }
      : null;
    
    setGameState(prev => ({
      ...prev,
      player: newPlayer,
    }));
    
    return profit;
  }, [gameState.company, gameState.player]);

  // 购买物品
  const handleBuyItem = useCallback((item: ShopItem) => {
    if (!gameState.player) return;
    
    const newPlayer = buyItem(gameState.player, item);
    const promotedPlayer = checkClassPromotion(newPlayer);
    
    setGameState(prev => ({
      ...prev,
      player: promotedPlayer,
    }));
  }, [gameState.player]);

  // 选择策略
  const selectStrategy = useCallback((strategy: Strategy) => {
    setGameState(prev => ({
      ...prev,
      strategies: [...prev.strategies, strategy],
    }));
  }, []);

  // 切换城市
  const changeCity = useCallback((city: City) => {
    setGameState(prev => ({ ...prev, currentCity: city }));
  }, []);

  // 保存游戏
  const saveGame = useCallback(() => {
    if (!gameState.player) return;
    
    const saveData = {
      player: gameState.player,
      company: gameState.company,
      strategies: gameState.strategies,
      currentCity: gameState.currentCity,
      selectedIdentity: gameState.selectedIdentity,
      timestamp: new Date().toISOString(),
    };
    
    localStorage.setItem(STORAGE_KEY, JSON.stringify(saveData));
  }, [gameState]);

  // 读取游戏
  const loadGame = useCallback(() => {
    const saveData = localStorage.getItem(STORAGE_KEY);
    if (!saveData) return false;
    
    try {
      const parsed = JSON.parse(saveData);
      setGameState({
        player: parsed.player,
        company: parsed.company,
        strategies: parsed.strategies || [],
        currentCity: parsed.currentCity || CITIES[0],
        selectedIdentity: parsed.selectedIdentity,
        gameStarted: true,
        gameEnded: false,
      });
      return true;
    } catch (e) {
      console.error('读取存档失败:', e);
      return false;
    }
  }, []);

  // 重置游戏
  const resetGame = useCallback(() => {
    localStorage.removeItem(STORAGE_KEY);
    setGameState({
      player: null,
      selectedIdentity: null,
      company: null,
      strategies: [],
      currentCity: CITIES[0],
      gameStarted: false,
      gameEnded: false,
    });
  }, []);

  // 检查游戏结束
  React.useEffect(() => {
    if (!gameState.player) return;
    
    const netWorth = calculateNetWorth(gameState.player);
    
    if (gameState.player.health <= 0) {
      setGameState(prev => ({
        ...prev,
        gameEnded: true,
        endReason: '健康崩溃',
      }));
    } else if (netWorth < 0) {
      setGameState(prev => ({
        ...prev,
        gameEnded: true,
        endReason: '破产',
      }));
    } else if (gameState.player.corruption && gameState.player.corruption >= 100) {
      setGameState(prev => ({
        ...prev,
        gameEnded: true,
        endReason: '入狱',
      }));
    }
  }, [gameState.player]);

  const value: GameContextType = {
    ...gameState,
    selectIdentity,
    startGame,
    handleWork,
    handleStudy,
    handleRest,
    handleCreateCompany,
    handleDailyOperation,
    handleBuyItem,
    selectStrategy,
    changeCity,
    saveGame,
    loadGame,
    resetGame,
  };

  return <GameContext.Provider value={value}>{children}</GameContext.Provider>;
}

export function useGame() {
  const context = useContext(GameContext);
  if (context === undefined) {
    throw new Error('useGame must be used within a GameProvider');
  }
  return context;
}
