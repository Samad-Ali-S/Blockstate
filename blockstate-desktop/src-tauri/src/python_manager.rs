use std::process::{Child, Command};
use std::path::PathBuf;
use log::{info, error};

pub struct PythonManager {
    backend_process: Option<Child>,
    backend_port: u16,
}

impl PythonManager {
    pub fn new() -> Self {
        PythonManager {
            backend_process: None,
            backend_port: 8000,
        }
    }

    pub fn start_backend(&mut self) -> Result<(), String> {
        // Get the path to the Python backend executable
        let backend_path = self.get_backend_path()?;

        info!("Starting Python backend from: {}", backend_path.display());

        // Start the Python FastAPI backend
        let child = Command::new("python")
            .arg(&backend_path)
            .env("BACKEND_PORT", self.backend_port.to_string())
            .env("BACKEND_HOST", "127.0.0.1")
            .spawn()
            .map_err(|e| format!("Failed to start Python backend: {}", e))?;

        self.backend_process = Some(child);
        info!("Python backend started successfully on port {}", self.backend_port);

        Ok(())
    }

    pub fn stop_backend(&mut self) -> Result<(), String> {
        if let Some(mut child) = self.backend_process.take() {
            child.kill().map_err(|e| format!("Failed to kill Python backend: {}", e))?;
            info!("Python backend stopped");
            Ok(())
        } else {
            Err("Backend process not running".to_string())
        }
    }

    pub fn is_running(&self) -> bool {
        self.backend_process.is_some()
    }

    pub fn get_backend_url(&self) -> String {
        format!("http://127.0.0.1:{}", self.backend_port)
    }

    fn get_backend_path(&self) -> Result<PathBuf, String> {
        // Try to find the Python backend in common locations
        let possible_paths = vec![
            // Relative to the app executable
            PathBuf::from("../blockstate-backend/main.py"),
            // Absolute path
            PathBuf::from("C:/blockstate-backend/main.py"),
            // User home directory
            dirs::home_dir()
                .unwrap_or_default()
                .join("blockstate-backend/main.py"),
        ];

        for path in possible_paths {
            if path.exists() {
                return Ok(path);
            }
        }

        Err("Python backend not found in expected locations".to_string())
    }
}

impl Drop for PythonManager {
    fn drop(&mut self) {
        if let Err(e) = self.stop_backend() {
            error!("Error stopping backend on drop: {}", e);
        }
    }
}

// Add the dirs crate for home directory detection
// Add to Cargo.toml: dirs = "5.0"
