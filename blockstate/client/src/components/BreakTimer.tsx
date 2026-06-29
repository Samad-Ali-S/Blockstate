import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Coffee, RotateCcw } from "lucide-react";

/**
 * BreakTimer Component
 * 
 * Manages break time after focus session completion.
 * Encourages healthy work-life balance and prevents burnout.
 * 
 * Design Rationale:
 * - Pomodoro technique recommends 5-15 min breaks after focus
 * - Automatic break suggestion reduces decision fatigue
 * - Guided break improves productivity in next focus session
 * - Holistic approach (focus + break) shows app cares about user wellness
 */

interface BreakTimerProps {
  breakTimeLeft: number;
  isBreakActive: boolean;
  onStartBreak: () => void;
  onSkipBreak: () => void;
  onEndBreak: () => void;
  suggestedBreakDuration: number;
}

export default function BreakTimer({
  breakTimeLeft,
  isBreakActive,
  onStartBreak,
  onSkipBreak,
  onEndBreak,
  suggestedBreakDuration,
}: BreakTimerProps) {
  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
  };

  if (!isBreakActive) {
    return (
      <Card className="bg-gradient-to-r from-emerald-50 to-teal-50 border-2 border-emerald-200 rounded-lg shadow-sm p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Coffee className="w-6 h-6 text-emerald-600" />
            <div>
              <p className="font-semibold text-gray-900">
                Great work! Time for a break.
              </p>
              <p className="text-sm text-gray-600 mt-1">
                We recommend a {suggestedBreakDuration}-minute break to recharge.
              </p>
            </div>
          </div>
          <div className="flex gap-3">
            <Button
              onClick={onStartBreak}
              className="bg-emerald-600 hover:bg-emerald-700 text-white"
            >
              Start Break
            </Button>
            <Button
              onClick={onSkipBreak}
              variant="outline"
              className="border-emerald-200 text-emerald-600 hover:bg-emerald-50"
            >
              Skip
            </Button>
          </div>
        </div>
      </Card>
    );
  }

  return (
    <Card className="bg-gradient-to-r from-emerald-50 to-teal-50 border-2 border-emerald-300 rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-emerald-600 mb-1">
            Break in Progress
          </p>
          <p className="text-4xl font-bold text-emerald-900 font-mono">
            {formatTime(breakTimeLeft)}
          </p>
          <p className="text-xs text-emerald-600 mt-2">
            Relax, stretch, or grab water. You've earned it!
          </p>
        </div>
        <div className="flex gap-3">
          <Button
            onClick={onEndBreak}
            className="bg-emerald-600 hover:bg-emerald-700 text-white"
          >
            End Break
          </Button>
          <Button
            onClick={onSkipBreak}
            variant="outline"
            className="border-emerald-200 text-emerald-600 hover:bg-emerald-50"
          >
            <RotateCcw className="w-4 h-4 mr-2" />
            Reset
          </Button>
        </div>
      </div>
    </Card>
  );
}
