import { createBrowserRouter, Navigate } from 'react-router-dom';
import { GameProvider } from './store/GameContext';
import Home from './pages/Home';
import GameLayout from './pages/GameLayout';
import Farm from './pages/Farm';
import Shop from './pages/Shop';
import Achievements from './pages/Achievements';
import AIAssistant from './pages/AIAssistant';
import Statistics from './pages/Statistics';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Home />,
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
