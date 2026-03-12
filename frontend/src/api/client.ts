import axios, { type AxiosInstance, AxiosError } from 'axios';
import type {
  Player,
  GameState,
  Crop,
  Achievement,
  PlantAdvice,
  GameStatus,
  FarmPlotResponse,
  PlantResponse,
  WaterResponse,
  HarvestResponse,
  AdvanceDayResponse,
  SaveLoadResponse,
  SavesListResponse,
  PlayerStats,
  AIChatResponse,
  ShopItem,
  ShopHistoryItem,
  AIConfig,
  AIConfigRequest,
} from '../types';

const BASE_URL = import.meta.env.VITE_API_URL || '/api';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: BASE_URL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        console.error('API Error:', error.message);
        return Promise.reject(error);
      }
    );
  }

  // ========== 玩家 API ==========

  async createGame(playerName: string, difficulty: string = 'normal'): Promise<{ success: boolean; message?: string; state?: GameState }> {
    const response = await this.client.post('/player/create', { player_name: playerName, difficulty });
    return response.data;
  }

  async getPlayerInfo(): Promise<Player> {
    const response = await this.client.get<Player>('/player/info');
    return response.data;
  }

  async getPlayerStats(): Promise<PlayerStats> {
    const response = await this.client.get<PlayerStats>('/player/stats');
    return response.data;
  }

  async getAchievements(): Promise<Achievement[]> {
    const response = await this.client.get<Achievement[]>('/player/achievements');
    return response.data;
  }

  async addGold(amount: number): Promise<{ success: boolean; gold: number }> {
    const response = await this.client.post('/player/add_gold', null, { params: { amount } });
    return response.data;
  }

  // ========== 农场 API ==========

  async getPlots(): Promise<FarmPlotResponse[]> {
    const response = await this.client.get<FarmPlotResponse[]>('/farm/plots');
    return response.data;
  }

  async getCrops(): Promise<Crop[]> {
    const response = await this.client.get<Crop[]>('/farm/crops');
    return response.data;
  }

  async getTimeStatus(): Promise<{
    year: number;
    day: number;
    season: string;
    weather: string;
    tomorrow_weather: string | null;
    date_string: string;
    season_progress: number;
    year_progress: number;
    total_days: number;
  }> {
    const response = await this.client.get('/farm/time');
    return response.data;
  }

  async plantCrop(row: number, col: number, cropName: string): Promise<PlantResponse> {
    const response = await this.client.post<PlantResponse>('/farm/plant', {
      row,
      col,
      crop_name: cropName,
    });
    return response.data;
  }

  async waterCrop(row: number, col: number): Promise<WaterResponse> {
    const response = await this.client.post<WaterResponse>('/farm/water', {
      row,
      col,
    });
    return response.data;
  }

  async harvestCrop(row: number, col: number): Promise<HarvestResponse> {
    const response = await this.client.post<HarvestResponse>('/farm/harvest', {
      row,
      col,
    });
    return response.data;
  }

  async clearPlot(row: number, col: number): Promise<{ success: boolean; message: string }> {
    const response = await this.client.post('/farm/clear', { row, col });
    return response.data;
  }

  // ========== 游戏控制 API ==========

  async getGameStatus(): Promise<GameStatus> {
    const response = await this.client.get<GameStatus>('/game/status');
    return response.data;
  }

  async advanceDay(): Promise<AdvanceDayResponse> {
    const response = await this.client.post<AdvanceDayResponse>('/game/advance_day');
    return response.data;
  }

  async saveGame(saveName: string): Promise<SaveLoadResponse> {
    const response = await this.client.post<SaveLoadResponse>('/game/save', {
      save_name: saveName,
    });
    return response.data;
  }

  async loadGame(saveName: string): Promise<SaveLoadResponse & { state?: GameState }> {
    const response = await this.client.post('/game/load', { save_name: saveName });
    return response.data;
  }

  async getSaves(): Promise<SavesListResponse> {
    const response = await this.client.get<SavesListResponse>('/game/saves');
    return response.data;
  }

  async deleteSave(saveName: string): Promise<SaveLoadResponse> {
    const response = await this.client.delete(`/game/save/${saveName}`);
    return response.data;
  }

  async resetGame(): Promise<SaveLoadResponse> {
    const response = await this.client.post<SaveLoadResponse>('/game/reset');
    return response.data;
  }

  async startNewGamePlus(): Promise<{ success: boolean; message: string; game_number: number }> {
    const response = await this.client.post('/game/new_game_plus');
    return response.data;
  }

  async getGameInfo(): Promise<{
    has_game: boolean;
    difficulty?: string;
    game_number?: number;
    total_games_played?: number;
  }> {
    const response = await this.client.get('/game/game_info');
    return response.data;
  }

  // ========== AI API ==========

  async chatWithAI(message: string): Promise<AIChatResponse> {
    const response = await this.client.post<AIChatResponse>('/ai/chat', { message });
    return response.data;
  }

  async getPlantingAdvice(): Promise<{ message: string; advice: PlantAdvice[] }> {
    const response = await this.client.get('/ai/advice/planting');
    return response.data;
  }

  async analyzeFarm(): Promise<{ score: number; message: string; suggestions?: string[] }> {
    const response = await this.client.get('/ai/analysis/farm');
    return response.data;
  }

  async getKnowledge(topic: string): Promise<{ title: string; content: string }> {
    const response = await this.client.get(`/ai/knowledge/${topic}`);
    return response.data;
  }

  // ========== 商店 API ==========

  async getShopItems(): Promise<ShopItem[]> {
    const response = await this.client.get('/shop/items');
    return response.data;
  }

  async buyItem(itemId: string, quantity: number = 1): Promise<{ success: boolean; message: string; remaining_gold: number }> {
    const response = await this.client.post('/shop/buy', { item_id: itemId, quantity });
    return response.data;
  }

  async getShopHistory(): Promise<{ history: ShopHistoryItem[] }> {
    const response = await this.client.get('/shop/history');
    return response.data;
  }

  // ========== AI 配置 API ==========

  async getAIConfig(): Promise<AIConfig> {
    const response = await this.client.get('/ai/config');
    return response.data;
  }

  async setAIConfig(config: AIConfigRequest): Promise<{ success: boolean; message: string; config: AIConfig }> {
    const response = await this.client.post('/ai/config', config);
    return response.data;
  }

  async testAIConnection(): Promise<{ success: boolean; message: string; response?: string }> {
    const response = await this.client.post('/ai/config/test');
    return response.data;
  }

  // ========== 健康检查 ==========

  async healthCheck(): Promise<{ status: string; version: string }> {
    const response = await this.client.get('/health');
    return response.data;
  }
}

export const apiClient = new ApiClient();
export default apiClient;
