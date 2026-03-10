import React, { createContext, useContext, useReducer, useEffect, ReactNode } from 'react';
import type { Player, GameState, Plot, Crop, GameStatus, Achievement, PlayerStats } from '../types';
import { apiClient } from '../api/client';

interface GameStateData {
  player: Player | null;
  gameState: GameState | null;
  plots: Plot[];
  crops: Crop[];
  achievements: Achievement[];
  playerStats: PlayerStats | null;
  status: GameStatus;
  isLoading: boolean;
  error: string | null;
  isInitialized: boolean;
}

type GameAction =
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'SET_GAME_STATE'; payload: GameState | null }
  | { type: 'SET_PLAYER'; payload: Player | null }
  | { type: 'SET_PLOTS'; payload: Plot[] }
  | { type: 'SET_CROPS'; payload: Crop[] }
  | { type: 'SET_ACHIEVEMENTS'; payload: Achievement[] }
  | { type: 'SET_PLAYER_STATS'; payload: PlayerStats | null }
  | { type: 'SET_STATUS'; payload: GameStatus }
  | { type: 'UPDATE_GOLD'; payload: number }
  | { type: 'UPDATE_PLOT'; payload: { row: number; col: number; plot: Plot } }
  | { type: 'SET_INITIALIZED'; payload: boolean }
  | { type: 'RESET' };

const initialState: GameStateData = {
  player: null,
  gameState: null,
  plots: [],
  crops: [],
  achievements: [],
  playerStats: null,
  status: { has_game: false, is_running: false, season: '春天', day: 1, year: 1, weather: '晴天' },
  isLoading: false,
  error: null,
  isInitialized: false,
};

function gameReducer(state: GameStateData, action: GameAction): GameStateData {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload, isLoading: false };
    case 'SET_GAME_STATE':
      return { ...state, gameState: action.payload };
    case 'SET_PLAYER':
      return { ...state, player: action.payload };
    case 'SET_PLOTS':
      return { ...state, plots: action.payload };
    case 'SET_CROPS':
      return { ...state, crops: action.payload };
    case 'SET_ACHIEVEMENTS':
      return { ...state, achievements: action.payload };
    case 'SET_PLAYER_STATS':
      return { ...state, playerStats: action.payload };
    case 'SET_STATUS':
      return { ...state, status: action.payload };
    case 'UPDATE_GOLD':
      if (state.player) {
        return { ...state, player: { ...state.player, gold: action.payload } };
      }
      if (state.gameState) {
        return { ...state, gameState: { ...state.gameState, gold: action.payload } };
      }
      return state;
    case 'UPDATE_PLOT':
      const updatedPlots = state.plots.map((p) =>
        p.row === action.payload.row && p.col === action.payload.col ? action.payload.plot : p
      );
      return { ...state, plots: updatedPlots };
    case 'SET_INITIALIZED':
      return { ...state, isInitialized: action.payload };
    case 'RESET':
      return { ...initialState, isInitialized: true };
    default:
      return state;
  }
}

interface GameContextType {
  state: GameStateData;
  dispatch: React.Dispatch<GameAction>;
  createGame: (playerName: string) => Promise<boolean>;
  loadGameData: () => Promise<void>;
  plantCrop: (row: number, col: number, cropName: string) => Promise<boolean>;
  waterCrop: (row: number, col: number) => Promise<boolean>;
  harvestCrop: (row: number, col: number) => Promise<boolean>;
  advanceDay: () => Promise<boolean>;
  saveGame: (saveName: string) => Promise<boolean>;
  loadGame: (saveName: string) => Promise<boolean>;
}

const GameContext = createContext<GameContextType | null>(null);

