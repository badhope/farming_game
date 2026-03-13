/**
 * 中国百万富翁 - 游戏核心逻辑
 * 基于 Python 版本移植
 */

// ============ 身份系统 ============
export interface Identity {
  name: string;
  description: string;
  startMoney: number;
  connections: number;
  education: string;
  skills: string[];
  bonus: Record<string, number>;
  bonusDescription: string;
}

export const IDENTITIES: Identity[] = [
  {
    name: '农民',
    description: '农村起家，农业相关加成',
    startMoney: 8000,
    connections: 20,
    education: '初中',
    skills: ['精通农业', '吃苦耐劳'],
    bonus: {
      agriculture_cost: 0.7,
      crop_yield: 1.25,
    },
    bonusDescription: '农业成本 -30%，产量 +25%',
  },
  {
    name: '小镇青年',
    description: '县城创业，零售业优势',
    startMoney: 25000,
    connections: 35,
    education: '高中',
    skills: ['精打细算', '人情世故'],
    bonus: {
      rent_discount: 0.6,
      loan_approve: 1.3,
    },
    bonusDescription: '租金 -40%，小额贷款更容易',
  },
  {
    name: '大学生',
    description: '科技创业，互联网行业',
    startMoney: 50000,
    connections: 25,
    education: '本科',
    skills: ['创新思维', '学习能力'],
    bonus: {
      tech_startup: 0.5,
      funding_rate: 1.4,
    },
    bonusDescription: '科技创业门槛 -50%，融资成功率 +40%',
  },
  {
    name: '海归',
    description: '国际贸易，金融投资',
    startMoney: 200000,
    connections: 15,
    education: '硕士',
    skills: ['国际视野', '英语流利'],
    bonus: {
      tariff_discount: 0.7,
      forex_fee: 0.5,
    },
    bonusDescription: '国际贸易关税 -30%，外汇手续费 -50%',
  },
  {
    name: '个体户',
    description: '批发市场，制造业',
    startMoney: 80000,
    connections: 50,
    education: '高中',
    skills: ['生意头脑', '供应链'],
    bonus: {
      wholesale_discount: 0.75,
      cash_flow: 1.3,
    },
    bonusDescription: '批发价 -25%，现金流 +30%',
  },
  {
    name: '官二代',
    description: '人脉优势，政策敏感',
    startMoney: 150000,
    connections: 80,
    education: '本科',
    skills: ['人脉通天', '政策敏感'],
    bonus: {
      gov_project: 1.6,
      loan_approve: 1.4,
    },
    bonusDescription: '政府项目优势，贷款审批更容易（但有腐败风险）',
  },
];

// ============ 社会阶层 ============
export interface SocialClass {
  level: number;
  name: string;
  minNetWorth: number;
  unlocks: string[];
}

export const SOCIAL_CLASSES: SocialClass[] = [
  { level: 1, name: '赤贫阶层', minNetWorth: 0, unlocks: ['路边摊', '打工'] },
  { level: 2, name: '底层劳工', minNetWorth: 10000, unlocks: ['小生意', '夜市摆摊'] },
  { level: 3, name: '小商贩', minNetWorth: 50000, unlocks: ['开小店', '倒买倒卖'] },
  { level: 4, name: '小老板', minNetWorth: 200000, unlocks: ['开公司', '银行贷款'] },
  { level: 5, name: '中产阶层', minNetWorth: 1000000, unlocks: ['房地产', '股票基金'] },
  { level: 6, name: '富豪阶层', minNetWorth: 5000000, unlocks: ['并购重组', '私募股权'] },
  { level: 7, name: '大资本家', minNetWorth: 50000000, unlocks: ['跨国贸易', '金融杠杆'] },
  { level: 8, name: '顶级富豪', minNetWorth: 500000000, unlocks: ['垄断行业', '影响政策'] },
];

// ============ 玩家接口 ============
export interface Player {
  name: string;
  identity: Identity;
  cash: number;
  realEstate: number;
  vehicles: number;
  investments: number;
  loans: number;
  stamina: number; // 体力 0-100
  mood: number; // 心情 0-100
  health: number; // 健康 0-100
  reputation: number; // 声誉 0-100
  connections: number; // 人脉 0-100
  skills: string[];
  classLevel: number;
  currentClass: string;
  day: number;
  company?: Company;
  corruption?: number; // 腐败值（官二代专属）
}

