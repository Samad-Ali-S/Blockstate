import { useApp } from "@/contexts/AppContext";
import { Card } from "@/components/ui/card";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { CheckCircle2, Circle, Bell, Clock, Zap } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";

/**
 * Enhanced Settings Page
 * 
 * Comprehensive configuration interface with:
 * - Focus time presets for quick session setup
 * - Notification preferences for break reminders
 * - Application behavior toggles
 * - Backend connection status
 * 
 * Design Rationale:
 * - Presets reduce friction and encourage app usage
 * - Notifications ensure users don't miss break opportunities
 * - Clear settings organization improves discoverability
 * - Visual feedback builds confidence in configuration
 */

export default function Settings() {
  const {
    startAtBoot,
    setStartAtBoot,
    strictMode,
    setStrictMode,
    backendConnected,
    setInitialTime,
  } = useApp();

  const [notificationsEnabled, setNotificationsEnabled] = useState(true);
  const [soundEnabled, setSoundEnabled] = useState(true);
  const [breakReminders, setBreakReminders] = useState(true);
  const [selectedPreset, setSelectedPreset] = useState(25);

  // Focus time presets
  const focusPresets = [
    { label: "15 min", value: 15 * 60 },
    { label: "25 min (Pomodoro)", value: 25 * 60 },
    { label: "45 min", value: 45 * 60 },
    { label: "90 min (Deep Work)", value: 90 * 60 },
  ];

  const handlePresetSelect = (minutes: number) => {
    setInitialTime(minutes);
    setSelectedPreset(minutes / 60);
    toast.success(`Focus duration set to ${minutes / 60} minutes`);
  };

  return (
    <main className="flex-1 flex flex-col px-8 py-8 bg-gray-50 overflow-y-auto">
      <div className="max-w-2xl w-full space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
          <p className="text-gray-500 mt-1">
            Customize your BlockState experience
          </p>
        </div>

        {/* Focus Time Presets */}
        <Card className="bg-white border border-gray-200 rounded-lg shadow-sm p-6">
          <div className="flex items-center gap-2 mb-6">
            <Clock className="w-5 h-5 text-blue-600" />
            <h2 className="text-lg font-semibold text-gray-900">
              Focus Time Presets
            </h2>
          </div>

          <p className="text-sm text-gray-600 mb-4">
            Quickly set your focus duration with these presets
          </p>

          <div className="grid grid-cols-2 gap-3">
            {focusPresets.map((preset) => (
              <Button
                key={preset.value}
                onClick={() => handlePresetSelect(preset.value)}
                className={`py-6 font-semibold transition-all ${
                  selectedPreset === preset.value / 60
                    ? "bg-blue-600 hover:bg-blue-700 text-white"
                    : "bg-gray-100 hover:bg-gray-200 text-gray-900"
                }`}
              >
                {preset.label}
              </Button>
            ))}
          </div>
        </Card>

        {/* Notification Settings */}
        <Card className="bg-white border border-gray-200 rounded-lg shadow-sm p-6">
          <div className="flex items-center gap-2 mb-6">
            <Bell className="w-5 h-5 text-emerald-600" />
            <h2 className="text-lg font-semibold text-gray-900">
              Notifications
            </h2>
          </div>

          <div className="space-y-6">
            {/* Notifications Toggle */}
            <div className="flex items-center justify-between pb-6 border-b border-gray-200">
              <div>
                <Label className="text-sm font-medium text-gray-900">
                  Enable Notifications
                </Label>
                <p className="text-xs text-gray-500 mt-1">
                  Receive desktop notifications for focus sessions
                </p>
              </div>
              <Switch
                checked={notificationsEnabled}
                onCheckedChange={setNotificationsEnabled}
              />
            </div>

            {/* Sound Toggle */}
            <div className="flex items-center justify-between pb-6 border-b border-gray-200">
              <div>
                <Label className="text-sm font-medium text-gray-900">
                  Sound Alerts
                </Label>
                <p className="text-xs text-gray-500 mt-1">
                  Play sound when focus session ends
                </p>
              </div>
              <Switch
                checked={soundEnabled}
                onCheckedChange={setSoundEnabled}
                disabled={!notificationsEnabled}
              />
            </div>

            {/* Break Reminders */}
            <div className="flex items-center justify-between">
              <div>
                <Label className="text-sm font-medium text-gray-900">
                  Break Reminders
                </Label>
                <p className="text-xs text-gray-500 mt-1">
                  Remind me to take a break after each focus session
                </p>
              </div>
              <Switch
                checked={breakReminders}
                onCheckedChange={setBreakReminders}
                disabled={!notificationsEnabled}
              />
            </div>
          </div>
        </Card>

        {/* Application Behavior */}
        <Card className="bg-white border border-gray-200 rounded-lg shadow-sm p-6">
          <div className="flex items-center gap-2 mb-6">
            <Zap className="w-5 h-5 text-purple-600" />
            <h2 className="text-lg font-semibold text-gray-900">
              Application Behavior
            </h2>
          </div>

          <div className="space-y-6">
            {/* Start at Boot Toggle */}
            <div className="flex items-center justify-between pb-6 border-b border-gray-200">
              <div>
                <Label className="text-sm font-medium text-gray-900">
                  Start at System Boot
                </Label>
                <p className="text-xs text-gray-500 mt-1">
                  Automatically launch BlockState when your system starts
                </p>
              </div>
              <Switch
                checked={startAtBoot}
                onCheckedChange={setStartAtBoot}
              />
            </div>

            {/* Strict Mode Toggle */}
            <div className="flex items-center justify-between">
              <div>
                <Label className="text-sm font-medium text-gray-900">
                  Strict Mode
                </Label>
                <p className="text-xs text-gray-500 mt-1">
                  Cannot pause timer once started. Must complete the full session.
                </p>
              </div>
              <Switch
                checked={strictMode}
                onCheckedChange={setStrictMode}
              />
            </div>
          </div>
        </Card>

        {/* Backend Status */}
        <Card className="bg-white border border-gray-200 rounded-lg shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-6">
            System Status
          </h2>

          {/* Backend Connection */}
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div>
                <Label className="text-sm font-medium text-gray-900">
                  Python Backend Connection
                </Label>
                <p className="text-xs text-gray-500 mt-1">
                  Status of the system enforcer backend service
                </p>
              </div>
              <div className="flex items-center gap-2">
                {backendConnected ? (
                  <>
                    <CheckCircle2 className="w-5 h-5 text-emerald-600" />
                    <span className="text-sm font-medium text-emerald-600">
                      Connected
                    </span>
                  </>
                ) : (
                  <>
                    <Circle className="w-5 h-5 text-red-600" />
                    <span className="text-sm font-medium text-red-600">
                      Disconnected
                    </span>
                  </>
                )}
              </div>
            </div>

            {/* API Endpoint Info */}
            <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
              <p className="text-xs font-semibold text-blue-900 mb-2">
                API Configuration
              </p>
              <code className="block bg-white p-2 rounded text-xs font-mono text-gray-700 border border-blue-100 mb-2">
                http://localhost:8000/api
              </code>
              <p className="text-xs text-blue-800">
                Make sure your Python backend is running on this endpoint for
                the enforcer to work.
              </p>
            </div>
          </div>
        </Card>

        {/* About Section */}
        <Card className="bg-gradient-to-r from-gray-50 to-gray-100 border border-gray-200 rounded-lg shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">About</h2>
          <div className="space-y-3 text-sm text-gray-600">
            <div>
              <p className="font-semibold text-gray-900">BlockState</p>
              <p className="text-xs">v1.0.0</p>
            </div>
            <div>
              <p className="font-semibold text-gray-900">Description</p>
              <p className="text-xs leading-relaxed">
                A professional desktop productivity application that enforces
                deep work by controlling system processes via a Python backend.
                Built with React, Tailwind CSS, and modern web technologies.
              </p>
            </div>
            <div>
              <p className="font-semibold text-gray-900">Design Philosophy</p>
              <p className="text-xs leading-relaxed">
                Minimalist Academic Precision inspired by Notion and Linear.
                Focused on clarity, trust, and user confidence in the system
                enforcer.
              </p>
            </div>
          </div>
        </Card>
      </div>
    </main>
  );
}
