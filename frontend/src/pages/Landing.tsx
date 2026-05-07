import { ArrowRight, Radar, ShieldCheck, Sparkles } from 'lucide-react';

import { GlassPanel } from '../components/GlassPanel';

const features = [
  { title: 'Realtime monitoring', description: 'Stream sentiment updates, WebSocket alerts, and cached KPI cards.', icon: Radar },
  { title: 'Operational summaries', description: 'Convert noisy social data into executive-ready insight briefs.', icon: Sparkles },
  { title: 'Governed access', description: 'Workspace-level RBAC, audit trails, and secure JWT sessions.', icon: ShieldCheck },
];

export function LandingPage() {
  return (
    <div className="mx-auto flex min-h-screen max-w-7xl items-center px-5 py-12 lg:px-8">
      <div className="grid w-full gap-6 xl:grid-cols-[1.15fr_0.85fr]">
        <div className="space-y-6">
          <p className="inline-flex rounded-full border border-white/10 bg-white/7 px-4 py-2 text-xs uppercase tracking-[0.34em] text-slate-300">Sentiment intelligence for modern teams</p>
          <h1 className="max-w-3xl text-5xl font-semibold tracking-tight text-white lg:text-7xl">
            A control room for social sentiment, topics, and brand health.
          </h1>
          <p className="max-w-2xl text-lg leading-8 text-slate-300">
            FastAPI analytics, Django orchestration, Redis caching, Celery automation, and a React dashboard designed for serious operational monitoring.
          </p>
          <div className="flex flex-wrap gap-3">
            <a className="inline-flex items-center gap-2 rounded-2xl bg-white px-5 py-3 text-sm font-semibold text-slate-950" href="/dashboard">
              Enter dashboard <ArrowRight className="h-4 w-4" />
            </a>
            <a className="inline-flex items-center gap-2 rounded-2xl border border-white/10 bg-white/7 px-5 py-3 text-sm font-semibold text-white" href="/api-docs">
              Explore API surface
            </a>
          </div>
        </div>

        <GlassPanel className="space-y-4 p-6">
          <p className="text-xs uppercase tracking-[0.3em] text-slate-400">Why teams use it</p>
          {features.map((feature) => (
            <div key={feature.title} className="rounded-2xl border border-white/8 bg-white/5 p-4">
              <div className="flex items-center gap-3">
                <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-white/8 text-cyan-300">
                  <feature.icon className="h-4 w-4" />
                </div>
                <div>
                  <h3 className="font-semibold text-white">{feature.title}</h3>
                  <p className="mt-1 text-sm leading-6 text-slate-400">{feature.description}</p>
                </div>
              </div>
            </div>
          ))}
        </GlassPanel>
      </div>
    </div>
  );
}
