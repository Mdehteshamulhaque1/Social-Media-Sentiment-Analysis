import { Clock3, ShieldCheck } from 'lucide-react';

import { GlassPanel } from '../components/GlassPanel';

export function ActivityPage() {
  return (
    <GlassPanel>
      <div className="flex items-center gap-3 text-cyan-300">
        <Clock3 className="h-5 w-5" /> Activity history
      </div>
      <div className="mt-5 space-y-4">
        {['CSV upload accepted', 'Workspace role updated', 'Report export generated'].map((event) => (
          <div key={event} className="flex items-center justify-between rounded-3xl border border-white/8 bg-white/5 px-5 py-4">
            <span className="text-sm text-white">{event}</span>
            <span className="inline-flex items-center gap-2 text-xs text-slate-400"><ShieldCheck className="h-4 w-4" />audited</span>
          </div>
        ))}
      </div>
    </GlassPanel>
  );
}
