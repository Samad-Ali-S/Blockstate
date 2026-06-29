import React, { createContext, useContext, useEffect, useState } from "react";

/**
 * AppContext - Global State Management for BlockState
 * 
 * Manages:
 * - Timer state (running, time left, initial time, elapsed time)
 * - Break timer state (for post-focus recovery)
 * - System Enforcer status (active/standby)
 * - Current workflow selection
 * - Session tracking (distractions blocked, apps used)
 * - Workflow data
 */

export interface Workflow {
  id: string;
  name: string;
  allowedApps: string[];
  allowedSites: string[];
  blockedProcesses: string[];
}

export interface AppContextType {
  // Timer state
  isRunning: boolean;
  timeLeft: number;
  initialTime: number;
  timeElapsed: number;
  startTimer: () => void;
  stopTimer: () => void;
  resetTimer: () => void;
  setInitialTime: (time: number) => void;

  // Break timer state
  isBreakActive: boolean;
  breakTimeLeft: number;
  breakDuration: number;
  startBreak: (duration?: number) => void;
  endBreak: () => void;
  skipBreak: () => void;

  // Enforcer state
  isEnforcerActive: boolean;
  setEnforcerActive: (active: boolean) => void;

  // Workflow state
  workflows: Workflow[];
  currentWorkflowId: string;
  setCurrentWorkflowId: (id: string) => void;
  updateWorkflow: (workflow: Workflow) => void;
  addWorkflow: (workflow: Workflow) => void;
  deleteWorkflow: (id: string) => void;

  // Settings
  startAtBoot: boolean;
  setStartAtBoot: (value: boolean) => void;
  strictMode: boolean;
  setStrictMode: (value: boolean) => void;
  backendConnected: boolean;
  setBackendConnected: (value: boolean) => void;

  // Session tracking
  distractionsBlocked: number;
  setDistractionsBlocked: (count: number) => void;
  appsUsed: string[];
  addAppUsed: (app: string) => void;
  sessions: any[];
  loadSessions: () => Promise<void>;

  // Loading state
  isLoading: boolean;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  // Timer state
  const [isRunning, setIsRunning] = useState(false);
  const [timeLeft, setTimeLeft] = useState(25 * 60); // 25 minutes
  const [initialTime, setInitialTime] = useState(25 * 60);
  const [timeElapsed, setTimeElapsed] = useState(0);

  // Break timer state
  const [isBreakActive, setIsBreakActive] = useState(false);
  const [breakTimeLeft, setBreakTimeLeft] = useState(5 * 60); // 5 minutes default
  const [breakDuration, setBreakDuration] = useState(5 * 60);

  // Enforcer state
  const [isEnforcerActive, setEnforcerActive] = useState(false);

  // Workflow state
  const [workflows, setWorkflows] = useState<Workflow[]>([
    {
      id: "deep-coding",
      name: "Deep Coding",
      allowedApps: ["VS Code", "GitHub", "StackOverflow"],
      allowedSites: ["github.com", "stackoverflow.com", "docs.python.org"],
      blockedProcesses: ["Discord.exe", "Steam.exe", "Spotify.exe"],
    },
    {
      id: "exam-study",
      name: "Exam Study",
      allowedApps: ["Notion", "PDF Reader", "Calculator"],
      allowedSites: ["notion.so", "wikipedia.org"],
      blockedProcesses: ["Discord.exe", "Steam.exe", "Spotify.exe", "Chrome.exe"],
    },
    {
      id: "reading",
      name: "Reading",
      allowedApps: ["PDF Reader", "Browser"],
      allowedSites: ["medium.com", "arxiv.org", "scholar.google.com"],
      blockedProcesses: ["Discord.exe", "Steam.exe", "Spotify.exe"],
    },
  ]);
  const [currentWorkflowId, setCurrentWorkflowId] = useState("deep-coding");

  // Settings
  const [startAtBoot, setStartAtBoot] = useState(false);
  const [strictMode, setStrictMode] = useState(false);
  const [backendConnected, setBackendConnected] = useState(true);

