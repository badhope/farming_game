import React, { useState } from 'react';
import { useGame } from '../store/GameContext';
import { getMarketIntelligence, calculateNetWorth, formatMoney, SHOP_ITEMS, ShopItem, CITIES, STRATEGIES } from '../game/gameLogic';
import './MainGame.css';

export default function MainGame() {
  const { 
    player, 
    company, 
    currentCity, 
    handleWork, 
    handleStudy, 
    handleRest, 
    handleBuyItem,
    saveGame,
    resetGame,
    gameEnded,
    endReason,
  } = useGame();

  const [message, setMessage] = useState<string>('');
  const [showShop, setShowShop] = useState(false);
  const [showFinancials, setShowFinancials] = useState(false);
  const [showCompany, setShowCompany] = useState(false);
  const [showCityMap, setShowCityMap] = useState(false);

  if (!player) {
    return <div className="main-game error">游戏未开始，请返回首页</div>;
  }

  const marketIntel = getMarketIntelligence(player);
  const netWorth = calculateNetWorth(player);

  const showMessage = (msg: string) => {
    setMessage(msg);
    setTimeout(() => setMessage(''), 3000);
  };

  const onWork = () => {
    const income = handleWork();
    showMessage(`💪 你今天努力工作，收入${formatMoney(income)}`);
  };

  const onStudy = () => {
    handleStudy();
    showMessage(`📚 你学习了新知识，技能提升了！`);
  };

  const onRest = () => {
    const recovered = handleRest();
    showMessage(`😴 你休息了一天，体力恢复了${recovered}点`);
  };

  const onBuyItem = (item: ShopItem) => {
    if (player.cash < item.price) {
      showMessage(`❌ 现金不足！需要${formatMoney(item.price)}`);
      return;
    }
    handleBuyItem(item);
    showMessage(`✅ 购买了${item.name}，效果：${item.effect} +${item.effectValue}`);
  };

  const onSaveGame = () => {
    saveGame();
    showMessage('💾 游戏已保存');
  };

  if (gameEnded) {
    return (
      <div className="main-game game-over">
        <h1>💔 游戏结束</h1>
        <h2>结束原因：{endReason}</h2>
        <div className="final-stats">
          <p>坚持了 {player.day} 天</p>
          <p>最终身份：{player.identity.name}</p>
          <p>社会阶层：{player.currentClass}</p>
          <p>净资产：{formatMoney(netWorth)}</p>
        </div>
        <button className="restart-button" onClick={resetGame}>
          🔄 重新开始
        </button>
      </div>
    );
  }

  return (
    <div className="main-game">
      {/* 每日报告 */}
      <div className="daily-report">
        <h2>📊 第 {player.day} 天的经营报告</h2>
        
        <div className="report-grid">
          <div className="report-section assets">
            <h3>💰 资产状况</h3>
            <div className="stat-row">
              <span className="label">现金：</span>
              <span className="value">{formatMoney(player.cash)}</span>
            </div>
            <div className="stat-row">
              <span className="label">总资产：</span>
              <span className="value">{formatMoney(netWorth + player.loans)}</span>
            </div>
            <div className="stat-row">
              <span className="label">净资产：</span>
              <span className="value highlight">{formatMoney(netWorth)}</span>
            </div>
          </div>

          <div className="report-section status">
            <h3>📊 社会地位</h3>
            <div className="stat-row">
              <span className="label">当前阶层：</span>
              <span className="value">{player.currentClass} (Lv.{player.classLevel})</span>
            </div>
            <div className="stat-row">
              <span className="label">人脉关系：</span>
              <span className="value">{player.connections}/100</span>
            </div>
            <div className="stat-row">
              <span className="label">声誉：</span>
              <span className="value">{player.reputation}/100</span>
            </div>
          </div>

          <div className="report-section personal">
            <h3>👤 个人状态</h3>
            <div className="stat-row">
              <span className="label">体力：</span>
              <div className="progress-bar">
                <div 
                  className="progress fill-stamina" 
                  style={{ width: `${player.stamina}%` }}
                />
                <span className="progress-text">{player.stamina}/100</span>
              </div>
            </div>
            <div className="stat-row">
              <span className="label">心情：</span>
              <div className="progress-bar">
                <div 
                  className="progress fill-mood" 
                  style={{ width: `${player.mood}%` }}
                />
                <span className="progress-text">{player.mood}/100</span>
              </div>
            </div>
            <div className="stat-row">
              <span className="label">健康：</span>
              <div className="progress-bar">
                <div 
                  className="progress fill-health" 
                  style={{ width: `${player.health}%` }}
                />
                <span className="progress-text">{player.health}/100</span>
              </div>
            </div>
          </div>

          <div className="report-section intel">
            <h3>📈 今日情报</h3>
            {Object.entries(marketIntel).map(([market, info]) => (
              <div key={market} className="intel-item">
                <span className="market">{market}：</span>
                <span className="info">{info}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 消息提示 */}
      {message && (
        <div className="message-toast">
          {message}
        </div>
      )}

      {/* 行动选择区域 */}
      <div className="actions-section">
        <h3>🎯 今日行动</h3>
        
        <div className="actions-grid">
          {/* 基础行动 */}
          <div className="action-category">
            <h4>📌 基础行动</h4>
            <div className="action-buttons">
              <button 
                className="action-btn work" 
                onClick={onWork}
                disabled={player.stamina < 20}
              >
                💼 工作赚钱
                <span className="btn-desc">打工获取收入</span>
              </button>
              <button className="action-btn study" onClick={onStudy}>
                📚 学习提升
                <span className="btn-desc">提升技能</span>
              </button>
              <button 
                className="action-btn rest" 
                onClick={onRest}
                disabled={player.stamina >= 100}
              >
                😴 休息恢复
                <span className="btn-desc">恢复体力</span>
              </button>
            </div>
          </div>

          {/* 解锁的行动 */}
          {player.classLevel >= 4 && (
            <div className="action-category">
              <h4>💼 商业行动</h4>
              <div className="action-buttons">
                <button 
                  className="action-btn business"
                  onClick={() => setShowCompany(!showCompany)}
                >
                  🏢 公司经营
                  <span className="btn-desc">
                    {company ? '管理公司' : '创建公司'}
                  </span>
                </button>
              </div>
            </div>
          )}

          {player.classLevel >= 5 && (
            <div className="action-category">
              <h4>📊 投资行动</h4>
              <div className="action-buttons">
                <button className="action-btn investment">
                  📈 投资理财
                  <span className="btn-desc">钱生钱</span>
                </button>
                <button className="action-btn investment">
                  🏠 房地产
                  <span className="btn-desc">买房致富</span>
                </button>
              </div>
            </div>
          )}

          {/* 消费行动 */}
          <div className="action-category">
            <h4>🛒 消费行动</h4>
            <div className="action-buttons">
              <button 
                className="action-btn shop"
                onClick={() => setShowShop(!showShop)}
              >
                🛍️ 逛商场购物
                <span className="btn-desc">提升生活质量</span>
              </button>
            </div>
          </div>

          {/* 查询 */}
          <div className="action-category">
            <h4>📊 查询</h4>
            <div className="action-buttons">
              <button 
                className="action-btn info"
                onClick={() => setShowFinancials(!showFinancials)}
              >
                📋 查看完整资产
                <span className="btn-desc">详细财务报表</span>
              </button>
              {company && (
                <button 
                  className="action-btn info"
                  onClick={() => setShowCompany(!showCompany)}
                >
                  🏢 查看公司状况
                  <span className="btn-desc">公司经营数据</span>
                </button>
              )}
              <button 
                className="action-btn info"
                onClick={() => setShowCityMap(!showCityMap)}
              >
                🗺️ 查看地图
                <span className="btn-desc">可前往的城市</span>
              </button>
            </div>
          </div>

          {/* 游戏控制 */}
          <div className="action-category">
            <h4>⏸️ 游戏控制</h4>
            <div className="action-buttons">
              <button className="action-btn save" onClick={onSaveGame}>
                💾 保存并退出
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* 购物面板 */}
      {showShop && (
        <div className="modal-overlay" onClick={() => setShowShop(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <h3>🛍️ 购物中心 - {currentCity?.name}</h3>
            <button className="close-btn" onClick={() => setShowShop(false)}>×</button>
            
            <div className="shop-items">
              {SHOP_ITEMS.map(item => (
                <div key={item.name} className="shop-item">
                  <div className="item-info">
                    <h4>{item.name}</h4>
                    <p className="item-effect">{item.effect} +{item.effectValue}</p>
                  </div>
                  <div className="item-price">
                    <span className="price">{formatMoney(item.price)}</span>
                    <button 
                      className="buy-btn"
                      onClick={() => onBuyItem(item)}
                      disabled={player.cash < item.price}
                    >
                      购买
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* 财务报表面板 */}
      {showFinancials && (
        <div className="modal-overlay" onClick={() => setShowFinancials(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <h3>📋 完整财务报表</h3>
            <button className="close-btn" onClick={() => setShowFinancials(false)}>×</button>
            
            <div className="financial-report">
              <div className="report-section-full">
                <h4>💰 资产</h4>
                <div className="report-row">
                  <span>现金：</span>
                  <span>{formatMoney(player.cash)}</span>
                </div>
                <div className="report-row">
                  <span>房产：</span>
                  <span>{formatMoney(player.realEstate)}</span>
                </div>
                <div className="report-row">
                  <span>车辆：</span>
                  <span>{formatMoney(player.vehicles)}</span>
                </div>
                <div className="report-row">
                  <span>投资：</span>
                  <span>{formatMoney(player.investments)}</span>
                </div>
                <div className="report-row total">
                  <span>总资产：</span>
                  <span>{formatMoney(player.cash + player.realEstate + player.vehicles + player.investments)}</span>
                </div>
              </div>

              <div className="report-section-full">
                <h4>💸 负债</h4>
                <div className="report-row">
                  <span>贷款：</span>
                  <span>{formatMoney(player.loans)}</span>
                </div>
                <div className="report-row total">
                  <span>总负债：</span>
                  <span>{formatMoney(player.loans)}</span>
                </div>
              </div>

              <div className="report-section-full">
                <h4>📊 净资产</h4>
                <div className="report-row highlight">
                  <span>净资产：</span>
                  <span>{formatMoney(netWorth)}</span>
                </div>
              </div>

              <div className="report-section-full">
                <h4>🏆 社会地位</h4>
                <div className="report-row">
                  <span>当前阶层：</span>
                  <span>{player.currentClass}</span>
                </div>
                <div className="report-row">
                  <span>阶层等级：</span>
                  <span>Lv.{player.classLevel}</span>
                </div>
                <div className="report-row">
                  <span>财富排名：</span>
                  <span>第{player.connections}名</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 城市地图面板 */}
      {showCityMap && (
        <div className="modal-overlay" onClick={() => setShowCityMap(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <h3>🗺️ 中国地图</h3>
            <button className="close-btn" onClick={() => setShowCityMap(false)}>×</button>
            
            <div className="city-list">
              {CITIES.map(city => (
                <div 
                  key={city.name} 
                  className={`city-item ${currentCity?.name === city.name ? 'current' : ''}`}
                >
                  <div className="city-info">
                    <h4>{city.name}</h4>
                    <p className="city-type">{city.type}</p>
                    <p className="city-industry">产业：{city.industry}</p>
                  </div>
                  <div className="city-bonus">
                    {Object.entries(city.bonuses).map(([key, value]) => (
                      <span key={key} className="bonus-tag">
                        {key} +{((value - 1) * 100).toFixed(0)}%
                      </span>
                    ))}
                  </div>
                  {currentCity?.name !== city.name && (
                    <button className="travel-btn">
                      前往
                    </button>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* 公司面板 */}
      {showCompany && (
        <div className="modal-overlay" onClick={() => setShowCompany(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <h3>🏢 公司管理</h3>
            <button className="close-btn" onClick={() => setShowCompany(false)}>×</button>
            
            {company ? (
              <div className="company-details">
                <div className="company-header">
                  <h4>{company.name}</h4>
                  <span className="company-type">{company.type}</span>
                </div>
                <div className="company-stats">
                  <div className="stat-row">
                    <span>等级：</span>
                    <span>Lv.{company.level}</span>
                  </div>
                  <div className="stat-row">
                    <span>员工：</span>
                    <span>{company.employees}人</span>
                  </div>
                  <div className="stat-row">
                    <span>月收入：</span>
                    <span className="income">{formatMoney(company.monthlyRevenue)}</span>
                  </div>
                  <div className="stat-row">
                    <span>月支出：</span>
                    <span className="cost">{formatMoney(company.monthlyCost)}</span>
                  </div>
                  <div className="stat-row">
                    <span>月利润：</span>
                    <span className="profit">{formatMoney(company.monthlyProfit)}</span>
                  </div>
                </div>
                <button className="action-btn operate">
                  📊 日常经营
                </button>
              </div>
            ) : (
              <div className="create-company">
                <p>创建你的第一家公司！</p>
                <p className="cost">💰 创建成本：¥50,000</p>
                <div className="form-group">
                  <label>公司名称：</label>
                  <input type="text" placeholder="输入公司名称" />
                </div>
                <div className="form-group">
                  <label>公司类型：</label>
                  <select>
                    <option>科技</option>
                    <option>贸易</option>
                    <option>餐饮</option>
                    <option>制造</option>
                    <option>农业</option>
                  </select>
                </div>
                <button className="action-btn create">
                  🚀 创建公司
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