// ============ 公司接口 ============
export interface Company {
  name: string;
  type: string;
  level: number;
  employees: number;
  monthlyRevenue: number;
  monthlyCost: number;
  monthlyProfit: number;
}

// ============ 策略接口 ============
export interface Strategy {
  name: string;
  type: string;
  effect: string;
  bonus: Record<string, number>;
  unlockRequirement: string;
  description: string;
}

export const STRATEGIES: Strategy[] = [
  // 商业策略
  {
    name: '稳扎稳打',
    type: '商业',
    effect: '利润稳定，风险低，增长慢',
    bonus: { profit: 1.0, risk: 0.5, growth: 0.8 },
    unlockRequirement: '无',
    description: '老老实实做生意，薄利多销',
  },
  {
    name: '薄利多销',
    type: '商业',
    effect: '销量大，单利薄，总收益稳定',
    bonus: { sales: 1.5, profit_margin: 0.7 },
    unlockRequirement: '小老板',
    description: '量大管饱，走量取胜',
  },
  {
    name: '高端定位',
    type: '商业',
    effect: '单利高，销量小，客户群体高端',
    bonus: { profit_margin: 2.0, sales: 0.6 },
    unlockRequirement: '中产阶层',
    description: '只做高端客户，三年不开张，开张吃三年',
  },
  {
    name: '垄断经营',
    type: '商业',
    effect: '超高利润，高风险，需要关系网',
    bonus: { profit: 3.0, risk: 0.9 },
    unlockRequirement: '大资本家',
    description: '这个行业的规矩，我说了算',
  },
  
  // 投资策略
  {
    name: '保守理财',
    type: '投资',
    effect: '年化 5%，稳赚不赔',
    bonus: { return: 0.05, risk: 0 },
    unlockRequirement: '无',
    description: '银行理财，保本第一',
  },
  {
    name: '股票投机',
    type: '投资',
    effect: '高风险高回报，可能翻倍也可能亏光',
    bonus: { return: 0.5, risk: 0.8 },
    unlockRequirement: '小老板',
    description: '搏一搏，单车变摩托',
  },
  {
    name: '房地产投资',
    type: '投资',
    effect: '稳定增值，抗通胀',
    bonus: { return: 0.15, risk: 0.2 },
    unlockRequirement: '中产阶层',
    description: '买房致富，永远的神',
  },
  {
    name: '风险投资',
    type: '投资',
    effect: '极高回报，极高失败率',
    bonus: { return: 2.0, risk: 0.95 },
    unlockRequirement: '富豪阶层',
    description: '投资 10 个项目，成 1 个就赚翻',
  },
  
  // 社交策略
  {
    name: '低调做人',
    type: '社交',
    effect: '减少麻烦，人脉增长慢',
    bonus: { trouble: -0.5, connections_growth: 0.5 },
    unlockRequirement: '无',
    description: '闷声发大财',
  },
  {
    name: '高调炫富',
    type: '社交',
    effect: '吸引机会，也吸引麻烦',
    bonus: { opportunity: 1.5, trouble: 1.5 },
    unlockRequirement: '小老板',
    description: '让所有人都知道我有钱',
  },
  {
    name: '广结善缘',
    type: '社交',
    effect: '人脉快速增长',
    bonus: { connections_growth: 2.0 },
    unlockRequirement: '中产阶层',
    description: '朋友多了路好走',
  },
  {
    name: '攀附权贵',
    type: '社交',
    effect: '快速晋升，但有风险',
    bonus: { class_growth: 1.5, corruption: 0.1 },
    unlockRequirement: '富豪阶层',
    description: '抱大腿，上位快',
  },
  
  // 政治策略
  {
    name: '合法经营',
    type: '政治',
    effect: '安全，但发展慢',
    bonus: { safety: 1.0, growth: 0.7 },
    unlockRequirement: '无',
    description: '遵纪守法，安心睡觉',
  },
  {
    name: '官商勾结',
    type: '政治',
    effect: '快速发展，腐败风险',
    bonus: { growth: 2.0, corruption: 0.2 },
    unlockRequirement: '小老板',
    description: '朝中有人好办事',
  },
  {
    name: '政商旋转门',
    type: '政治',
    effect: '左右逢源，需要高智商',
    bonus: { growth: 2.5, safety: 0.8 },
    unlockRequirement: '大资本家',
    description: '我当过官，也做过商',
  },
  
  // 灰色策略
  {
    name: '偷税漏税',
    type: '灰色',
    effect: '短期暴利，发现就坐牢',
    bonus: { profit: 1.5, jail_risk: 0.3 },
    unlockRequirement: '小老板',
    description: '省下的就是赚到的',
  },
  {
    name: '假冒伪劣',
    type: '灰色',
    effect: '成本大降，风险极高',
    bonus: { cost: 0.3, jail_risk: 0.5 },
    unlockRequirement: '中产阶层',
    description: '反正消费者看不出来',
  },
  {
    name: '内幕交易',
    type: '灰色',
    effect: '稳赚不赔，发现就坐牢',
    bonus: { profit: 5.0, jail_risk: 0.8 },
    unlockRequirement: '大资本家',
    description: '利用内幕消息炒股',
  },
];

