'use client';

import React from 'react';

/**
 * SettingsSidebar - Shared Settings Navigation Component
 *
 * Extracted from Settings and SettingsProfile screens (poc test project)
 * Figma project: 6Pmf9gCcUccyqbCO9nN6Ts
 *
 * Features:
 * - Fixed width sidebar (224px)
 * - 6 navigation items
 * - Active state highlighting
 * - Hover states
 *
 * Pattern: sidebar-layout with space-y-1 spacing
 */

interface SettingsSidebarProps {
  /**
   * Currently active settings page
   */
  activePage: 'Profile' | 'Account' | 'Members' | 'Billing' | 'Invoices' | 'API';
}

export default function SettingsSidebar({ activePage }: SettingsSidebarProps) {
  const menuItems = ['Profile', 'Account', 'Members', 'Billing', 'Invoices', 'API'] as const;

  return (
    <aside className="w-[224px] flex-shrink-0">
      <nav className="space-y-1">
        {menuItems.map((item) => (
          <a
            key={item}
            href="#"
            className={`block px-4 py-2 text-sm rounded-md ${
              activePage === item
                ? 'font-medium bg-zinc-100 text-zinc-900'
                : 'text-zinc-600 hover:text-zinc-900 hover:bg-zinc-50'
            }`}
          >
            {item}
          </a>
        ))}
      </nav>
    </aside>
  );
}
