import { Link } from "wouter";
import {
  LayoutDashboard,
  Zap,
  BarChart3,
  Settings,
  History,
} from "lucide-react";

/**
 * Sidebar Component
 * 
 * Persistent left navigation for BlockState application.
 * Displays branding and navigation items.
 */

interface NavItemProps {
  icon: React.ReactNode;
  label: string;
  href: string;
  active: boolean;
}

function NavItem({ icon, label, href, active }: NavItemProps) {
  return (
    <Link
      href={href}
      className={`flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-150 ${
        active
          ? "bg-blue-50 text-blue-600"
          : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
      }`}
    >
      {icon}
      <span>{label}</span>
    </Link>
  );
}

interface SidebarProps {
  currentPath: string;
}

export default function Sidebar({ currentPath }: SidebarProps) {
  return (
    <aside className="w-64 bg-white border-r border-gray-200 flex flex-col shadow-sm">
      {/* Branding */}
      <div className="px-6 py-8 border-b border-gray-200">
        <h1 className="text-2xl font-bold text-blue-600">BlockState</h1>
        <p className="text-xs text-gray-500 mt-1">Focus Enforcer</p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-6 space-y-2">
        <NavItem
          icon={<LayoutDashboard className="w-5 h-5" />}
          label="Dashboard"
          href="/"
          active={currentPath === "/"}
        />
        <NavItem
          icon={<Zap className="w-5 h-5" />}
          label="Workflows"
          href="/workflows"
          active={currentPath === "/workflows"}
        />
        <NavItem
          icon={<BarChart3 className="w-5 h-5" />}
          label="Statistics"
          href="/statistics"
          active={currentPath === "/statistics"}
        />
        <NavItem
          icon={<History className="w-5 h-5" />}
          label="Session History"
          href="/history"
          active={currentPath === "/history"}
        />
        <NavItem
          icon={<Settings className="w-5 h-5" />}
          label="Settings"
          href="/settings"
          active={currentPath === "/settings"}
        />
      </nav>

      {/* Footer */}
      <div className="px-6 py-4 border-t border-gray-200 text-xs text-gray-500">
        <p>v1.0.0</p>
      </div>
    </aside>
  );
}
