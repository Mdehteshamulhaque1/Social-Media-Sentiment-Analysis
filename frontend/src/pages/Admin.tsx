import { BarChart4, ServerCog } from 'lucide-react';

import { GlassPanel } from '../components/GlassPanel';

export function AdminPage() {
  return (
    <div className="grid gap-6 xl:grid-cols-2">
      <GlassPanel>
        <div className="flex items-center gap-3 text-cyan-300">
          <ServerCog className="h-5 w-5" /> Admin monitoring
        </div>
        <p className="mt-4 text-sm leading-7 text-slate-400">Operational dashboards for queue depth, API error budgets, Celery retries, and platform health.</p>
      </GlassPanel>
      <GlassPanel>
        <div className="flex items-center gap-3 text-cyan-300">
          <BarChart4 className="h-5 w-5" /> Usage analytics
        </div>
        <p className="mt-4 text-sm leading-7 text-slate-400">Request volumes, rate limiting, cache hit ratio, and workspace usage are surfaced for administrators.</p>
      </GlassPanel>
    </div>
  );
}
