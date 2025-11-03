import React from "react";
import { Button, Card, Input, Label, Avatar } from "./ui";

export interface SettingsProps {
  className?: string;
}

export function Settings({ className }: SettingsProps) {
  return (
    <div className={`min-h-screen bg-gray-50 ${className}`}>
      {/* Top Navigation Bar */}
      <nav className="bg-white border-b border-gray-200 px-6 py-3">
        <div className="max-w-[1400px] mx-auto flex items-center gap-6">
          {/* Logo */}
          <div className="flex items-center">
            <div className="w-9 h-9 bg-black rounded flex items-center justify-center relative">
              <div className="absolute top-0 left-0 w-2 h-2 bg-white border-2 border-blue-500 rounded-sm"></div>
              <div className="absolute top-0 right-0 w-2 h-2 bg-white border-2 border-blue-500 rounded-sm"></div>
              <div className="absolute bottom-0 left-0 w-2 h-2 bg-white border-2 border-blue-500 rounded-sm"></div>
              <div className="absolute bottom-0 right-0 w-2 h-2 bg-white border-2 border-blue-500 rounded-sm"></div>
              <div className="w-6 h-6 border-2 border-blue-500 rounded-sm"></div>
            </div>
          </div>

          {/* Navigation Links - Right Aligned */}
          <div className="flex items-center gap-8 ml-auto">
            <button className="text-gray-600 hover:text-gray-900 font-medium text-sm">
              Dashboard
            </button>
            <button className="text-gray-600 hover:text-gray-900 font-medium text-sm">
              Orders
            </button>
            <button className="text-gray-600 hover:text-gray-900 font-medium text-sm">
              Products
            </button>
            <button className="text-gray-600 hover:text-gray-900 font-medium text-sm">
              Customers
            </button>
            <button className="text-gray-900 font-semibold text-sm border-b-2 border-black pb-3 -mb-3">
              Settings
            </button>
          </div>

          {/* Right: Upgrade Button + Avatar */}
          <div className="flex items-center gap-3">
            <Button className="bg-black hover:bg-gray-800 text-white px-4 py-2 rounded-md text-sm font-medium flex items-center gap-2">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              Upgrade
            </Button>
            <Avatar className="w-10 h-10" />
          </div>
        </div>
      </nav>

      {/* Settings Header with Search - Full Width with Bottom Border */}
      <div className="border-b border-gray-200">
        <div className="max-w-[1400px] mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
            <div className="relative w-72">
              <svg
                className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <Input
                type="search"
                placeholder="Search"
                className="pl-10 pr-4 py-2 w-full border border-gray-300 rounded-lg text-sm"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Area with Sidebar */}
      <div className="max-w-[1400px] mx-auto flex gap-6 px-6 pt-6 pb-6">
        {/* Left Sidebar Navigation */}
        <aside className="w-56 flex-shrink-0">
          <nav className="space-y-1">
            <button className="w-full text-left px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-100">
              Profile
            </button>
            <button className="w-full text-left px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-100">
              Account
            </button>
            <button className="w-full text-left px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-100">
              Members
            </button>
            <button className="w-full text-left px-3 py-2 rounded-md text-sm font-medium text-gray-900 bg-gray-100">
              Billing
            </button>
            <button className="w-full text-left px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-100">
              Invoices
            </button>
            <button className="w-full text-left px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-100">
              API
            </button>
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1">

          {/* Free Plan Banner */}
          <div className="bg-black text-white p-6 mb-6 flex items-center justify-between rounded-lg">
            <div>
              <h2 className="text-lg font-semibold mb-1">You&apos;re using free plan</h2>
              <p className="text-gray-300 text-sm">
                You can add components to your app by upgrading to the next plan.
              </p>
            </div>
            <button className="bg-white hover:bg-gray-100 active:bg-gray-200 text-black px-5 py-2 rounded-md text-sm font-medium flex items-center gap-2 transition-colors duration-150">
              View plans
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>

          {/* Card Details Section */}
          <Card className="bg-white mb-6 rounded-lg border border-gray-200">
            <div className="px-6 pt-6 mb-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-1">Card details</h2>
              <p className="text-sm text-gray-500">View and update your card details here.</p>
            </div>

            <div className="px-6 space-y-6">
              {/* Row 1: Name on card and Expiry */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="cardName" className="text-sm font-medium text-gray-700 mb-2 block">
                    Name on card
                  </Label>
                  <Input
                    id="cardName"
                    type="text"
                    defaultValue="Kathy Pacheco"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
                  />
                </div>
                <div>
                  <Label htmlFor="expiry" className="text-sm font-medium text-gray-700 mb-2 block">
                    Expiry
                  </Label>
                  <Input
                    id="expiry"
                    type="text"
                    defaultValue="05/2025"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
                  />
                </div>
              </div>

              {/* Row 2: Card number and CVV */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="cardNumber" className="text-sm font-medium text-gray-700 mb-2 block">
                    Card number
                  </Label>
                  <div className="relative">
                    <svg
                      className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
                    </svg>
                    <Input
                      id="cardNumber"
                      type="text"
                      defaultValue="1414 1412 4141 1422"
                      className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md text-sm"
                    />
                  </div>
                </div>
                <div>
                  <Label htmlFor="cvv" className="text-sm font-medium text-gray-700 mb-2 block">
                    CVV
                  </Label>
                  <Input
                    id="cvv"
                    type="text"
                    defaultValue="***"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
                  />
                </div>
              </div>
            </div>

            {/* Save Button */}
            <div className="px-6 mt-6 pt-6 border-t border-gray-200 flex justify-end">
              <Button className="bg-black hover:bg-gray-800 text-white px-6 py-2 rounded-md text-sm font-medium">
                Save
              </Button>
            </div>
          </Card>

          {/* Customer Details Section */}
          <Card className="bg-white rounded-lg border border-gray-200">
            <div className="px-6 pt-6 mb-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-1">Customer details</h2>
              <p className="text-sm text-gray-500">View and update your customer details here.</p>
            </div>

            <div className="px-6 space-y-6">
              {/* Row 1: Client name and Street address */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="clientName" className="text-sm font-medium text-gray-700 mb-2 block">
                    Client name
                  </Label>
                  <Input
                    id="clientName"
                    type="text"
                    defaultValue="Kathy Pacheco"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
                  />
                </div>
                <div>
                  <Label htmlFor="streetAddress" className="text-sm font-medium text-gray-700 mb-2 block">
                    Street adress
                  </Label>
                  <Input
                    id="streetAddress"
                    type="text"
                    defaultValue="2825 Winding Way, Providence, RI 02908"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
                  />
                </div>
              </div>

              {/* Row 2: Email address and City */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="emailAddress" className="text-sm font-medium text-gray-700 mb-2 block">
                    Email address
                  </Label>
                  <div className="relative">
                    <svg
                      className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                    <Input
                      id="emailAddress"
                      type="email"
                      defaultValue="hi@shadcndesign.com"
                      className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md text-sm"
                    />
                  </div>
                </div>
                <div>
                  <Label htmlFor="city" className="text-sm font-medium text-gray-700 mb-2 block">
                    City
                  </Label>
                  <Input
                    id="city"
                    type="text"
                    defaultValue="Providence"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
                  />
                </div>
              </div>

              {/* Row 3: Country and State */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="country" className="text-sm font-medium text-gray-700 mb-2 block">
                    Country
                  </Label>
                  <div className="relative">
                    <select
                      id="country"
                      defaultValue="United States"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm bg-white appearance-none cursor-pointer"
                    >
                      <option>United States</option>
                      <option>Canada</option>
                      <option>United Kingdom</option>
                      <option>Australia</option>
                    </select>
                    <svg
                      className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </div>
                <div>
                  <Label htmlFor="state" className="text-sm font-medium text-gray-700 mb-2 block">
                    State
                  </Label>
                  <div className="relative">
                    <select
                      id="state"
                      defaultValue="Rhode Island"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm bg-white appearance-none cursor-pointer"
                    >
                      <option>Rhode Island</option>
                      <option>California</option>
                      <option>New York</option>
                      <option>Texas</option>
                    </select>
                    <svg
                      className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </div>
              </div>
            </div>

            {/* Save Button */}
            <div className="px-6 mt-6 pt-6 border-t border-gray-200 flex justify-end">
              <Button className="bg-black hover:bg-gray-800 text-white px-6 py-2 rounded-md text-sm font-medium">
                Save
              </Button>
            </div>
          </Card>
        </main>
      </div>
    </div>
  );
}
