export interface Player {
  name: string;
  level: number;
  exp: number;
  gold: number;
  stamina: number;
  max_stamina: number;
}

export interface GameState {
  season: string;
  day: number;
  year: number;
  weather: string;
  player_name: string;
  gold: number;
  level: number;
  exp: number;
  stamina: number;
  max_stamina: number;
  plot_size: number;
}

export interface Plot {
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

export interface Crop {
  id: string;
  name: string;
  emoji: string;
  seed_price: number;
  sell_price: number;
  grow_days: number;
  season: string;
  description: string;
}

export interface Achievement {
  id: string;
  name: string;
  description: string;
  unlocked: boolean;
  progress: number;
  target: number;
  reward_text: string;
}

export interface PlantAdvice {
  success: boolean;
  recommended_crop: string;
  reason: string;
  analysis: CropAnalysis[];
}

export interface CropAnalysis {
  name: string;
  seed_price: number;
  sell_price: number;
  grow_days: number;
  water_needed: number;
  can_plant: boolean;
  max_seeds: number;
  profit_per_crop: number;
  profit_rate: number;
  profit_per_day: number;
  total_profit: number;
}

export interface GameStatus {
  has_game: boolean;
  is_running: boolean;
  season: string;
  day: number;
  year: number;
  weather: string;
}

export interface ApiResponse<T = unknown> {
  success: boolean;
  message?: string;
  data?: T;
}

export interface FarmPlotResponse {
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

export interface PlantResponse {
  success: boolean;
  message: string;
  remaining_gold: number;
}

export interface WaterResponse {
  success: boolean;
  message: string;
}

export interface HarvestResponse {
  success: boolean;
  message: string;
  earned_gold: number;
  remaining_gold: number;
}

export interface AdvanceDayResponse {
  success: boolean;
  message: string;
  crops_grown: number;
  crops_matured: number;
  events: string[];
  new_state: GameState;
}

export interface SaveLoadResponse {
  success: boolean;
  message: string;
}

export interface SavesListResponse {
  saves: string[];
  count: number;
}

export interface PlayerStats {
  total_plots: number;
  planted_plots: number;
  mature_plots: number;
  empty_plots: number;
  needs_water: number;
  gold: number;
  level: number;
  exp: number;
}

export interface AIChatRequest {
  message: string;
}

export interface AIChatResponse {
  response: string;
  suggestions: string[];
}

export interface ShopItem {
  id: string;
  name: string;
  emoji: string;
  category: string;
  price: number;
  description: string;
  effect?: Record<string, unknown>;
}

export interface ShopHistoryItem {
  item_id: string;
  quantity: number;
  total_price: number;
}

export interface AIConfig {
  provider: string;
  model: string;
  base_url: string;
  temperature: number;
  has_api_key: boolean;
}

export interface AIConfigRequest {
  provider: string;
  api_key?: string;
  model: string;
  base_url: string;
  temperature: number;
}