// ============ 城市系统 ============
export interface City {
  name: string;
  type: string;
  industry: string;
  costMultiplier: number;
  bonuses: Record<string, number>;
}

export const CITIES: City[] = [
  {
    name: '广州',
    type: '千年商都',
    industry: '贸易 + 餐饮',
    costMultiplier: 1.2,
    bonuses: { trade: 1.3, restaurant: 1.5 },
  },
  {
    name: '深圳',
    type: '科技之都',
    industry: '科技 + 金融',
    costMultiplier: 1.5,
    bonuses: { tech: 1.5, finance: 1.3 },
  },
  {
    name: '北京',
    type: '政治中心',
    industry: '政府 + 文化',
    costMultiplier: 1.8,
    bonuses: { government: 1.5, culture: 1.3 },
  },
  {
    name: '上海',
    type: '金融中心',
    industry: '金融 + 奢侈品',
    costMultiplier: 2.0,
    bonuses: { finance: 1.5, luxury: 1.4 },
  },
];

// ============ 购物系统 ============
export interface ShopItem {
  name: string;
  price: number;
  category: string;
  effect: string;
  effectValue: number;
}

export const SHOP_ITEMS: ShopItem[] = [
  // 生活消费
  { name: '便当', price: 15, category: '生活消费', effect: '体力', effectValue: 5 },
  { name: '饮料', price: 5, category: '生活消费', effect: '体力', effectValue: 2 },
  { name: '零食', price: 10, category: '生活消费', effect: '心情', effectValue: 3 },
  { name: '快餐', price: 30, category: '生活消费', effect: '体力', effectValue: 10 },
  { name: '保健品', price: 200, category: '生活消费', effect: '健康', effectValue: 5 },
  { name: '健身卡', price: 2000, category: '生活消费', effect: '健康', effectValue: 20 },
  { name: '体检套餐', price: 1000, category: '生活消费', effect: '健康', effectValue: 10 },
  { name: '培训课程', price: 5000, category: '生活消费', effect: '技能', effectValue: 10 },
  { name: '人脉活动', price: 10000, category: '生活消费', effect: '人脉', effectValue: 20 },
  
  // 奢侈品
  { name: '名牌包', price: 50000, category: '奢侈品', effect: '心情', effectValue: 30 },
  { name: '手表', price: 100000, category: '奢侈品', effect: '声誉', effectValue: 20 },
  { name: '豪车', price: 1000000, category: '奢侈品', effect: '声誉', effectValue: 50 },
  { name: '豪宅', price: 10000000, category: '奢侈品', effect: '声誉', effectValue: 100 },
  { name: '私人飞机', price: 100000000, category: '奢侈品', effect: '声誉', effectValue: 500 },
];

