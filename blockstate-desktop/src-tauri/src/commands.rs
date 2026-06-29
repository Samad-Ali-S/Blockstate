use serde::{Deserialize, Serialize};
use tauri::State;
use std::sync::{Arc, Mutex};
use crate::python_manager::PythonManager;
use log::info;

#[derive(Serialize, Deserialize)]
pub struct EnforcerResponse {
    pub success: bool,
    pub message: String,
    pub data: Option<serde_json::Value>,
}

#[derive(Serialize, Deserialize)]
pub struct SystemStats {
    pub cpu_percent: f64,
    pub memory_percent: f64,
    pub disk_percent: f64,
    pub running_processes: usize,
}

/// Start the focus enforcer
#[tauri::command]
pub async fn start_enforcer(
    workflow_id: String,
    duration_minutes: u32,
    python_manager: State<'_, Arc<Mutex<PythonManager>>>,
) -> Result<EnforcerResponse, String> {
    info!("Starting enforcer with workflow: {}", workflow_id);

    let mgr = python_manager.lock().unwrap();
    let backend_url = mgr.get_backend_url();
    drop(mgr);

    let client = reqwest::Client::new();
    let url = format!("{}/api/enforcer/start", backend_url);

    let payload = serde_json::json!({
        "workflow_id": workflow_id,
        "duration_minutes": duration_minutes,
        "strict_mode": false
    });

    match client.post(&url).json(&payload).send().await {
        Ok(response) => {
            match response.json::<EnforcerResponse>().await {
                Ok(data) => Ok(data),
                Err(e) => Err(format!("Failed to parse response: {}", e)),
            }
        }
        Err(e) => Err(format!("Failed to start enforcer: {}", e)),
    }
}

/// Stop the focus enforcer
#[tauri::command]
pub async fn stop_enforcer(
    session_id: String,
    python_manager: State<'_, Arc<Mutex<PythonManager>>>,
) -> Result<EnforcerResponse, String> {
    info!("Stopping enforcer for session: {}", session_id);

    let mgr = python_manager.lock().unwrap();
    let backend_url = mgr.get_backend_url();
    drop(mgr);

    let client = reqwest::Client::new();
    let url = format!("{}/api/enforcer/stop", backend_url);

    let payload = serde_json::json!({
        "session_id": session_id,
        "reason": "User stopped session"
    });

    match client.post(&url).json(&payload).send().await {
        Ok(response) => {
            match response.json::<EnforcerResponse>().await {
                Ok(data) => Ok(data),
                Err(e) => Err(format!("Failed to parse response: {}", e)),
            }
        }
        Err(e) => Err(format!("Failed to stop enforcer: {}", e)),
    }
}

/// Get enforcer status
#[tauri::command]
pub async fn get_enforcer_status(
    python_manager: State<'_, Arc<Mutex<PythonManager>>>,
) -> Result<EnforcerResponse, String> {
    info!("Getting enforcer status");

    let mgr = python_manager.lock().unwrap();
    let backend_url = mgr.get_backend_url();
    drop(mgr);

    let client = reqwest::Client::new();
    let url = format!("{}/api/enforcer/status", backend_url);

    match client.get(&url).send().await {
        Ok(response) => {
            match response.json::<EnforcerResponse>().await {
                Ok(data) => Ok(data),
                Err(e) => Err(format!("Failed to parse response: {}", e)),
            }
        }
        Err(e) => Err(format!("Failed to get enforcer status: {}", e)),
    }
}

/// Get system statistics
#[tauri::command]
pub async fn get_system_stats(
    python_manager: State<'_, Arc<Mutex<PythonManager>>>,
) -> Result<SystemStats, String> {
    info!("Getting system statistics");

    let mgr = python_manager.lock().unwrap();
    let backend_url = mgr.get_backend_url();
    drop(mgr);

    let client = reqwest::Client::new();
    let url = format!("{}/api/system/stats", backend_url);

    match client.get(&url).send().await {
        Ok(response) => {
            match response.json::<serde_json::Value>().await {
                Ok(data) => {
                    if let Some(stats_data) = data.get("data") {
                        let stats = SystemStats {
                            cpu_percent: stats_data
                                .get("cpu_percent")
                                .and_then(|v| v.as_f64())
                                .unwrap_or(0.0),
                            memory_percent: stats_data
                                .get("memory_percent")
                                .and_then(|v| v.as_f64())
                                .unwrap_or(0.0),
                            disk_percent: stats_data
                                .get("disk_percent")
                                .and_then(|v| v.as_f64())
                                .unwrap_or(0.0),
                            running_processes: stats_data
                                .get("running_processes")
                                .and_then(|v| v.as_u64())
                                .unwrap_or(0) as usize,
                        };
                        Ok(stats)
                    } else {
                        Err("Invalid response format".to_string())
                    }
                }
                Err(e) => Err(format!("Failed to parse response: {}", e)),
            }
        }
        Err(e) => Err(format!("Failed to get system stats: {}", e)),
    }
}
