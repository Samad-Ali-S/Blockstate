import { useApp } from "@/contexts/AppContext";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";
import { Calendar, TrendingUp, Flame, Award, Loader2 } from "lucide-react";
import { useEffect, useState } from "react";
import { apiService } from "@/lib/api";

/**
 * Session History Page
 * 
 * Comprehensive productivity dashboard showing:
 * - Historical focus sessions with detailed metrics
 * - Productivity trends and patterns
 * - Workflow effectiveness comparison
 * - Streak tracking and achievements
 * - Real-time backend integration
 * 
 * Design Rationale:
 * - Gamification through streaks and achievements builds habit
 * - Historical data shows long-term progress and patterns
 * - Workflow comparison helps users optimize their focus setup
 * - Visual charts make data more engaging and actionable
 */

export default function SessionHistory() {
  const { sessions, loadSessions } = useApp();
  const [isLoading, setIsLoading] = useState(false);
  const [metrics, setMetrics] = useState<any>(null);
  const [chartData, setChartData] = useState<any[]>([]);

  useEffect(() => {
    loadSessionData();
  }, []);

  const loadSessionData = async () => {
    setIsLoading(true);
    try {
      // Load sessions
      await loadSessions();

      // Load metrics
      const metricsResponse = await apiService.getSessionMetrics(7);
      if (metricsResponse.success) {
        setMetrics(metricsResponse.data);
      }

      // Prepare chart data from sessions
      if (sessions && sessions.length > 0) {
        const groupedByDate = sessions.reduce((acc: any, session: any) => {
          const date = new Date(session.startTime).toLocaleDateString();
          const existing = acc.find((d: any) => d.date === date);
          if (existing) {
            existing.sessions += 1;
            existing.totalDuration += session.duration;
            existing.distractionsBlocked += session.distractionsBlocked;
          } else {
            acc.push({
              date,
              sessions: 1,
              totalDuration: session.duration,
              distractionsBlocked: session.distractionsBlocked,
            });
          }
          return acc;
        }, []);
        setChartData(groupedByDate.slice(-7)); // Last 7 days
      }
    } catch (error) {
      console.error("Failed to load session data:", error);
    } finally {
      setIsLoading(false);
    }
  };

  // Calculate statistics
  const totalSessions = sessions?.length || 0;
  const totalFocusTime = sessions?.reduce((sum: number, s: any) => sum + (s.duration || 0), 0) || 0;
  const totalDistractionsBlocked = sessions?.reduce((sum: number, s: any) => sum + (s.distractionsBlocked || 0), 0) || 0;
  const averageFocusTime = totalSessions > 0 ? Math.round(totalFocusTime / totalSessions) : 0;

  // Calculate streak
  const calculateStreak = () => {
    if (!sessions || sessions.length === 0) return 0;
    let streak = 0;
    const today = new Date();
    for (let i = 0; i < 365; i++) {
      const checkDate = new Date(today);
      checkDate.setDate(checkDate.getDate() - i);
      const dateStr = checkDate.toLocaleDateString();
      if (sessions.some((s: any) => new Date(s.startTime).toLocaleDateString() === dateStr)) {
        streak++;
      } else if (i > 0) {
        break;
      }
    }
    return streak;
  };

  const currentStreak = calculateStreak();

  // Workflow stats
  const workflowStats = sessions?.reduce((acc: any, session: any) => {
    const workflow = session.workflowId || "Unknown";
    const existing = acc.find((w: any) => w.name === workflow);
    if (existing) {
      existing.value += 1;
      existing.totalTime += session.duration;
    } else {
      acc.push({
        name: workflow,
        value: 1,
        totalTime: session.duration,
      });
    }
    return acc;
  }, []) || [];

  const COLORS = ["#3b82f6", "#ef4444", "#10b981", "#f59e0b", "#8b5cf6"];

  if (isLoading && sessions.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100">
        <div className="text-center">
          <Loader2 className="w-12 h-12 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-gray-600">Loading session history...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col overflow-hidden bg-gradient-to-br from-gray-50 to-gray-100">
      <div className="flex-1 overflow-auto p-8 space-y-8">
        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Total Sessions */}
          <Card className="p-6 bg-white shadow-md">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm font-medium">Total Sessions</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">{totalSessions}</p>
              </div>
              <Calendar className="w-12 h-12 text-blue-600 opacity-20" />
            </div>
          </Card>

          {/* Total Focus Time */}
          <Card className="p-6 bg-white shadow-md">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm font-medium">Total Focus Time</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">
                  {Math.floor(totalFocusTime / 60)}h {totalFocusTime % 60}m
                </p>
              </div>
              <TrendingUp className="w-12 h-12 text-green-600 opacity-20" />
            </div>
          </Card>

          {/* Current Streak */}
          <Card className="p-6 bg-white shadow-md">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm font-medium">Current Streak</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">{currentStreak} days</p>
              </div>
              <Flame className="w-12 h-12 text-red-600 opacity-20" />
            </div>
          </Card>

          {/* Distractions Blocked */}
          <Card className="p-6 bg-white shadow-md">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-600 text-sm font-medium">Distractions Blocked</p>
                <p className="text-3xl font-bold text-gray-900 mt-2">{totalDistractionsBlocked}</p>
              </div>
              <Award className="w-12 h-12 text-purple-600 opacity-20" />
            </div>
          </Card>
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Focus Time Trend */}
          <Card className="p-6 bg-white shadow-md">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Focus Time Trend (Last 7 Days)</h3>
            {chartData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="totalDuration"
                    stroke="#3b82f6"
                    name="Minutes"
                    strokeWidth={2}
                  />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-300 flex items-center justify-center text-gray-500">
                No data available
              </div>
            )}
          </Card>

          {/* Distractions Blocked Trend */}
          <Card className="p-6 bg-white shadow-md">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Distractions Blocked (Last 7 Days)</h3>
            {chartData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="distractionsBlocked" fill="#ef4444" name="Blocked" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-300 flex items-center justify-center text-gray-500">
                No data available
              </div>
            )}
          </Card>
        </div>

        {/* Workflow Distribution */}
        {workflowStats.length > 0 && (
          <Card className="p-6 bg-white shadow-md">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Workflow Distribution</h3>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={workflowStats}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, value }) => `${name}: ${value}`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {workflowStats.map((entry: any, index: number) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>

              <div className="space-y-3">
                {workflowStats.map((workflow: any, index: number) => (
                  <div key={workflow.name} className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div
                        className="w-3 h-3 rounded-full"
                        style={{ backgroundColor: COLORS[index % COLORS.length] }}
                      />
                      <span className="text-gray-700 font-medium">{workflow.name}</span>
                    </div>
                    <div className="text-right">
                      <p className="text-gray-900 font-semibold">{workflow.value} sessions</p>
                      <p className="text-gray-600 text-sm">{Math.round(workflow.totalTime)} min</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </Card>
        )}

        {/* Recent Sessions */}
        <Card className="p-6 bg-white shadow-md">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Sessions</h3>
          {sessions && sessions.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-left py-3 px-4 font-semibold text-gray-700">Date</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-700">Workflow</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-700">Duration</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-700">Blocked</th>
                    <th className="text-left py-3 px-4 font-semibold text-gray-700">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {sessions.slice(0, 10).map((session: any) => (
                    <tr key={session.id} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="py-3 px-4 text-gray-700">
                        {new Date(session.startTime).toLocaleDateString()}
                      </td>
                      <td className="py-3 px-4 text-gray-700">{session.workflowId}</td>
                      <td className="py-3 px-4 text-gray-700">{session.duration} min</td>
                      <td className="py-3 px-4 text-gray-700">{session.distractionsBlocked}</td>
                      <td className="py-3 px-4">
                        <Badge className="bg-green-100 text-green-800">Completed</Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              No sessions recorded yet. Start a focus session to see your history!
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
