import { ArrowRight, BarChart3, Radar, ShieldCheck, Sparkles } from 'lucide-react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';

import { GlassPanel } from '../components/GlassPanel';

const features = [
  { title: 'Realtime monitoring', description: 'Stream sentiment updates, WebSocket alerts, and cached KPI cards.', icon: Radar },
  { title: 'Operational summaries', description: 'Convert noisy social data into executive-ready insight briefs.', icon: Sparkles },
  { title: 'Governed access', description: 'Workspace-level RBAC, audit trails, and secure JWT sessions.', icon: ShieldCheck },
];

const stats = [
  { label: 'Sources indexed', value: '128K+' },
  { label: 'Signal latency', value: '< 2s' },
  { label: 'Models active', value: '6' },
];

export function LandingPage() {
  return (
    <div className="mx-auto flex min-h-screen max-w-7xl items-center px-5 py-12 lg:px-8">
      <div className="grid w-full gap-8 xl:grid-cols-[1.1fr_0.9fr]">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.55, ease: 'easeOut' }}
          className="space-y-6"
        >
          <p className="inline-flex rounded-full border border-cyan-400/20 bg-cyan-400/10 px-4 py-2 text-xs uppercase tracking-[0.34em] text-cyan-200">
            Sentiment intelligence for modern teams
          </p>
          <h1 className="max-w-3xl text-5xl font-semibold tracking-tight text-white lg:text-7xl">
            A command center for social sentiment, topics, and brand health.
          </h1>
          <p className="max-w-2xl text-lg leading-8 text-slate-300">
            FastAPI analytics, Django orchestration, Redis caching, Celery automation, and a React dashboard built to feel like a real operating system for brand signal.
          </p>
          <div className="flex flex-wrap gap-3">
            <Link className="inline-flex items-center gap-2 rounded-2xl bg-white px-5 py-3 text-sm font-semibold text-slate-950 transition hover:-translate-y-0.5 hover:bg-cyan-50" to="/dashboard">
              Enter dashboard <ArrowRight className="h-4 w-4" />
            </Link>
            <Link className="inline-flex items-center gap-2 rounded-2xl border border-white/10 bg-white/7 px-5 py-3 text-sm font-semibold text-white transition hover:border-cyan-400/30 hover:bg-white/12" to="/api-docs">
              Explore API surface
            </Link>
          </div>

          <div className="grid gap-3 sm:grid-cols-3">
            {stats.map((stat) => (
              <div key={stat.label} className="rounded-3xl border border-white/10 bg-white/5 p-4 backdrop-blur-xl">
                <div className="text-2xl font-semibold text-white">{stat.value}</div>
                <div className="mt-1 text-xs uppercase tracking-[0.24em] text-slate-400">{stat.label}</div>
              </div>
            ))}
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.65, delay: 0.1, ease: 'easeOut' }}
          className="space-y-4"
        >
          <GlassPanel className="relative overflow-hidden p-6">
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(56,189,248,0.16),transparent_30%),radial-gradient(circle_at_bottom_left,rgba(168,85,247,0.14),transparent_28%)]" />
            <div className="relative flex items-center justify-between">
              <div>
                <p className="text-xs uppercase tracking-[0.3em] text-slate-400">Live system pulse</p>
                <h2 className="mt-2 text-2xl font-semibold text-white">Operational signal board</h2>
              </div>
              <div className="rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1 text-xs font-medium text-emerald-200">
                99.98% uptime
              </div>
            </div>

            <div className="relative mt-6 grid gap-4 sm:grid-cols-2">
              <div className="rounded-3xl border border-white/10 bg-slate-950/55 p-4">
                <div className="flex items-center gap-3 text-cyan-300">
                  <BarChart3 className="h-5 w-5" />
                  <span className="text-sm font-medium uppercase tracking-[0.22em] text-slate-300">Signal score</span>
                </div>
                <div className="mt-4 text-4xl font-semibold text-white">94.2</div>
                <p className="mt-2 text-sm leading-6 text-slate-400">Brand sentiment is climbing across launch and product conversations.</p>
              </div>

              <div className="rounded-3xl border border-white/10 bg-slate-950/55 p-4">
                <p className="text-xs uppercase tracking-[0.24em] text-slate-400">Why teams use it</p>
                <div className="mt-4 space-y-3">
                  {features.map((feature) => (
                    <div key={feature.title} className="flex items-center gap-3 rounded-2xl border border-white/8 bg-white/5 p-3">
                      <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-white/8 text-cyan-300">
                        <feature.icon className="h-4 w-4" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-white">{feature.title}</h3>
                        <p className="text-sm leading-6 text-slate-400">{feature.description}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </GlassPanel>
        </motion.div>
      </div>
    </div>
  );
}
