import { createBrowserRouter, Navigate } from 'react-router-dom';
import Home from './pages/Home';
import Download from './pages/Download';
import GameLayout from './pages/GameLayout';
import Farm from './pages/Farm';
import Shop from './pages/Shop';
import Achievements from './pages/Achievements';
import AIAssistant from './pages/AIAssistant';
import Statistics from './pages/Statistics';
import IdentitySelection from './pages/IdentitySelection';
import MainGame from './pages/MainGame';
import { GameProvider } from './store/GameContext';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Home />,
  },
  {
    path: '/download',
    element: <Download />,
  },
  {
    path: '/millionaire',
    element: (
      <GameProvider>
        <IdentitySelection />
      </GameProvider>
    ),
  },
  {
    path: '/millionaire/game',
    element: (
      <GameProvider>
        <MainGame />
      </GameProvider>
    ),
  },
  {
    path: '/game',
    element: <GameLayout />,
    children: [
      {
        index: true,
        element: <Navigate to="/game/farm" replace />,
      },
      {
        path: 'farm',
        element: <Farm />,
      },
      {
        path: 'shop',
        element: <Shop />,
      },
      {
        path: 'achievements',
        element: <Achievements />,
      },
      {
        path: 'ai',
        element: <AIAssistant />,
      },
      {
        path: 'statistics',
        element: <Statistics />,
      },
    ],
  },
]);

export default router;
