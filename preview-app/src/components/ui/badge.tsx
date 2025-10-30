import * as React from 'react';
import { cn } from '@/lib/utils';

interface BadgeProps {
  children?: React.ReactNode;
  className?: string;
}

export function Badge({ children, className }: BadgeProps) {
  return (
    <div className={cn('inline-flex items-center rounded-full bg-zinc-900 px-2.5 py-0.5 text-xs font-semibold text-zinc-50', className)}>
      {children}
    </div>
  );
}
