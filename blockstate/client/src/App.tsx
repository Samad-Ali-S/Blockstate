import { Toaster } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { ThemeProvider } from "./contexts/ThemeContext";
import { AppProvider, useApp } from "./contexts/AppContext";
import { Route, Switch, useLocation } from "wouter";
import ErrorBoundary from "./components/ErrorBoundary";
import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import Workflows from "./pages/Workflows";
import Statistics from "./pages/Statistics";
import SessionHistory from "./pages/SessionHistory";
import Settings from "./pages/Settings";
import NotFound from "./pages/NotFound";

/**
 * BlockState Application
 * 
 * Multi-page React application with:
 * - Global state management via AppContext
 * - Persistent sidebar navigation
 * - Four main pages: Dashboard, Workflows, Statistics, Settings
 * - Background timer that continues running across page navigation
 */

function Router() {
  const [location] = useLocation();

  return (
    <div className="h-screen flex bg-gray-50">
      {/* Persistent Sidebar */}
      <Sidebar currentPath={location} />

      {/* Page Routes */}
      <Switch>
        <Route path="/" component={Dashboard} />
        <Route path="/workflows" component={Workflows} />
        <Route path="/statistics" component={Statistics} />
        <Route path="/history" component={SessionHistory} />
        <Route path="/settings" component={Settings} />
        <Route path="/404" component={NotFound} />
        {/* Final fallback route */}
        <Route component={NotFound} />
      </Switch>
    </div>
  );
}

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider defaultTheme="light">
        <AppProvider>
          <TooltipProvider>
            <Toaster />
            <Router />
          </TooltipProvider>
        </AppProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;
