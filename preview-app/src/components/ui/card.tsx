import * as React from 'react';
import { cn } from '@/lib/utils';

interface CardProps {
  children?: React.ReactNode;
  className?: string;
}

export function Card({ children, className }: CardProps) {
  return (
    <div className={cn('rounded-lg border border-zinc-200 bg-white shadow-md', className)}>
      {children}
    </div>
  );
}
