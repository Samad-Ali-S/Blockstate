import { AlertCircle, CheckCircle2, Activity, Zap } from "lucide-react";

/**
 * EnforcerStatusBanner Component
 * 
 * Large, confident status display for the system enforcer.
 * Provides real-time feedback that the system is actively protecting focus.
 * 
 * Design Rationale:
 * - Large banner ensures users see enforcer status at a glance
 * - Color coding (green = active, gray = standby) is immediately recognizable
 * - Process count builds confidence that the system is working
 * - Real-time updates show active monitoring
 */

interface EnforcerStatusBannerProps {
  isActive: boolean;
  blockedProcessCount?: number;
  allowedAppsCount?: number;
  backendConnected?: boolean;
}

export default function EnforcerStatusBanner({
  isActive,
  blockedProcessCount = 0,
  allowedAppsCount = 0,
  backendConnected = true,
}: EnforcerStatusBannerProps) {
  return (
    <div
      className={`w-full rounded-lg shadow-md p-6 border-2 transition-all duration-300 ${
        isActive
          ? "bg-gradient-to-r from-emerald-50 to-emerald-100 border-emerald-300"
          : "bg-gradient-to-r from-gray-50 to-gray-100 border-gray-300"
      }`}
    >
      <div className="flex items-center justify-between">
        {/* Status Info */}
        <div className="flex items-center gap-4">
          <div className="relative">
            {isActive ? (
              <>
                <CheckCircle2 className="w-10 h-10 text-emerald-600" />
                <div className="absolute inset-0 animate-pulse">
                  <CheckCircle2 className="w-10 h-10 text-emerald-600 opacity-50" />
                </div>
              </>
            ) : (
              <Activity className="w-10 h-10 text-gray-400" />
            )}
          </div>

          <div>
            <p className="text-sm font-semibold text-gray-900">
              System Enforcer: {" "}
              <span
                className={
                  isActive ? "text-emerald-600 font-bold" : "text-gray-500"
                }
              >
                {isActive ? "ACTIVE" : "STANDBY"}
              </span>
            </p>
            <p className="text-xs text-gray-600 mt-1">
              {isActive
                ? `Monitoring ${blockedProcessCount} blocked processes & ${allowedAppsCount} allowed apps`
                : "Ready to enforce focus when you start a session"}
            </p>
          </div>
        </div>

        {/* Backend Status */}
        <div className="flex items-center gap-2">
          {backendConnected ? (
            <>
              <Zap className="w-5 h-5 text-emerald-600" />
              <span className="text-xs font-medium text-emerald-600">
                Backend Connected
              </span>
            </>
          ) : (
            <>
              <AlertCircle className="w-5 h-5 text-red-600" />
              <span className="text-xs font-medium text-red-600">
                Backend Disconnected
              </span>
            </>
          )}
        </div>
      </div>

      {/* Process Monitoring Details */}
      {isActive && (
        <div className="mt-4 pt-4 border-t border-emerald-200 grid grid-cols-2 gap-4">
          <div className="text-xs">
            <p className="text-gray-600">Blocked Processes</p>
            <p className="text-lg font-bold text-emerald-600">
              {blockedProcessCount}
            </p>
          </div>
          <div className="text-xs">
            <p className="text-gray-600">Allowed Applications</p>
            <p className="text-lg font-bold text-emerald-600">
              {allowedAppsCount}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