  // Session tracking
  const [distractionsBlocked, setDistractionsBlocked] = useState(0);
  const [appsUsed, setAppsUsed] = useState<string[]>([]);
  const [sessions, setSessions] = useState<any[]>([]);

  // Load sessions from backend
  const loadSessions = async () => {
    // Mock implementation - replace with actual API call
    setSessions([]);
  };

  // Timer countdown effect
  useEffect(() => {
    let interval: NodeJS.Timeout;

    if (isRunning && timeLeft > 0) {
      interval = setInterval(() => {
        setTimeLeft((prev) => {
          setTimeElapsed((elapsed) => elapsed + 1);
          if (prev <= 1) {
            setIsRunning(false);
            setEnforcerActive(false);
            setIsBreakActive(true);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    } else if (timeLeft === 0 && isRunning) {
      setIsRunning(false);
      setEnforcerActive(false);
      setIsBreakActive(true);
    }

    return () => clearInterval(interval);
  }, [isRunning, timeLeft]);

  // Break timer countdown effect
  useEffect(() => {
    let interval: NodeJS.Timeout;

    if (isBreakActive && breakTimeLeft > 0) {
      interval = setInterval(() => {
        setBreakTimeLeft((prev) => {
          if (prev <= 1) {
            setIsBreakActive(false);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }

    return () => clearInterval(interval);
  }, [isBreakActive, breakTimeLeft]);

  // Sync enforcer state with timer
  useEffect(() => {
    if (isRunning) {
      setEnforcerActive(true);
    } else if (!strictMode) {
      setEnforcerActive(false);
    }
  }, [isRunning, strictMode]);

  const startTimer = () => {
    setIsRunning(true);
  };

  const stopTimer = () => {
    if (!strictMode) {
      setIsRunning(false);
    }
  };

  const resetTimer = () => {
    setIsRunning(false);
    setTimeLeft(initialTime);
    setTimeElapsed(0);
    setIsBreakActive(false);
    setBreakTimeLeft(breakDuration);
    setDistractionsBlocked(0);
    setAppsUsed([]);
  };

  const startBreak = (duration?: number) => {
    const breakLen = duration || breakDuration;
    setBreakTimeLeft(breakLen);
    setIsBreakActive(true);
  };

  const endBreak = () => {
    setIsBreakActive(false);
    setBreakTimeLeft(breakDuration);
  };

  const skipBreak = () => {
    setIsBreakActive(false);
    setBreakTimeLeft(breakDuration);
  };

  const addAppUsed = (app: string) => {
    setAppsUsed((prev) => {
      if (!prev.includes(app)) {
        return [...prev, app];
      }
      return prev;
    });
  };

  const updateWorkflow = (workflow: Workflow) => {
    setWorkflows((prev) =>
      prev.map((w) => (w.id === workflow.id ? workflow : w))
    );
  };

  const addWorkflow = (workflow: Workflow) => {
    setWorkflows((prev) => [...prev, workflow]);
  };

  const deleteWorkflow = (id: string) => {
    setWorkflows((prev) => prev.filter((w) => w.id !== id));
    if (currentWorkflowId === id && workflows.length > 0) {
      setCurrentWorkflowId(workflows[0].id);
    }
  };

  const value: AppContextType = {
    isRunning,
    timeLeft,
    initialTime,
    timeElapsed,
    startTimer,
    stopTimer,
    resetTimer,
    setInitialTime,
    isBreakActive,
    breakTimeLeft,
    breakDuration,
    startBreak,
    endBreak,
    skipBreak,
    isEnforcerActive,
    setEnforcerActive,
    workflows,
    currentWorkflowId,
    setCurrentWorkflowId,
    updateWorkflow,
    addWorkflow,
    deleteWorkflow,
    startAtBoot,
    setStartAtBoot,
    strictMode,
    setStrictMode,
    backendConnected,
    setBackendConnected,
    distractionsBlocked,
    setDistractionsBlocked,
    appsUsed,
    addAppUsed,
    sessions,
    loadSessions,
    isLoading: false,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};

export const useApp = (): AppContextType => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error("useApp must be used within an AppProvider");
  }
  return context;
};
