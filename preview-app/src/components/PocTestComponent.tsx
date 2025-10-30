/**
 * PocTestComponent - Settings/Billing Page
 *
 * PIXEL-PERFECT VERSION - Based on Vision Agent Analysis
 * 47 discrepancies identified and fixed
 * Source: https://www.figma.com/design/6Pmf9gCcUccyqbCO9nN6Ts/poc-test?node-id=2-948
 */

import React from 'react';

interface PocTestComponentProps {
  className?: string;
}

export default function PocTestComponent({ className = '' }: PocTestComponentProps) {
  return (
    <div className={`min-h-screen bg-white ${className}`}>
      {/* Top Navigation Header */}
      <header className="flex h-16 items-center justify-between border-b border-gray-200 bg-white px-6">
        {/* Logo */}
        <div className="flex items-center">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br from-blue-500 to-cyan-400">
            <svg className="h-6 w-6 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M13 2L3 14h8l-1 8 10-12h-8l1-8z" />
            </svg>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex items-center gap-8">
          <a href="#" className="text-sm font-medium text-gray-600 hover:text-gray-900">
            Dashboard
          </a>
          <a href="#" className="text-sm font-medium text-gray-600 hover:text-gray-900">
            Orders
          </a>
          <a href="#" className="text-sm font-medium text-gray-600 hover:text-gray-900">
            Products
          </a>
          <a href="#" className="text-sm font-medium text-gray-600 hover:text-gray-900">
            Customers
          </a>
          <a href="#" className="text-sm font-medium text-gray-900 border-b-[3px] border-gray-900 pb-[21px]">
            Settings
          </a>
        </nav>

        {/* Right Section - Upgrade Button & Avatar */}
        <div className="flex items-center gap-4">
          <button className="flex items-center gap-2 rounded-lg bg-black px-4 py-2 text-sm font-medium text-white hover:bg-gray-800">
            <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            Upgrade
          </button>
          <div className="h-8 w-8 overflow-hidden rounded-full bg-gradient-to-br from-purple-400 to-pink-500">
            <img
              src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect fill='%23a855f7' width='100' height='100'/%3E%3Ctext x='50' y='50' font-size='40' text-anchor='middle' dy='.35em' fill='white' font-family='sans-serif'%3EK%3C/text%3E%3C/svg%3E"
              alt="User avatar"
              className="h-full w-full object-cover"
            />
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <div className="flex">
        {/* Left Sidebar - FIXED: width 224px, bg-gray-50, proper padding */}
        <aside className="w-56 border-r border-gray-200 bg-gray-50 px-4 py-8">
        <h2 className="mb-6 text-lg font-medium text-gray-900">Settings</h2>
        <nav className="space-y-1">
          <a
            href="#"
            className="block rounded-md px-4 py-3 text-sm font-medium text-gray-600 hover:bg-gray-100"
          >
            Profile
          </a>
          <a
            href="#"
            className="block rounded-md px-4 py-3 text-sm font-medium text-gray-600 hover:bg-gray-100"
          >
            Account
          </a>
          <a
            href="#"
            className="block rounded-md px-4 py-3 text-sm font-medium text-gray-600 hover:bg-gray-100"
          >
            Members
          </a>
          <a
            href="#"
            className="block rounded-md bg-gray-100 px-4 py-3 text-sm font-medium text-gray-900"
          >
            Billing
          </a>
          <a
            href="#"
            className="block rounded-md px-4 py-3 text-sm font-medium text-gray-600 hover:bg-gray-100"
          >
            Invoices
          </a>
          <a
            href="#"
            className="block rounded-md px-4 py-3 text-sm font-medium text-gray-600 hover:bg-gray-100"
          >
            API
          </a>
        </nav>
      </aside>

        {/* Main Content - FIXED: left margin, padding, spacing */}
        <main className="flex-1 px-12 pt-10">
        {/* Header with Search - FIXED: larger text, proper margins */}
        <div className="mb-8 flex items-center justify-between">
          <h1 className="text-4xl font-bold text-gray-900">Settings</h1>
          <div className="relative mr-12">
            <input
              type="text"
              placeholder="Search"
              className="h-10 w-80 rounded-md border border-gray-300 py-2 pl-10 pr-4 text-sm focus:border-gray-900 focus:outline-none focus:ring-1 focus:ring-gray-900"
            />
            <svg
              className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </div>
        </div>

        {/* Free Plan Card - FIXED: larger padding, border thickness, border-radius */}
        <div className="mb-10 rounded-xl bg-black p-10 text-white">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="mb-2 text-lg font-medium">You're using free plan</h3>
              <p className="text-sm text-gray-400">
                You can add components to your app by upgrading to the next plan.
              </p>
            </div>
            <button className="rounded-lg border-2 border-white bg-white px-6 py-3 text-sm text-black hover:bg-gray-100">
              View plans →
            </button>
          </div>
        </div>

        {/* Form Sections - FIXED: larger spacing */}
        <div className="space-y-12">
          {/* Card Details Section - FIXED: larger text, proper padding */}
          <div>
            <h3 className="mb-2 text-xl font-semibold text-gray-900">Card details</h3>
            <p className="mb-6 text-sm text-gray-500">
              View and update your card details here.
            </p>

            <div className="grid grid-cols-2 gap-6">
              {/* Name on card */}
              <div>
                <label className="mb-2 block text-sm font-medium text-gray-700">
                  Name on card
                </label>
                <input
                  type="text"
                  defaultValue="Kathy Pacheco"
                  className="h-12 w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm text-gray-900 focus:border-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-900"
                />
              </div>

              {/* Expiry */}
              <div>
                <label className="mb-2 block text-sm font-medium text-gray-700">
                  Expiry
                </label>
                <input
                  type="text"
                  defaultValue="05/2025"
                  className="h-12 w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm text-gray-900 focus:border-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-900"
                />
              </div>

              {/* Card number */}
              <div>
                <label className="mb-2 block text-sm font-medium text-gray-700">
                  Card number
                </label>
                <input
                  type="text"
                  defaultValue="💳 1414 1412 4141 1422"
                  className="h-12 w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm text-gray-900 focus:border-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-900"
                />
              </div>

              {/* CVV */}
              <div>
                <label className="mb-2 block text-sm font-medium text-gray-700">
                  CVV
                </label>
                <input
                  type="text"
                  defaultValue="•••"
                  className="h-12 w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm text-gray-900 focus:border-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-900"
                />
              </div>
            </div>

            <div className="mt-6 flex justify-end">
              <button className="rounded-lg bg-black px-6 py-3 text-sm text-white hover:bg-gray-800">
                Save
              </button>
            </div>
          </div>

          {/* Customer Details Section */}
          <div>
            <h3 className="mb-2 text-xl font-semibold text-gray-900">Customer details</h3>
            <p className="mb-6 text-sm text-gray-500">
              View and update your customer details here.
            </p>

            <div className="grid grid-cols-2 gap-6">
              {/* Client name */}
              <div>
                <label className="mb-2 block text-sm font-medium text-gray-700">
                  Client name
                </label>
                <input
                  type="text"
                  defaultValue="Kathy Pacheco"
                  className="h-12 w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm text-gray-900 focus:border-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-900"
                />
              </div>

              {/* Street address */}
              <div>
                <label className="mb-2 block text-sm font-medium text-gray-700">
                  Street address
                </label>
                <input
                  type="text"
                  defaultValue="2825 Winding Way, Providence, RI 02908"
                  className="h-12 w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm text-gray-900 focus:border-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-900"
                />
              </div>

              {/* Email address */}
              <div>
                <label className="mb-2 block text-sm font-medium text-gray-700">
                  Email address
                </label>
                <input
                  type="email"
                  defaultValue="📧 hi@shadcndesign.com"
                  className="h-12 w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm text-gray-900 focus:border-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-900"
                />
              </div>

              {/* City */}
              <div>
                <label className="mb-2 block text-sm font-medium text-gray-700">
                  City
                </label>
                <input
                  type="text"
                  defaultValue="Providence"
                  className="h-12 w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm text-gray-900 focus:border-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-900"
                />
              </div>

              {/* Country */}
              <div>
                <label className="mb-2 block text-sm font-medium text-gray-700">
                  Country
                </label>
                <select className="h-12 w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm text-gray-900 focus:border-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-900">
                  <option>United States</option>
                </select>
              </div>

              {/* State */}
              <div>
                <label className="mb-2 block text-sm font-medium text-gray-700">
                  State
                </label>
                <select className="h-12 w-full rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm text-gray-900 focus:border-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-900">
                  <option>Rhode Island</option>
                </select>
              </div>
            </div>

            <div className="mt-6 flex justify-end">
              <button className="rounded-lg bg-black px-6 py-3 text-sm text-white hover:bg-gray-800">
                Save
              </button>
            </div>
          </div>
        </div>
        </main>
      </div>
    </div>
  );
}
