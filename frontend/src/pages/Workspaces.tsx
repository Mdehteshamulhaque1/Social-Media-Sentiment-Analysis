import { FolderKanban, Users } from 'lucide-react';

import { GlassPanel } from '../components/GlassPanel';

export function WorkspacesPage() {
  return (
    <GlassPanel>
      <div className="mb-5 flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.3em] text-slate-400">Workspaces</p>
          <h2 className="mt-2 text-xl font-semibold text-white">Team structures and ownership</h2>
        </div>
        <div className="flex items-center gap-2 rounded-full border border-white/8 bg-white/6 px-3 py-2 text-sm text-slate-300">
          <Users className="h-4 w-4" /> 18 active analysts
        </div>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        {[
          { name: 'Acme Growth', members: 8, streams: 12 },
          { name: 'Retail Intelligence', members: 12, streams: 18 },
        ].map((workspace) => (
          <div key={workspace.name} className="rounded-3xl border border-white/8 bg-white/5 p-5">
            <FolderKanban className="h-6 w-6 text-cyan-300" />
            <h3 className="mt-4 text-lg font-semibold text-white">{workspace.name}</h3>
            <p className="mt-2 text-sm text-slate-400">{workspace.members} members · {workspace.streams} monitored streams</p>
          </div>
        ))}
      </div>
    </GlassPanel>
  );
}
