import { Outlet } from 'react-router-dom';

import { Sidebar } from './Sidebar';
import { Topbar } from './Topbar';

export function Shell() {
  return (
    <div className="min-h-screen bg-[#060816] text-slate-100">
      <div className="pointer-events-none fixed inset-0 bg-[radial-gradient(circle_at_top_left,rgba(56,189,248,0.17),transparent_30%),radial-gradient(circle_at_right,rgba(236,72,153,0.18),transparent_32%),linear-gradient(180deg,rgba(2,6,23,0),rgba(2,6,23,0.82))]" />
      <div className="pointer-events-none fixed inset-0 bg-dashboard-grid bg-[size:22px_22px] opacity-20" />
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
