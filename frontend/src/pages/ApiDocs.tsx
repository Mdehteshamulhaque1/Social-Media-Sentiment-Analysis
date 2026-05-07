import { BookOpen, Code2 } from 'lucide-react';

import { GlassPanel } from '../components/GlassPanel';

const endpoints = [
  { method: 'POST', path: '/api/v1/analysis/text', description: 'Real-time sentiment and NLP analysis' },
  { method: 'POST', path: '/api/v1/analysis/batch', description: 'Batch scoring for CSV ingestion' },
  { method: 'GET', path: '/api/v1/metrics/overview', description: 'API usage and infrastructure metrics' },
];

export function ApiDocsPage() {
  return (
    <div className="space-y-6">
      <GlassPanel>
        <div className="flex items-center gap-3">
          <BookOpen className="h-5 w-5 text-cyan-300" />
          <div>
            <p className="text-xs uppercase tracking-[0.3em] text-slate-400">API documentation viewer</p>
            <h2 className="mt-2 text-xl font-semibold text-white">Versioned API surface</h2>
          </div>
        </div>
        <div className="mt-5 space-y-3">
          {endpoints.map((endpoint) => (
            <div key={endpoint.path} className="flex items-start gap-4 rounded-3xl border border-white/8 bg-white/5 p-4">
              <div className="rounded-2xl bg-white/8 px-3 py-2 text-xs font-semibold text-cyan-300">{endpoint.method}</div>
              <div>
                <p className="font-mono text-sm text-white">{endpoint.path}</p>
                <p className="mt-1 text-sm text-slate-400">{endpoint.description}</p>
              </div>
            </div>
          ))}
        </div>
      </GlassPanel>

      <GlassPanel>
        <div className="flex items-center gap-3 text-cyan-300"><Code2 className="h-5 w-5" />Example response format</div>
        <pre className="mt-4 overflow-auto rounded-3xl bg-slate-950/70 p-5 text-sm text-slate-300">
{`{
  "analysis_id": "a8d2...",
  "sentiment": "positive",
  "confidence": 0.94,
  "keywords": ["launch", "brand", "growth"]
}`}
        </pre>
      </GlassPanel>
    </div>
  );
}
