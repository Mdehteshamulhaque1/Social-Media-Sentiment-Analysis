import { motion } from 'framer-motion';
import { Flame, Globe2, Layers3, MessageSquareText, Sparkles } from 'lucide-react';
import { useEffect, useState } from 'react';

import { GlassPanel } from '../components/GlassPanel';
import { MetricCard } from '../components/MetricCard';
import { KeywordBars, TrendChart } from '../components/ChartPanel';
import { EmptyState } from '../components/EmptyState';
import { Skeleton } from '../components/Skeleton';
import { loadDashboardSnapshot } from '../lib/api';
import { DashboardSnapshot } from '../lib/types';
import { dashboardSnapshot as fallbackSnapshot } from '../data/mock';

const dashboardHighlights = [
  { label: 'Emotion detection', value: '92.4%', icon: Flame },
  { label: 'Multi-language coverage', value: '28 languages', icon: Globe2 },
  { label: 'Topic clustering', value: '14 clusters', icon: Layers3 },
  { label: 'Insight summaries', value: 'AI-generated', icon: Sparkles },
];

export function DashboardPage() {
  const [snapshot, setSnapshot] = useState<DashboardSnapshot>(fallbackSnapshot);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;
    const hydrate = async () => {
      try {
        const data = await loadDashboardSnapshot();
        if (!isMounted) {
          return;
        }
        setSnapshot({
          ...fallbackSnapshot,
          ...data,
          metrics: data.metrics?.length ? data.metrics : fallbackSnapshot.metrics,
          topKeywords: data.topKeywords?.length ? data.topKeywords : fallbackSnapshot.topKeywords,
          trendSeries: data.trendSeries?.length ? data.trendSeries : fallbackSnapshot.trendSeries,
          systemHealth: data.systemHealth?.length ? data.systemHealth : fallbackSnapshot.systemHealth,
        });
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    };

    hydrate();
    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <div className="space-y-6">
      <motion.section
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        className="grid gap-4 xl:grid-cols-[1.45fr_0.95fr]"
      >
        <GlassPanel className="relative overflow-hidden p-7">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(56,189,248,0.14),transparent_30%),radial-gradient(circle_at_bottom_left,rgba(236,72,153,0.12),transparent_28%)]" />
          <div className="relative max-w-3xl">
            <p className="text-xs uppercase tracking-[0.35em] text-slate-400">Real-time intelligence</p>
            <h2 className="mt-4 text-4xl font-semibold tracking-tight text-white lg:text-5xl">
              Monitor brand sentiment with a control-room style analytics stack.
            </h2>
            <p className="mt-5 max-w-2xl text-base leading-7 text-slate-300">
              FastAPI-powered analysis, Django orchestration, cached metrics, and live dashboards for teams that need real signal, not toy charts.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <button className="rounded-2xl bg-white px-4 py-3 text-sm font-semibold text-slate-950 transition hover:scale-[1.01]">Launch analysis</button>
              <button className="rounded-2xl border border-white/10 bg-white/7 px-4 py-3 text-sm font-semibold text-white transition hover:bg-white/12">View API docs</button>
            </div>
          </div>
        </GlassPanel>

        <GlassPanel className="space-y-4 p-6">
          <div>
            <p className="text-xs uppercase tracking-[0.3em] text-slate-400">System pulse</p>
            <h3 className="mt-2 text-lg font-semibold text-white">Current platform signals</h3>
          </div>
          {dashboardHighlights.map((item) => (
            <div key={item.label} className="flex items-center justify-between rounded-2xl border border-white/8 bg-white/5 px-4 py-4">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-white/8 text-cyan-300">
                  <item.icon className="h-4 w-4" />
                </div>
                <div>
                  <p className="text-sm text-slate-300">{item.label}</p>
                </div>
              </div>
              <div className="text-sm font-semibold text-white">{item.value}</div>
            </div>
          ))}
        </GlassPanel>
      </motion.section>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {isLoading
          ? Array.from({ length: 4 }).map((_, index) => <Skeleton key={index} className="h-36" />)
          : snapshot.metrics.map((metric) => <MetricCard key={metric.label} metric={metric} />)}
      </section>

      <section className="grid gap-6 xl:grid-cols-2">
        <TrendChart data={snapshot.trendSeries} />
        <KeywordBars data={snapshot.topKeywords} />
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.25fr_0.75fr]">
        <GlassPanel>
          <div className="mb-5 flex items-center justify-between">
            <div>
              <p className="text-xs uppercase tracking-[0.3em] text-slate-400">Recent analyses</p>
              <h3 className="mt-2 text-lg font-semibold text-white">Live feed of processed sentiment</h3>
            </div>
            <div className="rounded-full border border-white/8 bg-white/6 px-3 py-1 text-xs text-slate-300">Updated 12s ago</div>
          </div>
          <div className="overflow-hidden rounded-3xl border border-white/8">
            <table className="min-w-full divide-y divide-white/8 text-left text-sm">
              <thead className="bg-white/5 text-slate-400">
                <tr>
                  <th className="px-4 py-3 font-medium">Source</th>
                  <th className="px-4 py-3 font-medium">Sentiment</th>
                  <th className="px-4 py-3 font-medium">Confidence</th>
                  <th className="px-4 py-3 font-medium">Keywords</th>
                  <th className="px-4 py-3 font-medium">Age</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/8 bg-slate-950/30">
                {snapshot.recentAnalyses.map((row) => (
                  <tr key={row.id} className="transition hover:bg-white/5">
                    <td className="px-4 py-4 text-slate-100">{row.source}</td>
                    <td className="px-4 py-4 capitalize text-slate-300">{row.sentiment}</td>
                    <td className="px-4 py-4 text-slate-300">{Math.round(row.confidence * 100)}%</td>
                    <td className="px-4 py-4 text-slate-400">{row.keywords.join(' · ')}</td>
                    <td className="px-4 py-4 text-slate-500">{row.createdAt}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </GlassPanel>

        <GlassPanel>
          <div className="mb-5">
            <p className="text-xs uppercase tracking-[0.3em] text-slate-400">System health</p>
            <h3 className="mt-2 text-lg font-semibold text-white">Production infrastructure status</h3>
          </div>
          <div className="space-y-3">
            {snapshot.systemHealth.map((item) => (
              <div key={item.label} className="flex items-center justify-between rounded-2xl border border-white/8 bg-white/5 px-4 py-4">
                <div>
                  <p className="text-sm font-medium text-white">{item.label}</p>
                  <p className="text-xs text-slate-400">Operational component</p>
                </div>
                <div className="text-right">
                  <p className="text-sm font-semibold text-white">{item.value}</p>
                  <p className={`text-xs ${item.status === 'healthy' ? 'text-emerald-300' : item.status === 'warning' ? 'text-amber-300' : 'text-rose-300'}`}>
                    {item.status}
                  </p>
                </div>
              </div>
            ))}
          </div>
          <div className="mt-6 rounded-[24px] border border-white/8 bg-gradient-to-br from-cyan-500/10 via-slate-900/20 to-fuchsia-500/10 p-5">
            <div className="flex items-center gap-3 text-white">
              <MessageSquareText className="h-5 w-5 text-cyan-300" />
              <span className="font-semibold">AI insight summary</span>
            </div>
            <p className="mt-3 text-sm leading-6 text-slate-300">
              {snapshot.insightSummary ?? 'Positive feedback is trending upward on launch-related posts, while pricing conversations remain the leading source of negative sentiment.'}
            </p>
          </div>
        </GlassPanel>
      </section>

      <EmptyState
        title="No selected report yet"
        description="Select a saved report or create a new workspace view to populate the analytics canvas with filtered data."
      />
    </div>
  );
}
