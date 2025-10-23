import * as React from 'react';
import { cn } from '@/lib/utils';

interface AvatarProps {
  src?: string;
  alt?: string;
  className?: string;
}

export function Avatar({ src, alt = 'Avatar', className }: AvatarProps) {
  return (
    <div className={cn('relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full bg-zinc-200', className)}>
      {src ? (
        <img src={src} alt={alt} className="aspect-square h-full w-full" />
      ) : (
        <div className="flex h-full w-full items-center justify-center bg-zinc-300 text-zinc-600 text-sm font-medium">
          N
        </div>
      )}
    </div>
  );
}
