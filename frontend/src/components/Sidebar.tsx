import { Activity, BarChart3, BookText, FolderKanban, Gauge, Settings, ShieldCheck, Sparkles, Users } from 'lucide-react';
import { NavLink } from 'react-router-dom';

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: Gauge },
  { to: '/real-time', label: 'Live Analytics', icon: Sparkles },
  { to: '/reports', label: 'Report Center', icon: BarChart3 },
  { to: '/workspaces', label: 'Workspaces', icon: FolderKanban },
  { to: '/activity', label: 'Activity', icon: Activity },
  { to: '/api-docs', label: 'API Docs', icon: BookText },
  { to: '/admin', label: 'Admin', icon: ShieldCheck },
  { to: '/settings', label: 'Settings', icon: Settings },
];

export function Sidebar() {
  return (
    <aside className="hidden h-full w-72 shrink-0 border-r border-white/8 bg-slate-950/72 px-5 py-6 backdrop-blur xl:flex xl:flex-col">
      <div className="mb-8 flex items-center gap-3">
        <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-[linear-gradient(135deg,#22d3ee_0%,#38bdf8_45%,#a855f7_100%)] text-sm font-bold text-white shadow-lg shadow-cyan-500/20">
          SI
        </div>
        <div>
          <div className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-400">Sentiment Intelligence</div>
          <div className="text-lg font-semibold text-white">Platform</div>
        </div>
      </div>

      <nav className="space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              `group flex items-center gap-3 rounded-2xl px-4 py-3 text-sm font-medium transition ${
                isActive
                  ? 'bg-[linear-gradient(135deg,rgba(255,255,255,0.13),rgba(56,189,248,0.12))] text-white shadow-lg shadow-black/10 ring-1 ring-cyan-400/15'
                  : 'text-slate-400 hover:bg-white/6 hover:text-white hover:ring-1 hover:ring-white/5'
              }`
            }
          >
            <item.icon className="h-4 w-4" />
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="mt-auto rounded-[26px] border border-white/8 bg-gradient-to-br from-white/10 via-white/6 to-white/3 p-5 text-sm text-slate-300 shadow-glass">
        <div className="mb-2 flex items-center gap-2 text-white">
          <Users className="h-4 w-4" /> Team Health
        </div>
        <p className="leading-6 text-slate-400">4 workspaces active, 18 analysts online, 2 alerts waiting for review.</p>
        <div className="mt-4 flex items-center justify-between rounded-2xl border border-white/8 bg-slate-950/50 px-3 py-2 text-xs uppercase tracking-[0.24em] text-slate-400">
          <span>Pipeline</span>
          <span className="text-emerald-300">Stable</span>
        </div>
      </div>
    </aside>
  );
}