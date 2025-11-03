import * as React from 'react';
import { cn } from '@/lib/utils';

interface AvatarProps {
  children?: React.ReactNode;
  className?: string;
}

export function Avatar({ children, className }: AvatarProps) {
  return (
    <div className={cn('relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full bg-zinc-200', className)}>
      {children}
    </div>
  );
}

interface AvatarImageProps extends React.ImgHTMLAttributes<HTMLImageElement> {
  src?: string;
  alt?: string;
}

export function AvatarImage({ src, alt = 'Avatar', className, ...props }: AvatarImageProps) {
  return (
    <img
      src={src}
      alt={alt}
      className={cn('aspect-square h-full w-full object-cover', className)}
      {...props}
    />
  );
}

interface AvatarFallbackProps {
  children?: React.ReactNode;
  className?: string;
}

export function AvatarFallback({ children, className }: AvatarFallbackProps) {
  return (
    <div className={cn('flex h-full w-full items-center justify-center bg-zinc-300 text-zinc-600 text-sm font-medium', className)}>
      {children || 'N'}
    </div>
  );
}
