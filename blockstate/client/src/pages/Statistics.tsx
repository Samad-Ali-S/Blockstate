import { Card } from "@/components/ui/card";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

/**
 * Statistics Page
 * 
 * Data dashboard showing focus session metrics and trends.
 * Displays mock data for demonstration.
 */

// Mock data for the last 7 days
const focusHoursData = [
  { day: "Mon", hours: 4.5 },
  { day: "Tue", hours: 5.2 },
  { day: "Wed", hours: 3.8 },
  { day: "Thu", hours: 6.1 },
  { day: "Fri", hours: 4.9 },
  { day: "Sat", hours: 2.3 },
  { day: "Sun", hours: 3.6 },
];

export default function Statistics() {
  // Mock metrics
  const totalFocusHours = focusHoursData.reduce((sum, day) => sum + day.hours, 0);
  const averageHoursPerDay = (totalFocusHours / focusHoursData.length).toFixed(1);
  const topWorkflow = "Deep Coding";
  const distractionsBlocked = 1247;

  return (
    <main className="flex-1 flex flex-col px-8 py-8 bg-gray-50 overflow-y-auto">
      <div className="max-w-6xl w-full space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Statistics</h1>
          <p className="text-gray-500 mt-1">Track your focus sessions and productivity</p>
        </div>

        {/* Metrics Cards */}
        <div className="grid grid-cols-3 gap-6">
          <MetricCard
            title="Total Focus Hours"
            value={totalFocusHours.toFixed(1)}
            unit="hours"
            subtitle="Last 7 days"
          />
          <MetricCard
            title="Top Workflow Used"
            value={topWorkflow}
            unit=""
            subtitle="Most active workflow"
          />
          <MetricCard
            title="Distractions Blocked"
            value={distractionsBlocked.toString()}
            unit="processes"
            subtitle="This week"
          />
        </div>

        {/* Chart */}
        <Card className="bg-white border border-gray-200 rounded-lg shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-6">
            Focus Hours per Day (Last 7 Days)
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={focusHoursData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="day" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#ffffff",
                  border: "1px solid #e5e7eb",
                  borderRadius: "0.5rem",
                }}
                formatter={(value) => `${value} hours`}
              />
              <Legend />
              <Bar dataKey="hours" fill="#2563eb" name="Focus Hours" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>

        {/* Additional Stats */}
        <div className="grid grid-cols-2 gap-6">
          <Card className="bg-white border border-gray-200 rounded-lg shadow-sm p-6">
            <h3 className="text-sm font-semibold text-gray-700 mb-4">
              Daily Average
            </h3>
            <p className="text-3xl font-bold text-blue-600">
              {averageHoursPerDay}
              <span className="text-lg text-gray-500 ml-2">hours</span>
            </p>
            <p className="text-xs text-gray-500 mt-2">Per day average</p>
          </Card>

          <Card className="bg-white border border-gray-200 rounded-lg shadow-sm p-6">
            <h3 className="text-sm font-semibold text-gray-700 mb-4">
              Best Day
            </h3>
            <p className="text-3xl font-bold text-emerald-600">
              6.1
              <span className="text-lg text-gray-500 ml-2">hours</span>
            </p>
            <p className="text-xs text-gray-500 mt-2">Thursday</p>
          </Card>
        </div>
      </div>
    </main>
  );
}

interface MetricCardProps {
  title: string;
  value: string;
  unit: string;
  subtitle: string;
}

function MetricCard({ title, value, unit, subtitle }: MetricCardProps) {
  return (
    <Card className="bg-white border border-gray-200 rounded-lg shadow-sm p-6">
      <p className="text-sm font-medium text-gray-600">{title}</p>
      <div className="mt-3">
        <p className="text-3xl font-bold text-gray-900">
          {value}
          {unit && <span className="text-lg text-gray-500 ml-2">{unit}</span>}
        </p>
      </div>
      <p className="text-xs text-gray-500 mt-2">{subtitle}</p>
    </Card>
  );
}
