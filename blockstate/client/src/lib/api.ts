/**
 * API Service Layer
 * Handles all communication with the Python FastAPI backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export interface ApiResponse<T = any> {
  success: boolean;
  message: string;
  data?: T;
  error?: string;
}

class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseUrl}${endpoint}`;
    const defaultHeaders = {
      'Content-Type': 'application/json',
    };

    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          ...defaultHeaders,
          ...options.headers,
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      return {
        success: false,
        message: 'API request failed',
        error: error instanceof Error ? error.message : String(error),
      };
    }
  }

  // ============ ENFORCER ENDPOINTS ============

  async startEnforcer(workflowId: string, durationMinutes: number, strictMode: boolean = false) {
    return this.request('/enforcer/start', {
      method: 'POST',
      body: JSON.stringify({
        workflow_id: workflowId,
        duration_minutes: durationMinutes,
        strict_mode: strictMode,
      }),
    });
  }

  async stopEnforcer(sessionId: string, reason: string = 'User stopped session') {
    return this.request('/enforcer/stop', {
      method: 'POST',
      body: JSON.stringify({
        session_id: sessionId,
        reason,
      }),
    });
  }

  async getEnforcerStatus() {
    return this.request('/enforcer/status', {
      method: 'GET',
    });
  }

  // ============ WORKFLOWS ENDPOINTS ============

  async getWorkflows() {
    return this.request('/workflows/', {
      method: 'GET',
    });
  }

  async getWorkflow(workflowId: string) {
    return this.request(`/workflows/${workflowId}`, {
      method: 'GET',
    });
  }

  async createWorkflow(workflow: {
    name: string;
    description?: string;
    blocked_processes: string[];
    blocked_domains: string[];
    allowed_processes?: string[];
  }) {
    return this.request('/workflows/', {
      method: 'POST',
      body: JSON.stringify(workflow),
    });
  }

  async updateWorkflow(workflowId: string, workflow: any) {
    return this.request(`/workflows/${workflowId}`, {
      method: 'PUT',
      body: JSON.stringify(workflow),
    });
  }

  async deleteWorkflow(workflowId: string) {
    return this.request(`/workflows/${workflowId}`, {
      method: 'DELETE',
    });
  }

  // ============ SESSIONS ENDPOINTS ============

  async getSessions(limit: number = 50) {
    return this.request(`/sessions/?limit=${limit}`, {
      method: 'GET',
    });
  }

  async getSession(sessionId: string) {
    return this.request(`/sessions/${sessionId}`, {
      method: 'GET',
    });
  }

  async getSessionStats() {
    return this.request('/sessions/stats', {
      method: 'GET',
    });
  }

  async getSessionMetrics(days: number = 7) {
    return this.request(`/sessions/metrics?days=${days}`, {
      method: 'GET',
    });
  }

  // ============ SYSTEM ENDPOINTS ============

  async getSystemStats() {
    return this.request('/system/stats', {
      method: 'GET',
    });
  }

  async getRunningProcesses() {
    return this.request('/system/processes', {
      method: 'GET',
    });
  }

  // ============ CATEGORIZATION ENDPOINTS ============

  async categorizeUrl(url: string) {
    return this.request(`/categorization/url?url=${encodeURIComponent(url)}`, {
      method: 'POST',
    });
  }

  async categorizeApp(appName: string) {
    return this.request(`/categorization/app?app_name=${encodeURIComponent(appName)}`, {
      method: 'POST',
    });
  }
}

// Export singleton instance
export const apiService = new ApiService();
