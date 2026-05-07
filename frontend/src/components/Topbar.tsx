import { MoonStar, Search, SunMedium } from 'lucide-react';

import { useTheme } from '../lib/theme';

export function Topbar() {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="flex items-center justify-between gap-4 border-b border-white/8 px-5 py-4 lg:px-8">
      <div>
        <p className="text-xs uppercase tracking-[0.34em] text-slate-400">Operational overview</p>
        <h1 className="mt-2 text-2xl font-semibold text-white dark:text-slate-50">Sentiment Intelligence Platform</h1>
      </div>

      <div className="flex items-center gap-3">
        <div className="hidden items-center gap-2 rounded-full border border-white/10 bg-white/7 px-4 py-2 text-sm text-slate-400 md:flex">
          <Search className="h-4 w-4" /> Search analyses, workspaces, reports
        </div>
        <button
          type="button"
          onClick={toggleTheme}
          className="flex h-11 w-11 items-center justify-center rounded-2xl border border-white/10 bg-white/7 text-slate-200 transition hover:bg-white/12"
        >
          {theme === 'dark' ? <SunMedium className="h-4 w-4" /> : <MoonStar className="h-4 w-4" />}
        </button>
      </div>
    </header>
  );
}
