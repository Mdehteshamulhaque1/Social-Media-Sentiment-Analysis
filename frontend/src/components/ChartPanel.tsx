import { Area, AreaChart, Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

import { GlassPanel } from './GlassPanel';

export function TrendChart({ data }: { data: Array<{ label: string; positive: number; negative: number; neutral: number }> }) {
  return (
    <GlassPanel className="h-[360px]">
      <div className="mb-5 flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.3em] text-slate-400">Trend comparison</p>
          <h2 className="mt-2 text-lg font-semibold text-white">Sentiment movement over the last 7 days</h2>
        </div>
        <div className="rounded-full border border-white/8 bg-white/6 px-3 py-1 text-xs text-slate-300">Live feed</div>
      </div>
      <ResponsiveContainer width="100%" height="85%">
        <AreaChart data={data}>
          <defs>
            <linearGradient id="positiveFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#22c55e" stopOpacity={0.45} />
              <stop offset="95%" stopColor="#22c55e" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="negativeFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#f43f5e" stopOpacity={0.35} />
              <stop offset="95%" stopColor="#f43f5e" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="4 4" stroke="rgba(255,255,255,0.08)" vertical={false} />
          <XAxis dataKey="label" tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={false} tickLine={false} />
          <YAxis tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={false} tickLine={false} />
          <Tooltip
            contentStyle={{
              background: 'rgba(2, 6, 23, 0.92)',
              border: '1px solid rgba(255,255,255,0.08)',
              borderRadius: 18,
              color: '#fff',
            }}
          />
          <Area type="monotone" dataKey="positive" stroke="#22c55e" fill="url(#positiveFill)" strokeWidth={2.5} />
          <Area type="monotone" dataKey="negative" stroke="#f43f5e" fill="url(#negativeFill)" strokeWidth={2.5} />
          <Area type="monotone" dataKey="neutral" stroke="#38bdf8" fillOpacity={0} strokeWidth={2.2} />
        </AreaChart>
      </ResponsiveContainer>
    </GlassPanel>
  );
}

export function KeywordBars({ data }: { data: Array<{ label: string; value: number }> }) {
  return (
    <GlassPanel className="h-[360px]">
      <div className="mb-5">
        <p className="text-xs uppercase tracking-[0.3em] text-slate-400">Top keywords</p>
        <h2 className="mt-2 text-lg font-semibold text-white">High-signal themes across monitored sources</h2>
      </div>
      <ResponsiveContainer width="100%" height="86%">
        <BarChart data={data} layout="vertical">
          <CartesianGrid strokeDasharray="4 4" stroke="rgba(255,255,255,0.08)" horizontal={false} />
          <XAxis type="number" tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={false} tickLine={false} />
          <YAxis dataKey="label" type="category" tick={{ fill: '#cbd5e1', fontSize: 12 }} axisLine={false} tickLine={false} width={80} />
          <Tooltip contentStyle={{ background: 'rgba(2, 6, 23, 0.92)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: 18 }} />
          <Bar dataKey="value" radius={[0, 14, 14, 0]} fill="url(#keywordGradient)" />
          <defs>
            <linearGradient id="keywordGradient" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor="#38bdf8" />
              <stop offset="100%" stopColor="#c084fc" />
            </linearGradient>
          </defs>
        </BarChart>
      </ResponsiveContainer>
    </GlassPanel>
  );
}
