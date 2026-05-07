import { GlassPanel } from '../components/GlassPanel';

export function AuthPage() {
  return (
    <div className="mx-auto flex min-h-screen max-w-5xl items-center px-5 py-10">
      <GlassPanel className="grid w-full gap-0 overflow-hidden p-0 xl:grid-cols-2">
        <div className="border-b border-white/8 bg-white/5 p-8 xl:border-b-0 xl:border-r">
          <p className="text-xs uppercase tracking-[0.3em] text-slate-400">Access control</p>
          <h2 className="mt-3 text-3xl font-semibold text-white">Secure workspace sign-in</h2>
          <p className="mt-4 max-w-md text-sm leading-7 text-slate-400">JWT-backed authentication, team-level permissions, and audit-ready access flows.</p>
        </div>
        <form className="space-y-4 p-8">
          <div>
            <label className="mb-2 block text-sm text-slate-300">Email</label>
            <input className="w-full rounded-2xl border border-white/10 bg-slate-950/60 px-4 py-3 text-white outline-none placeholder:text-slate-500" placeholder="name@company.com" />
          </div>
          <div>
            <label className="mb-2 block text-sm text-slate-300">Password</label>
            <input type="password" className="w-full rounded-2xl border border-white/10 bg-slate-950/60 px-4 py-3 text-white outline-none placeholder:text-slate-500" placeholder="••••••••" />
          </div>
          <button className="w-full rounded-2xl bg-white px-4 py-3 text-sm font-semibold text-slate-950">Sign in</button>
        </form>
      </GlassPanel>
    </div>
  );
}
