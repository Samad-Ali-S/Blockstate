import { useApp } from "@/contexts/AppContext";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { CheckCircle2, Ban } from "lucide-react";
import { useState, useEffect } from "react";
import { toast } from "sonner";
import CircularTimer from "@/components/CircularTimer";
import EnforcerStatusBanner from "@/components/EnforcerStatusBanner";
import SessionSummary from "@/components/SessionSummary";
import BreakTimer from "@/components/BreakTimer";

/**
 * Enhanced Dashboard Page
 * 
 * Professional focus interface with:
 * - Circular progress timer for visual confidence
 * - Enhanced enforcer status banner
 * - Real-time session statistics
 * - Break timer management
 * - Workflow display
 * - Live backend integration
 */

export default function Dashboard() {
  const {
    isRunning,
    timeLeft,
    initialTime,
    timeElapsed,
    startTimer,
    stopTimer,
    resetTimer,
    isEnforcerActive,
    isBreakActive,
    breakTimeLeft,
    breakDuration,
    startBreak,
    endBreak,
    skipBreak,
    workflows,
    currentWorkflowId,
    setCurrentWorkflowId,
    distractionsBlocked,
    appsUsed,
  } = useApp();

  const [isLoading, setIsLoading] = useState(false);

  const currentWorkflow = workflows.find((w) => w.id === currentWorkflowId);

  const handleStartFocus = async () => {
    setIsLoading(true);
    try {
      await startTimer();
      toast.success("🎯 Focus session started! System enforcer is now active.");
    } catch (error) {
      console.error("Error starting enforcer:", error);
      toast.error("Failed to start focus session");
    } finally {
      setIsLoading(false);
    }
  };

  const handleStopFocus = async () => {
    setIsLoading(true);
    try {
      await stopTimer();
      toast.success("✋ Focus session stopped. Great work!");
    } catch (error) {
      console.error("Error stopping enforcer:", error);
      toast.error("Failed to stop focus session");
    } finally {
      setIsLoading(false);
    }
  };

  const handleResetFocus = () => {
    resetTimer();
    toast.info("🔄 Timer reset to initial duration");
  };

  const handleWorkflowChange = (workflowId: string) => {
    setCurrentWorkflowId(workflowId);
    const workflowName = workflows.find(w => w.id === workflowId)?.name;
    toast.success(`✅ Switched to ${workflowName} workflow`);
  };

  return (
    <div className="flex-1 flex flex-col overflow-hidden bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Main Content */}
      <div className="flex-1 overflow-auto p-8 space-y-8">
        {/* Enforcer Status Banner */}
        <EnforcerStatusBanner
          isActive={isEnforcerActive}
          blockedProcessCount={0}
          allowedAppsCount={0}
          backendConnected={true}
        />

        {/* Timer Section */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Circular Timer */}
          <div className="lg:col-span-2">
            <Card className="p-8 bg-white shadow-lg">
              <div className="flex flex-col items-center justify-center">
                <CircularTimer
                  timeLeft={timeLeft}
                  initialTime={initialTime}
                  isRunning={isRunning}
                />

                {/* Controls */}
                <div className="flex gap-4 mt-8">
                  {!isRunning ? (
                    <Button
                      onClick={handleStartFocus}
                      disabled={isLoading}
                      className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-2 rounded-lg font-semibold transition-all duration-150"
                    >
                      {isLoading ? "Starting..." : "Start Focus"}
                    </Button>
                  ) : (
                    <Button
                      onClick={handleStopFocus}
                      disabled={isLoading}
                      className="bg-red-600 hover:bg-red-700 text-white px-8 py-2 rounded-lg font-semibold transition-all duration-150"
                    >
                      {isLoading ? "Stopping..." : "Stop Focus"}
                    </Button>
                  )}

                  <Button
                    onClick={handleResetFocus}
                    disabled={isLoading}
                    className="bg-gray-600 hover:bg-gray-700 text-white px-8 py-2 rounded-lg font-semibold transition-all duration-150"
                  >
                    Reset
                  </Button>
                </div>

                {/* Status Text */}
                <p className="text-sm text-gray-600 mt-6 text-center">
                  {isRunning
                    ? "🎯 Focus session in progress..."
                    : "Ready to start a focus session"}
                </p>
              </div>
            </Card>
          </div>

          {/* Session Summary */}
          <SessionSummary
            distractionsBlocked={distractionsBlocked}
            timeElapsed={timeElapsed}
            appsUsed={appsUsed}
            isRunning={isRunning}
            workflowName={currentWorkflow?.name || "No Workflow"}
          />
        </div>

        {/* Break Timer (if active) */}
        {isBreakActive && (
          <BreakTimer
            breakTimeLeft={breakTimeLeft}
            isBreakActive={isBreakActive}
            onStartBreak={startBreak}
            onSkipBreak={skipBreak}
            onEndBreak={endBreak}
            suggestedBreakDuration={breakDuration}
          />
        )}

        {/* Workflow Selection */}
        <Card className="p-6 bg-white shadow-md">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Current Workflow</h3>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {workflows.map((workflow) => (
              <button
                key={workflow.id}
                onClick={() => handleWorkflowChange(workflow.id)}
                className={`p-4 rounded-lg border-2 transition-all duration-150 ${
                  currentWorkflowId === workflow.id
                    ? "border-blue-600 bg-blue-50"
                    : "border-gray-200 bg-white hover:border-gray-300"
                }`}
              >
                <p className="font-semibold text-gray-900">{workflow.name}</p>
                <p className="text-xs text-gray-600 mt-2">
                  {workflow.blockedProcesses.length} apps blocked
                </p>
              </button>
            ))}
          </div>
        </Card>

        {/* Current Workflow Details */}
        {currentWorkflow && (
          <Card className="p-6 bg-white shadow-md">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              {currentWorkflow.name} Details
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Allowed Apps */}
              <div>
                <h4 className="font-medium text-gray-700 mb-3 flex items-center gap-2">
                  <CheckCircle2 className="w-5 h-5 text-green-600" />
                  Allowed Apps
                </h4>
                <div className="flex flex-wrap gap-2">
                  {currentWorkflow.allowedApps.map((app) => (
                    <span
                      key={app}
                      className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm"
                    >
                      {app}
                    </span>
                  ))}
                </div>
              </div>

              {/* Blocked Apps */}
              <div>
                <h4 className="font-medium text-gray-700 mb-3 flex items-center gap-2">
                  <Ban className="w-5 h-5 text-red-600" />
                  Blocked Apps
                </h4>
                <div className="flex flex-wrap gap-2">
                  {currentWorkflow.blockedProcesses.map((app) => (
                    <span
                      key={app}
                      className="px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm"
                    >
                      {app}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}
