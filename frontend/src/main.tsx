import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { RouterProvider } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import zhCN from 'antd/locale/zh_CN';
import { GameProvider } from './store/GameContext';
import router from './router';
import './index.css';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ConfigProvider locale={zhCN}>
      <GameProvider>
        <RouterProvider router={router} />
      </GameProvider>
    </ConfigProvider>
  </StrictMode>
);