export function GameProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(gameReducer, initialState);

  const createGame = async (playerName: string): Promise<boolean> => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const result = await apiClient.createGame(playerName);
      if (result.success && result.state) {
        dispatch({ type: 'SET_GAME_STATE', payload: result.state });
        dispatch({
          type: 'SET_PLAYER',
          payload: {
            name: result.state.player_name,
            level: result.state.level,
            exp: result.state.exp,
            gold: result.state.gold,
            stamina: result.state.stamina,
            max_stamina: result.state.max_stamina,
          },
        });
        dispatch({
          type: 'SET_STATUS',
          payload: {
            has_game: true,
            is_running: true,
            season: result.state.season,
            day: result.state.day,
            year: result.state.year,
            weather: result.state.weather,
          },
        });
        await loadGameData();
        return true;
      }
      dispatch({ type: 'SET_ERROR', payload: result.message || '创建游戏失败' });
      return false;
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: '创建游戏失败，请稍后重试' });
      return false;
    }
  };

  const loadGameData = async (): Promise<void> => {
    try {
      const [plots, crops, stats, achievements, status] = await Promise.all([
        apiClient.getPlots(),
        apiClient.getCrops(),
        apiClient.getPlayerStats().catch(() => null),
        apiClient.getAchievements().catch(() => []),
        apiClient.getGameStatus(),
      ]);

      dispatch({ type: 'SET_PLOTS', payload: plots as unknown as Plot[] });
      dispatch({ type: 'SET_CROPS', payload: crops });
      dispatch({ type: 'SET_PLAYER_STATS', payload: stats });
      dispatch({ type: 'SET_ACHIEVEMENTS', payload: achievements });
      dispatch({ type: 'SET_STATUS', payload: status });
    } catch (error) {
      console.error('加载游戏数据失败:', error);
    }
  };

  const plantCrop = async (row: number, col: number, cropName: string): Promise<boolean> => {
    try {
      const result = await apiClient.plantCrop(row, col, cropName);
      if (result.success) {
        dispatch({ type: 'UPDATE_GOLD', payload: result.remaining_gold });
        await loadGameData();
        return true;
      }
      dispatch({ type: 'SET_ERROR', payload: result.message });
      return false;
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: '种植失败' });
      return false;
    }
  };

  const waterCrop = async (row: number, col: number): Promise<boolean> => {
    try {
      const result = await apiClient.waterCrop(row, col);
      if (result.success) {
        await loadGameData();
        return true;
      }
      dispatch({ type: 'SET_ERROR', payload: result.message });
      return false;
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: '浇水失败' });
      return false;
    }
  };

  const harvestCrop = async (row: number, col: number): Promise<boolean> => {
    try {
      const result = await apiClient.harvestCrop(row, col);
      if (result.success) {
        dispatch({ type: 'UPDATE_GOLD', payload: result.remaining_gold });
        await loadGameData();
        return true;
      }
      dispatch({ type: 'SET_ERROR', payload: result.message });
      return false;
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: '收获失败' });
      return false;
    }
  };

  const advanceDay = async (): Promise<boolean> => {
    try {
      const result = await apiClient.advanceDay();
      if (result.success) {
        dispatch({ type: 'SET_GAME_STATE', payload: result.new_state });
        await loadGameData();
        return true;
      }
      dispatch({ type: 'SET_ERROR', payload: result.message });
      return false;
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: '时间推进失败' });
      return false;
    }
  };

  const saveGame = async (saveName: string): Promise<boolean> => {
    try {
      const result = await apiClient.saveGame(saveName);
      if (!result.success) {
        dispatch({ type: 'SET_ERROR', payload: result.message });
        return false;
      }
      return true;
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: '保存游戏失败' });
      return false;
    }
  };

  const loadGame = async (saveName: string): Promise<boolean> => {
    try {
      const result = await apiClient.loadGame(saveName);
      if (result.success && result.state) {
        dispatch({ type: 'SET_GAME_STATE', payload: result.state });
        dispatch({
          type: 'SET_PLAYER',
          payload: {
            name: result.state.player_name,
            level: result.state.level,
            exp: result.state.exp,
            gold: result.state.gold,
            stamina: result.state.stamina,
            max_stamina: result.state.max_stamina,
          },
        });
        await loadGameData();
        return true;
      }
      dispatch({ type: 'SET_ERROR', payload: result.message || '加载游戏失败' });
      return false;
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: '加载游戏失败' });
      return false;
    }
  };

  useEffect(() => {
    const init = async () => {
      try {
        const status = await apiClient.getGameStatus();
        dispatch({ type: 'SET_STATUS', payload: status });
        if (status.has_game) {
          await loadGameData();
        }
      } catch (error) {
        console.error('初始化失败:', error);
      } finally {
        dispatch({ type: 'SET_INITIALIZED', payload: true });
      }
    };
    init();
  }, []);

  return (
    <GameContext.Provider
      value={{
        state,
        dispatch,
        createGame,
        loadGameData,
        plantCrop,
        waterCrop,
        harvestCrop,
        advanceDay,
        saveGame,
        loadGame,
      }}
    >
      {children}
    </GameContext.Provider>
  );
}

export function useGame() {
  const context = useContext(GameContext);
  if (!context) {
    throw new Error('useGame must be used within a GameProvider');
  }
  return context;
}
