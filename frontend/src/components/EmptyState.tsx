import { Inbox } from 'lucide-react';

import { GlassPanel } from './GlassPanel';

export function EmptyState({ title, description }: { title: string; description: string }) {
  return (
    <GlassPanel className="flex min-h-[240px] items-center justify-center text-center">
      <div className="max-w-sm">
        <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl border border-white/10 bg-white/8 text-slate-300">
          <Inbox className="h-6 w-6" />
        </div>
        <h3 className="text-lg font-semibold text-white dark:text-slate-50">{title}</h3>
        <p className="mt-2 text-sm leading-6 text-slate-400">{description}</p>
      </div>
    </GlassPanel>
  );
}
