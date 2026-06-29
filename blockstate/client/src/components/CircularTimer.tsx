/**
 * CircularTimer Component
 * 
 * Animated circular progress indicator for the focus timer.
 * Provides visual confidence that the timer is actively running.
 * 
 * Design Rationale:
 * - Circular progress is more engaging than flat text
 * - Animation provides real-time visual feedback
 * - Large size emphasizes the importance of focus time
 * - Color change (blue → red) signals transition to break
 */

interface CircularTimerProps {
  timeLeft: number;
  initialTime: number;
  isRunning: boolean;
  isBreakTime?: boolean;
}

export default function CircularTimer({
  timeLeft,
  initialTime,
  isRunning,
  isBreakTime = false,
}: CircularTimerProps) {
  const progress = (timeLeft / initialTime) * 100;
  const circumference = 2 * Math.PI * 90; // radius = 90
  const strokeDashoffset = circumference - (progress / 100) * circumference;

  // Format time as MM:SS
  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
  };

  // Determine colors based on state
  const ringColor = isBreakTime ? "#10b981" : "#2563eb"; // emerald for break, blue for focus
  const textColor = isBreakTime ? "text-emerald-600" : "text-blue-600";
  const labelColor = isBreakTime ? "text-emerald-500" : "text-blue-500";

  return (
    <div className="flex flex-col items-center space-y-6">
      {/* Circular Progress Timer */}
      <div className="relative w-72 h-72">
        {/* Background circle */}
        <svg
          className="absolute inset-0 w-full h-full transform -rotate-90"
          viewBox="0 0 200 200"
        >
          <circle
            cx="100"
            cy="100"
            r="90"
            fill="none"
            stroke="#e5e7eb"
            strokeWidth="8"
          />
          {/* Animated progress ring */}
          <circle
            cx="100"
            cy="100"
            r="90"
            fill="none"
            stroke={ringColor}
            strokeWidth="8"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className={`transition-all ${isRunning ? "duration-1000" : "duration-300"}`}
            style={{
              filter: isRunning ? `drop-shadow(0 0 8px ${ringColor})` : "none",
            }}
          />
        </svg>

        {/* Center content */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <div className={`font-mono text-7xl font-bold ${textColor} tracking-tighter`}>
            {formatTime(timeLeft)}
          </div>
          <p className={`text-sm font-medium mt-2 ${labelColor}`}>
            {isBreakTime ? "Break Time" : "Focus Session"}
          </p>
        </div>
      </div>

      {/* Progress percentage indicator */}
      <div className="text-center">
        <p className="text-sm text-gray-500">
          {Math.round(progress)}% Complete
        </p>
        <p className={`text-xs font-medium mt-1 ${isRunning ? "text-emerald-600" : "text-gray-400"}`}>
          {isRunning ? "● Timer Running" : "● Timer Paused"}
        </p>
      </div>
    </div>
  );
}
