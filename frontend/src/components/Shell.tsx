import { Outlet } from 'react-router-dom';

import { Sidebar } from './Sidebar';
import { Topbar } from './Topbar';

export function Shell() {
  return (
    <div className="min-h-screen bg-[#050814] text-slate-100">
      <div className="pointer-events-none fixed inset-0 bg-[radial-gradient(circle_at_top_left,rgba(56,189,248,0.22),transparent_26%),radial-gradient(circle_at_80%_15%,rgba(168,85,247,0.16),transparent_28%),radial-gradient(circle_at_bottom_right,rgba(34,197,94,0.08),transparent_30%),linear-gradient(180deg,rgba(2,6,23,0),rgba(2,6,23,0.88))]" />
      <div className="pointer-events-none fixed inset-0 bg-dashboard-grid bg-[size:22px_22px] opacity-18" />
      <div className="relative flex min-h-screen">
        <Sidebar />
        <div className="relative flex min-h-screen flex-1 flex-col">
          <Topbar />
          <main className="flex-1 px-5 py-6 lg:px-8 lg:py-8">
            <Outlet />
          </main>
        </div>
      </div>
    </div>
  );
}
