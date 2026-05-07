import { ArrowDownRight, ArrowUpRight, Minus } from 'lucide-react';
import clsx from 'clsx';

import { MetricCardData } from '../lib/types';
import { GlassPanel } from './GlassPanel';

const toneStyles = {
  positive: 'text-emerald-300 bg-emerald-400/10',
  neutral: 'text-sky-300 bg-sky-400/10',
  negative: 'text-rose-300 bg-rose-400/10',
} as const;

export function MetricCard({ metric }: { metric: MetricCardData }) {
  const icon = metric.delta.startsWith('+') ? <ArrowUpRight className="h-4 w-4" /> : metric.delta.startsWith('-') ? <ArrowDownRight className="h-4 w-4" /> : <Minus className="h-4 w-4" />;

  return (
    <GlassPanel className="relative overflow-hidden">
      <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-white/20 to-transparent" />
      <p className="text-sm uppercase tracking-[0.28em] text-slate-400">{metric.label}</p>
      <div className="mt-4 flex items-end justify-between gap-4">
        <div>
          <div className="text-3xl font-semibold text-white dark:text-slate-50">{metric.value}</div>
          <div className={clsx('mt-2 inline-flex items-center gap-1 rounded-full px-3 py-1 text-xs font-medium', toneStyles[metric.tone])}>
            {icon}
            {metric.delta}
          </div>
        </div>
        <div className="h-14 w-14 rounded-2xl bg-gradient-to-br from-cyan-400/20 via-sky-400/10 to-fuchsia-500/20 blur-0" />
      </div>
    </GlassPanel>
  );
}
