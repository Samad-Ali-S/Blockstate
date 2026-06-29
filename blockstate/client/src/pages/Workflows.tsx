import { useApp } from "@/contexts/AppContext";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Trash2, Plus, Loader2 } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";

/**
 * Workflows Manager Page
 * 
 * Interface to create, edit, and manage focus workflows.
 * Users can customize allowed apps, sites, and blocked processes.
 * Integrates with backend for persistence.
 */

export default function Workflows() {
  const {
    workflows,
    currentWorkflowId,
    setCurrentWorkflowId,
    updateWorkflow,
    addWorkflow,
    deleteWorkflow,
    isLoading,
  } = useApp();

  const currentWorkflow = workflows.find((w) => w.id === currentWorkflowId);
  const [newAppInput, setNewAppInput] = useState("");
  const [newSiteInput, setNewSiteInput] = useState("");
  const [newProcessInput, setNewProcessInput] = useState("");
  const [isCreatingWorkflow, setIsCreatingWorkflow] = useState(false);
  const [newWorkflowName, setNewWorkflowName] = useState("");

  const handleAddApp = async () => {
    if (!newAppInput.trim() || !currentWorkflow) return;
    const updated = {
      ...currentWorkflow,
      allowedApps: [...currentWorkflow.allowedApps, newAppInput.trim()],
    };
    try {
      await updateWorkflow(updated);
      setNewAppInput("");
      toast.success(`✅ Added "${newAppInput}" to allowed apps`);
    } catch (error) {
      toast.error("Failed to add app");
    }
  };

  const handleAddSite = async () => {
    if (!newSiteInput.trim() || !currentWorkflow) return;
    const updated = {
      ...currentWorkflow,
      allowedSites: [...currentWorkflow.allowedSites, newSiteInput.trim()],
    };
    try {
      await updateWorkflow(updated);
      setNewSiteInput("");
      toast.success(`✅ Added "${newSiteInput}" to allowed sites`);
    } catch (error) {
      toast.error("Failed to add site");
    }
  };

  const handleAddProcess = async () => {
    if (!newProcessInput.trim() || !currentWorkflow) return;
    const updated = {
      ...currentWorkflow,
      blockedProcesses: [
        ...currentWorkflow.blockedProcesses,
        newProcessInput.trim(),
      ],
    };
    try {
      await updateWorkflow(updated);
      setNewProcessInput("");
      toast.success(`✅ Added "${newProcessInput}" to blocked processes`);
    } catch (error) {
      toast.error("Failed to add process");
    }
  };

  const handleRemoveApp = async (app: string) => {
    if (!currentWorkflow) return;
    const updated = {
      ...currentWorkflow,
      allowedApps: currentWorkflow.allowedApps.filter((a) => a !== app),
    };
    try {
      await updateWorkflow(updated);
      toast.success(`✅ Removed "${app}"`);
    } catch (error) {
      toast.error("Failed to remove app");
    }
  };

  const handleRemoveSite = async (site: string) => {
    if (!currentWorkflow) return;
    const updated = {
      ...currentWorkflow,
      allowedSites: currentWorkflow.allowedSites.filter((s) => s !== site),
    };
    try {
      await updateWorkflow(updated);
      toast.success(`✅ Removed "${site}"`);
    } catch (error) {
      toast.error("Failed to remove site");
    }
  };

  const handleRemoveProcess = async (process: string) => {
    if (!currentWorkflow) return;
    const updated = {
      ...currentWorkflow,
      blockedProcesses: currentWorkflow.blockedProcesses.filter(
        (p) => p !== process
      ),
    };
    try {
      await updateWorkflow(updated);
      toast.success(`✅ Removed "${process}"`);
    } catch (error) {
      toast.error("Failed to remove process");
    }
  };

  const handleCreateWorkflow = async () => {
    if (!newWorkflowName.trim()) {
      toast.error("Please enter a workflow name");
      return;
    }

    setIsCreatingWorkflow(true);
    try {
      const newWorkflow = {
        id: newWorkflowName.toLowerCase().replace(/\s+/g, "-"),
        name: newWorkflowName,
        allowedApps: [],
        allowedSites: [],
        blockedProcesses: [],
      };
      await addWorkflow(newWorkflow);
      setNewWorkflowName("");
      toast.success(`✅ Created "${newWorkflowName}" workflow`);
    } catch (error) {
      toast.error("Failed to create workflow");
    } finally {
      setIsCreatingWorkflow(false);
    }
  };

  const handleDeleteWorkflow = async (id: string) => {
    if (confirm("Are you sure you want to delete this workflow?")) {
      try {
        await deleteWorkflow(id);
        toast.success("✅ Workflow deleted");
      } catch (error) {
        toast.error("Failed to delete workflow");
      }
    }
  };

  return (
    <div className="flex-1 flex flex-col overflow-hidden bg-gradient-to-br from-gray-50 to-gray-100">
      <div className="flex-1 overflow-auto p-8 space-y-8">
        {/* Create New Workflow */}
        <Card className="p-6 bg-white shadow-md">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Create New Workflow</h3>
          <div className="flex gap-3">
            <Input
              type="text"
              placeholder="Workflow name (e.g., Deep Work, Gaming, etc.)"
              value={newWorkflowName}
              onChange={(e) => setNewWorkflowName(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && handleCreateWorkflow()}
              disabled={isCreatingWorkflow}
              className="flex-1"
            />
            <Button
              onClick={handleCreateWorkflow}
              disabled={isCreatingWorkflow || isLoading}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-semibold"
            >
              {isCreatingWorkflow ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Creating...
                </>
              ) : (
                <>
                  <Plus className="w-4 h-4 mr-2" />
                  Create
                </>
              )}
            </Button>
          </div>
        </Card>

        {/* Workflows List */}
        <Card className="p-6 bg-white shadow-md">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Your Workflows</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {workflows.map((workflow) => (
              <div
                key={workflow.id}
                className={`p-4 rounded-lg border-2 cursor-pointer transition-all duration-150 ${
                  currentWorkflowId === workflow.id
                    ? "border-blue-600 bg-blue-50"
                    : "border-gray-200 bg-white hover:border-gray-300"
                }`}
                onClick={() => setCurrentWorkflowId(workflow.id)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <p className="font-semibold text-gray-900">{workflow.name}</p>
                    <p className="text-xs text-gray-600 mt-2">
                      {workflow.blockedProcesses.length} blocked • {workflow.allowedApps.length} allowed
                    </p>
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDeleteWorkflow(workflow.id);
                    }}
                    className="text-red-600 hover:text-red-800 p-1"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </Card>

        {/* Edit Current Workflow */}
        {currentWorkflow && (
          <div className="space-y-6">
            <Card className="p-6 bg-white shadow-md">
              <h3 className="text-lg font-semibold text-gray-900 mb-6">
                Edit: {currentWorkflow.name}
              </h3>

              {/* Allowed Apps */}
              <div className="mb-8">
                <h4 className="font-medium text-gray-700 mb-3">Allowed Apps</h4>
                <div className="flex gap-2 mb-4">
                  <Input
                    type="text"
                    placeholder="Add app name..."
                    value={newAppInput}
                    onChange={(e) => setNewAppInput(e.target.value)}
                    onKeyPress={(e) => e.key === "Enter" && handleAddApp()}
                    disabled={isLoading}
                  />
                  <Button
                    onClick={handleAddApp}
                    disabled={isLoading}
                    className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg"
                  >
                    <Plus className="w-4 h-4" />
                  </Button>
                </div>
                <div className="flex flex-wrap gap-2">
                  {currentWorkflow.allowedApps.map((app) => (
                    <div
                      key={app}
                      className="flex items-center gap-2 px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm"
                    >
                      {app}
                      <button
                        onClick={() => handleRemoveApp(app)}
                        disabled={isLoading}
                        className="text-green-600 hover:text-green-800 ml-1"
                      >
                        ×
                      </button>
                    </div>
                  ))}
                </div>
              </div>

              {/* Allowed Sites */}
              <div className="mb-8">
                <h4 className="font-medium text-gray-700 mb-3">Allowed Sites</h4>
                <div className="flex gap-2 mb-4">
                  <Input
                    type="text"
                    placeholder="Add site (e.g., github.com)..."
                    value={newSiteInput}
                    onChange={(e) => setNewSiteInput(e.target.value)}
                    onKeyPress={(e) => e.key === "Enter" && handleAddSite()}
                    disabled={isLoading}
                  />
                  <Button
                    onClick={handleAddSite}
                    disabled={isLoading}
                    className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg"
                  >
                    <Plus className="w-4 h-4" />
                  </Button>
                </div>
                <div className="flex flex-wrap gap-2">
                  {currentWorkflow.allowedSites.map((site) => (
                    <div
                      key={site}
                      className="flex items-center gap-2 px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                    >
                      {site}
                      <button
                        onClick={() => handleRemoveSite(site)}
                        disabled={isLoading}
                        className="text-blue-600 hover:text-blue-800 ml-1"
                      >
                        ×
                      </button>
                    </div>
                  ))}
                </div>
              </div>

              {/* Blocked Processes */}
              <div>
                <h4 className="font-medium text-gray-700 mb-3">Blocked Processes</h4>
                <div className="flex gap-2 mb-4">
                  <Input
                    type="text"
                    placeholder="Add process (e.g., Discord.exe)..."
                    value={newProcessInput}
                    onChange={(e) => setNewProcessInput(e.target.value)}
                    onKeyPress={(e) => e.key === "Enter" && handleAddProcess()}
                    disabled={isLoading}
                  />
                  <Button
                    onClick={handleAddProcess}
                    disabled={isLoading}
                    className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg"
                  >
                    <Plus className="w-4 h-4" />
                  </Button>
                </div>
                <div className="flex flex-wrap gap-2">
                  {currentWorkflow.blockedProcesses.map((process) => (
                    <div
                      key={process}
                      className="flex items-center gap-2 px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm"
                    >
                      {process}
                      <button
                        onClick={() => handleRemoveProcess(process)}
                        disabled={isLoading}
                        className="text-red-600 hover:text-red-800 ml-1"
                      >
                        ×
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
}
