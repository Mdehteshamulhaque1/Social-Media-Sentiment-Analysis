import { FileDown, FileText, PieChart, Send } from 'lucide-react';

import { GlassPanel } from '../components/GlassPanel';

const reports = [
  { title: 'Weekly Brand Health', status: 'ready', format: 'PDF', icon: FileText },
  { title: 'Campaign Sentiment', status: 'processing', format: 'CSV', icon: PieChart },
  { title: 'Executive Summary', status: 'ready', format: 'PDF', icon: Send },
];

export function ReportsPage() {
  return (
    <div className="space-y-6">
      <GlassPanel>
        <div className="mb-5 flex items-center justify-between">
          <div>
            <p className="text-xs uppercase tracking-[0.3em] text-slate-400">Report center</p>
            <h2 className="mt-2 text-xl font-semibold text-white">Saved reports and export queue</h2>
          </div>
          <button className="inline-flex items-center gap-2 rounded-2xl bg-white px-4 py-3 text-sm font-semibold text-slate-950">
            <FileDown className="h-4 w-4" /> Export bundle
          </button>
        </div>
        <div className="grid gap-4 md:grid-cols-3">
          {reports.map((report) => (
            <div key={report.title} className="rounded-3xl border border-white/8 bg-white/5 p-5">
              <report.icon className="h-6 w-6 text-cyan-300" />
              <h3 className="mt-4 text-base font-semibold text-white">{report.title}</h3>
              <p className="mt-2 text-sm text-slate-400">{report.format} report · {report.status}</p>
            </div>
          ))}
        </div>
      </GlassPanel>
    </div>
  );
}
