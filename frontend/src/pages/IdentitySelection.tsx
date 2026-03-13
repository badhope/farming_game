import React, { useState } from 'react';
import { useGame } from '../store/GameContext';
import { Identity } from '../game/gameLogic';
import './IdentitySelection.css';

export default function IdentitySelection() {
  const { selectedIdentity, selectIdentity, startGame } = useGame();
  const [playerName, setPlayerName] = useState('玩家');
  const [gameStarted, setGameStarted] = useState(false);

  const handleStartGame = () => {
    if (selectedIdentity) {
      startGame(playerName);
      setGameStarted(true);
    }
  };

  if (gameStarted) {
    return (
      <div className="identity-selection game-started">
        <h2>🎮 游戏已开始！</h2>
        <p>祝你游戏愉快，早日成为中国百万富翁！</p>
      </div>
    );
  }

  return (
    <div className="identity-selection">
      <div className="header">
        <h1>🎯 中国百万富翁</h1>
        <h2>CHINESE MILLIONAIRE</h2>
        <p className="subtitle">你的致富之路，从这里开始！</p>
      </div>

      <div className="step-indicator">
        <div className="step active">第一步：选择你的起始身份</div>
      </div>

      <div className="instructions">
        <p>不同的身份将决定你的：</p>
        <ul>
          <li>💰 启动资金</li>
          <li>🤝 初始人脉</li>
          <li>📚 特殊技能</li>
          <li>🎯 发展路线</li>
        </ul>
      </div>

      <div className="identities-grid">
        {[
          {
            name: '农民',
            emoji: '🧑‍🌾',
            color: '#8B4513',
          },
          {
            name: '小镇青年',
            emoji: '🧑‍💼',
            color: '#4682B4',
          },
          {
            name: '大学生',
            emoji: '🎓',
            color: '#4169E1',
          },
          {
            name: '海归',
            emoji: '✈️',
            color: '#1E90FF',
          },
          {
            name: '个体户',
            emoji: '🏪',
            color: '#32CD32',
          },
          {
            name: '官二代',
            emoji: '🏛️',
            color: '#DAA520',
          },
        ].map((identityInfo) => {
          const identity = selectedIdentity?.name === identityInfo.name 
            ? selectedIdentity 
            : undefined;
          const isSelected = !!identity;

          return (
            <div
              key={identityInfo.name}
              className={`identity-card ${isSelected ? 'selected' : ''}`}
              onClick={() => {
                const fullIdentity = [
                  {
                    name: '农民',
                    description: '农村起家，农业相关加成',
                    startMoney: 8000,
                    connections: 20,
                    education: '初中',
                    skills: ['精通农业', '吃苦耐劳'],
                    bonus: { agriculture_cost: 0.7, crop_yield: 1.25 },
                    bonusDescription: '农业成本 -30%，产量 +25%',
                  },
                  {
                    name: '小镇青年',
                    description: '县城创业，零售业优势',
                    startMoney: 25000,
                    connections: 35,
                    education: '高中',
                    skills: ['精打细算', '人情世故'],
                    bonus: { rent_discount: 0.6, loan_approve: 1.3 },
                    bonusDescription: '租金 -40%，小额贷款更容易',
                  },
                  {
                    name: '大学生',
                    description: '科技创业，互联网行业',
                    startMoney: 50000,
                    connections: 25,
                    education: '本科',
                    skills: ['创新思维', '学习能力'],
                    bonus: { tech_startup: 0.5, funding_rate: 1.4 },
                    bonusDescription: '科技创业门槛 -50%，融资成功率 +40%',
                  },
                  {
                    name: '海归',
                    description: '国际贸易，金融投资',
                    startMoney: 200000,
                    connections: 15,
                    education: '硕士',
                    skills: ['国际视野', '英语流利'],
                    bonus: { tariff_discount: 0.7, forex_fee: 0.5 },
                    bonusDescription: '国际贸易关税 -30%，外汇手续费 -50%',
                  },
                  {
                    name: '个体户',
                    description: '批发市场，制造业',
                    startMoney: 80000,
                    connections: 50,
                    education: '高中',
                    skills: ['生意头脑', '供应链'],
                    bonus: { wholesale_discount: 0.75, cash_flow: 1.3 },
                    bonusDescription: '批发价 -25%，现金流 +30%',
                  },
                  {
                    name: '官二代',
                    description: '人脉优势，政策敏感',
                    startMoney: 150000,
                    connections: 80,
                    education: '本科',
                    skills: ['人脉通天', '政策敏感'],
                    bonus: { gov_project: 1.6, loan_approve: 1.4 },
                    bonusDescription: '政府项目优势，贷款审批更容易（但有腐败风险）',
                  },
                ].find(i => i.name === identityInfo.name);
                
                if (fullIdentity) {
                  selectIdentity(fullIdentity);
                }
              }}
              style={{ borderColor: isSelected ? identityInfo.color : 'transparent' }}
            >
              <div className="identity-emoji" style={{ color: identityInfo.color }}>
                {identityInfo.emoji}
              </div>
              <h3>{identityInfo.name}</h3>
              {identity && (
                <div className="identity-details">
                  <p className="description">{identity.description}</p>
                  <div className="stats">
                    <div className="stat">
                      <span className="label">💰 启动资金</span>
                      <span className="value">¥{identity.startMoney.toLocaleString()}</span>
                    </div>
                    <div className="stat">
                      <span className="label">🤝 初始人脉</span>
                      <span className="value">{identity.connections}/100</span>
                    </div>
                    <div className="stat">
                      <span className="label">🎓 学历</span>
                      <span className="value">{identity.education}</span>
                    </div>
                    <div className="stat">
                      <span className="label">📚 特殊技能</span>
                      <span className="value">{identity.skills.join('、')}</span>
                    </div>
                    <div className="stat bonus">
                      <span className="label">⭐ 核心优势</span>
                      <span className="value">{identity.bonusDescription}</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      <div className="player-name-input">
        <label htmlFor="playerName">你的名字：</label>
        <input
          type="text"
          id="playerName"
          value={playerName}
          onChange={(e) => setPlayerName(e.target.value)}
          placeholder="输入你的名字"
          maxLength={20}
        />
      </div>

      <div className="action-buttons">
        <button
          className="start-button"
          onClick={handleStartGame}
          disabled={!selectedIdentity}
        >
          🚀 开始致富之路
        </button>
      </div>

      {!selectedIdentity && (
        <p className="hint">👆 请先选择一个身份开始游戏</p>
      )}
    </div>
  );
}