// ============ 工具函数 ============
export function formatMoney(amount: number): string {
  return `¥${amount.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

export function formatNumber(num: number): string {
  return num.toLocaleString('zh-CN');
}

export function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value));
}

export function calculateNetWorth(player: Player): number {
  return player.cash + player.realEstate + player.vehicles + player.investments - player.loans;
}

export function checkClassPromotion(player: Player): Player {
  const netWorth = calculateNetWorth(player);
  
  // 从高级到低级检查
  for (let i = SOCIAL_CLASSES.length - 1; i >= 0; i--) {
    const classInfo = SOCIAL_CLASSES[i];
    if (netWorth >= classInfo.minNetWorth) {
      if (player.classLevel < classInfo.level) {
        return {
          ...player,
          classLevel: classInfo.level,
          currentClass: classInfo.name,
        };
      }
      break;
    }
  }
  
  return player;
}

// ============ 游戏逻辑函数 ============
export function createPlayer(identity: Identity, name: string = '玩家'): Player {
  return {
    name,
    identity,
    cash: identity.startMoney,
    realEstate: 0,
    vehicles: 0,
    investments: 0,
    loans: 0,
    stamina: 100,
    mood: 80,
    health: 100,
    reputation: 50,
    connections: identity.connections,
    skills: [...identity.skills],
    classLevel: 1,
    currentClass: '赤贫阶层',
    day: 1,
    corruption: identity.name === '官二代' ? 0 : undefined,
  };
}

export function work(player: Player): { income: number; newPlayer: Player } {
  const baseIncome = player.identity.startMoney * 0.01; // 日收入为启动资金的 1%
  const income = Math.floor(baseIncome * (1 + player.classLevel * 0.1));
  
  return {
    income,
    newPlayer: {
      ...player,
      cash: player.cash + income,
      stamina: clamp(player.stamina - 20, 0, 100),
      mood: clamp(player.mood - 5, 0, 100),
    },
  };
}

export function study(player: Player): Player {
  return {
    ...player,
    stamina: clamp(player.stamina - 10, 0, 100),
    reputation: clamp(player.reputation + 1, 0, 100),
    mood: clamp(player.mood + 5, 0, 100),
  };
}

export function rest(player: Player): { recovered: number; newPlayer: Player } {
  const recovered = 20;
  return {
    recovered,
    newPlayer: {
      ...player,
      stamina: clamp(player.stamina + recovered, 0, 100),
      health: clamp(player.health + 2, 0, 100),
    },
  };
}

export function createCompany(name: string, type: string, player: Player): Company {
  return {
    name,
    type,
    level: 1,
    employees: 1,
    monthlyRevenue: player.identity.startMoney * 0.1,
    monthlyCost: player.identity.startMoney * 0.05,
    monthlyProfit: player.identity.startMoney * 0.05,
  };
}

export function dailyOperation(company: Company): number {
  const dailyProfit = company.monthlyProfit / 30;
  return Math.floor(dailyProfit);
}

export function buyItem(player: Player, item: ShopItem): Player {
  if (player.cash < item.price) {
    return player; // 钱不够
  }
  
  let updatedPlayer = {
    ...player,
    cash: player.cash - item.price,
  };
  
  // 应用效果
  switch (item.effect) {
    case '体力':
      updatedPlayer.stamina = clamp(updatedPlayer.stamina + item.effectValue, 0, 100);
      break;
    case '心情':
      updatedPlayer.mood = clamp(updatedPlayer.mood + item.effectValue, 0, 100);
      break;
    case '健康':
      updatedPlayer.health = clamp(updatedPlayer.health + item.effectValue, 0, 100);
      break;
    case '技能':
      updatedPlayer.reputation = clamp(updatedPlayer.reputation + item.effectValue / 2, 0, 100);
      break;
    case '人脉':
      updatedPlayer.connections = clamp(updatedPlayer.connections + item.effectValue, 0, 100);
      break;
    case '声誉':
      updatedPlayer.reputation = clamp(updatedPlayer.reputation + item.effectValue / 2, 0, 100);
      break;
  }
  
  return updatedPlayer;
}

export function getMarketIntelligence(player: Player): Record<string, string> {
  const level = player.classLevel;
  
  if (level <= 2) {
    // 低身份：模糊情报
    return {
      '房地产': '听说房子能赚钱？（模糊）',
      '股票': '股市好像有风险？（传闻）',
      '大宗商品': '什么东西在涨价？（不清楚）',
    };
  } else if (level <= 4) {
    // 中等身份：基本准确
    return {
      '房地产': '房价可能在涨（+10~40%）',
      '股票': '股市不太乐观（-10~-30%）',
      '大宗商品': '价格波动较大（±15%）',
    };
  } else if (level <= 6) {
    // 高身份：准确情报
    return {
      '房地产': '准确数据：房价将涨 +25~35%',
      '股票': '内部消息：股市将跌 -15~-25%',
      '大宗商品': '精确数据：震荡±8-12%',
    };
  } else {
    // 顶级身份：内幕消息
    return {
      '房地产': '内幕：某新区规划即将公布，房价将涨 30%',
      '股票': '高层决策：某政策即将出台，某股将跌 20%',
      '大宗商品': '机密：国家储备计划，价格将上涨 15%',
    };
  }
}
