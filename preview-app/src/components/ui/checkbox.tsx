import * as React from 'react';
import { cn } from '@/lib/utils';
import { Check } from 'lucide-react';

interface CheckboxProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  onCheckedChange?: (checked: boolean) => void;
}

export const Checkbox = React.forwardRef<HTMLInputElement, CheckboxProps>(
  ({ className, onCheckedChange, onChange, ...props }, ref) => {
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      onChange?.(e);
      onCheckedChange?.(e.target.checked);
    };

    return (
      <div className="relative inline-flex">
        <input
          type="checkbox"
          ref={ref}
          className={cn(
            'peer h-4 w-4 shrink-0 rounded-sm border border-zinc-300 bg-white',
            'focus:outline-none focus:ring-2 focus:ring-zinc-400 focus:ring-offset-2',
            'disabled:cursor-not-allowed disabled:opacity-50',
            'checked:bg-zinc-900 checked:border-zinc-900',
            className
          )}
          onChange={handleChange}
          {...props}
        />
        <Check className="absolute left-0 top-0 h-4 w-4 text-white opacity-0 peer-checked:opacity-100 pointer-events-none" strokeWidth={3} />
      </div>
    );
  }
);

Checkbox.displayName = 'Checkbox';
