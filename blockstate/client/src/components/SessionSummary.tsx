import { Card } from "@/components/ui/card";
import { TrendingUp, Zap, Clock } from "lucide-react";

/**
 * SessionSummary Component
 * 
 * Displays real-time statistics for the current focus session.
 * Provides immediate feedback on session progress and impact.
 * 
 * Design Rationale:
 * - Real-time stats build confidence in the enforcer
 * - Shows tangible value (distractions blocked, apps used)
 * - Motivates users to complete their session
 * - Creates sense of accomplishment
 */

interface SessionSummaryProps {
  isRunning: boolean;
  timeElapsed: number;
  distractionsBlocked: number;
  appsUsed: string[];
  workflowName: string;
}

export default function SessionSummary({
  isRunning,
  timeElapsed,
  distractionsBlocked,
  appsUsed,
  workflowName,
}: SessionSummaryProps) {
  const formatTime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    if (hours > 0) return `${hours}h ${mins}m`;
    return `${mins}m`;
  };

  return (
    <Card className="bg-white border border-gray-200 rounded-lg shadow-sm p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-gray-900">
          Session Overview
        </h3>
        <span
          className={`px-3 py-1 rounded-full text-xs font-medium ${
            isRunning
              ? "bg-emerald-100 text-emerald-700"
              : "bg-gray-100 text-gray-700"
          }`}
        >
          {isRunning ? "In Progress" : "Paused"}
        </span>
      </div>

      <div className="grid grid-cols-3 gap-4">
        {/* Time Elapsed */}
        <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <Clock className="w-4 h-4 text-blue-600" />
            <p className="text-xs font-medium text-blue-600">Time Elapsed</p>
          </div>
          <p className="text-2xl font-bold text-blue-900">
            {formatTime(timeElapsed)}
          </p>
        </div>

        {/* Distractions Blocked */}
        <div className="bg-gradient-to-br from-red-50 to-red-100 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <Zap className="w-4 h-4 text-red-600" />
            <p className="text-xs font-medium text-red-600">
              Distractions Blocked
            </p>
          </div>
          <p className="text-2xl font-bold text-red-900">
            {distractionsBlocked}
          </p>
        </div>

        {/* Workflow */}
        <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <TrendingUp className="w-4 h-4 text-purple-600" />
            <p className="text-xs font-medium text-purple-600">Workflow</p>
          </div>
          <p className="text-sm font-bold text-purple-900 truncate">
            {workflowName}
          </p>
        </div>
      </div>

      {/* Apps Used */}
      {appsUsed.length > 0 && (
        <div className="mt-6 pt-6 border-t border-gray-200">
          <p className="text-xs font-semibold text-gray-700 mb-3">
            Active Applications
          </p>
          <div className="flex flex-wrap gap-2">
            {appsUsed.map((app) => (
              <span
                key={app}
                className="px-3 py-1 bg-gray-100 text-gray-700 text-xs font-medium rounded-full"
              >
                {app}
              </span>
            ))}
          </div>
        </div>
      )}
    </Card>
  );
}
