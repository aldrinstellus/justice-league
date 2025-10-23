'use client';

import React from 'react';

/**
 * AppHeader - Shared Header Component
 *
 * Extracted from Settings and SettingsProfile screens (poc test project)
 * Figma project: 6Pmf9gCcUccyqbCO9nN6Ts
 *
 * Features:
 * - Full-width border with constrained content (learned pattern from Artemis)
 * - Logo (Z in black square)
 * - Navigation menu with active state
 * - Upgrade button with lightning icon
 * - User avatar with gradient
 *
 * Pattern: full-width-divider + constrained-content-max-w-1400
 */

interface AppHeaderProps {
  /**
   * Current active page for navigation highlighting
   */
  currentPage?: 'Dashboard' | 'Orders' | 'Products' | 'Customers' | 'Settings';
}

export default function AppHeader({ currentPage = 'Dashboard' }: AppHeaderProps) {
  const navItems = ['Dashboard', 'Orders', 'Products', 'Customers', 'Settings'] as const;

  return (
    <div className="w-full bg-white">
      {/* Full-width border (learned pattern from Settings conversion) */}
      <div className="w-full border-b border-zinc-200">
        {/* Constrained content */}
        <div className="max-w-[1400px] mx-auto px-6 py-6 flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-black rounded flex items-center justify-center text-white font-bold">
              Z
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex items-center gap-6 ml-auto mr-6">
            {navItems.map((item) => (
              <a
                key={item}
                href="#"
                className={`text-sm ${
                  currentPage === item
                    ? 'font-medium text-zinc-900'
                    : 'text-zinc-600 hover:text-zinc-900'
                }`}
              >
                {item}
              </a>
            ))}
          </nav>

          {/* Actions */}
          <div className="flex items-center gap-3">
            <button className="px-4 py-2 bg-black text-white text-sm rounded-md hover:bg-zinc-800 flex items-center gap-2">
              <span>⚡</span>
              Upgrade
            </button>
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-pink-500"></div>
          </div>
        </div>
      </div>
    </div>
  );
}
