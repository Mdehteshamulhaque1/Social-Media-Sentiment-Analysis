import { Navigate, Route, Routes } from 'react-router-dom';

import { Shell } from './components/Shell';
import { ActivityPage } from './pages/Activity';
import { AdminPage } from './pages/Admin';
import { ApiDocsPage } from './pages/ApiDocs';
import { AuthPage } from './pages/Auth';
import { DashboardPage } from './pages/Dashboard';
import { LandingPage } from './pages/Landing';
import { ReportsPage } from './pages/Reports';
import { SettingsPage } from './pages/Settings';
import { WorkspacesPage } from './pages/Workspaces';

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<AuthPage />} />
      <Route element={<Shell />}>
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/real-time" element={<DashboardPage />} />
        <Route path="/reports" element={<ReportsPage />} />
        <Route path="/workspaces" element={<WorkspacesPage />} />
        <Route path="/activity" element={<ActivityPage />} />
        <Route path="/api-docs" element={<ApiDocsPage />} />
        <Route path="/admin" element={<AdminPage />} />
        <Route path="/settings" element={<SettingsPage />} />
      </Route>
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}
