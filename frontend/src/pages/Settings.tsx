import { BellRing, KeyRound, UserCircle2 } from 'lucide-react';

import { GlassPanel } from '../components/GlassPanel';

export function SettingsPage() {
  return (
    <GlassPanel>
      <div className="grid gap-6 md:grid-cols-3">
        {[
          { icon: UserCircle2, title: 'Profile', description: 'User identity and preferences' },
          { icon: BellRing, title: 'Notifications', description: 'Alert routing and thresholds' },
          { icon: KeyRound, title: 'API keys', description: 'Scoped tokens and access control' },
        ].map((item) => (
          <div key={item.title} className="rounded-3xl border border-white/8 bg-white/5 p-5">
            <item.icon className="h-5 w-5 text-cyan-300" />
            <h3 className="mt-4 text-base font-semibold text-white">{item.title}</h3>
            <p className="mt-2 text-sm text-slate-400">{item.description}</p>
          </div>
        ))}
      </div>
    </GlassPanel>
  );
}
