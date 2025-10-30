import React from "react";
import { Button, Card, Input, Label, Badge, Avatar, Tabs, Select } from "@/components/ui";

export interface SettingsProps {
  className?: string;
}

export function Settings({ className }: SettingsProps) {
  return (
    <div className="`min-h-screen bg-gray-50 ${className}`">
  <Card className="p-6">
    <div className="grid grid-cols-1 gap-4">
      <div className="space-y-2">
        <Input placeholder="Enter value..." />
      </div>
      <div className="space-y-2">
        <Input placeholder="Enter value..." />
      </div>
      <div className="space-y-2">
        <Input placeholder="Enter value..." />
      </div>
      <div className="space-y-2">
        <Label>Home</Label>
        <Input placeholder="Home" />
      </div>
      <div className="space-y-2">
        <Label>Billing</Label>
        <Input placeholder="Billing" />
      </div>
      <div className="space-y-2">
        <Label>Billing</Label>
        <Input placeholder="Billing" />
      </div>
      <div className="space-y-2">
        <Label>Billing</Label>
        <Input placeholder="Billing" />
      </div>
      <div className="space-y-2">
        <Label>Invoices</Label>
        <Input placeholder="Invoices" />
      </div>
    </div>
  </Card>
    </div>
  );
}
