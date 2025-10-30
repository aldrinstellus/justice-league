import * as React from 'react';

interface TableProps {
  children?: React.ReactNode;
  className?: string;
}

export function Table({ children, className = '' }: TableProps) {
  return (
    <table className={`w-full text-sm ${className}`}>
      {children}
    </table>
  );
}
