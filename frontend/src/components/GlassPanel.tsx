import clsx from 'clsx';

export function GlassPanel({ className, children }: { className?: string; children: React.ReactNode }) {
  return (
    <section
      className={clsx(
        'rounded-[28px] border border-white/10 bg-white/7 p-5 shadow-glass backdrop-blur-xl transition duration-300 dark:border-white/8 dark:bg-slate-950/55',
        className,
      )}
    >
      {children}
    </section>
  );
}
