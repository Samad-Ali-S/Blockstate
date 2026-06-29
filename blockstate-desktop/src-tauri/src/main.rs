// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod commands;
mod python_manager;
mod system_tray;

use tauri::{
    CustomMenuItem, Manager, SystemTray, SystemTrayEvent, SystemTrayMenu, SystemTrayMenuItem,
};
use std::sync::{Arc, Mutex};

fn main() {
    env_logger::init();

    let quit = CustomMenuItem::new("quit".to_string(), "Quit BlockState");
    let hide = CustomMenuItem::new("hide".to_string(), "Hide");
    let show = CustomMenuItem::new("show".to_string(), "Show");
    let settings = CustomMenuItem::new("settings".to_string(), "Settings");

    let tray_menu = SystemTrayMenu::new()
        .add_item(show)
        .add_item(hide)
        .add_native_item(SystemTrayMenuItem::Separator)
        .add_item(settings)
        .add_native_item(SystemTrayMenuItem::Separator)
        .add_item(quit);

    let system_tray = SystemTray::new().with_menu(tray_menu);

    let python_manager = Arc::new(Mutex::new(python_manager::PythonManager::new()));

    tauri::Builder::default()
        .system_tray(system_tray)
        .on_system_tray_event(|app, event| {
            system_tray::handle_tray_event(app, event);
        })
        .on_window_event(|event| {
            #[cfg(any(windows, target_os = "macos"))]
            {
                use tauri::WindowEvent;
                if let WindowEvent::CloseRequested { api, .. } = event.event() {
                    event.window().hide().unwrap();
                    api.prevent_close();
                }
            }
        })
        .invoke_handler(tauri::generate_handler![
            commands::start_enforcer,
            commands::stop_enforcer,
            commands::get_enforcer_status,
            commands::get_system_stats,
        ])
        .manage(python_manager.clone())
        .setup(|app| {
            // Start Python backend on app startup
            let python_mgr = app.state::<Arc<Mutex<python_manager::PythonManager>>>();
            let mut mgr = python_mgr.lock().unwrap();
            
            match mgr.start_backend() {
                Ok(_) => {
                    log::info!("Python backend started successfully");
                }
                Err(e) => {
                    log::error!("Failed to start Python backend: {}", e);
                }
            }

            Ok(())
        })
        .on_window_event(|event| {
            if let tauri::WindowEvent::Destroyed = event.event() {
                // Cleanup when window is destroyed
                log::info!("Window destroyed, cleaning up...");
            }
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
