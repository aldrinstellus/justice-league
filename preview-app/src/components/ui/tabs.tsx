import * as React from 'react';
import { cn } from '@/lib/utils';

interface TabsProps {
  children?: React.ReactNode;
  className?: string;
}

export function Tabs({ children, className }: TabsProps) {
  return (
    <div className={cn('flex flex-row space-x-2 border-b border-zinc-200', className)}>
      {children}
    </div>
  );
}
