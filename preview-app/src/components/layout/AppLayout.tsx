'use client';

import React from 'react';
import AppHeader from './AppHeader';

/**
 * AppLayout - Shared Layout Wrapper
 *
 * Extracted from Settings and SettingsProfile screens (poc test project)
 * Figma project: 6Pmf9gCcUccyqbCO9nN6Ts
 *
 * Features:
 * - Full-height page background
 * - App header integration
 * - Constrained content area (max-w-1400)
 * - Consistent spacing (24px / py-6)
 *
 * Pattern: Enterprise layout with constrained-content-max-w-1400
 */

interface AppLayoutProps {
  /**
   * Page content to render
   */
  children: React.ReactNode;

  /**
   * Current active page for header navigation
   */
  currentPage?: 'Dashboard' | 'Orders' | 'Products' | 'Customers' | 'Settings';

  /**
   * Show page header with title and search (optional)
   */
  showPageHeader?: boolean;

  /**
   * Page title (if showPageHeader is true)
   */
  pageTitle?: string;
}

export default function AppLayout({
  children,
  currentPage = 'Dashboard',
  showPageHeader = false,
  pageTitle
}: AppLayoutProps) {
  return (
    <div className="min-h-screen bg-[#fafafa]">
      {/* App Header */}
      <AppHeader currentPage={currentPage} />

      {/* Main Content Area */}
      <div className="max-w-[1400px] mx-auto px-6 py-6">
        {/* Optional Page Header */}
        {showPageHeader && (
          <div className="flex items-center justify-between mb-6">
            <h1 className="text-3xl font-bold text-zinc-900">{pageTitle || currentPage}</h1>
            <div className="relative">
              <input
                type="search"
                placeholder="Search"
                className="w-64 px-4 py-2 border border-zinc-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-black"
              />
              <span className="absolute right-3 top-1/2 -translate-y-1/2 text-zinc-400">🔍</span>
            </div>
          </div>
        )}

        {/* Page Content */}
        {children}
      </div>
    </div>
  );
}
