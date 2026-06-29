use tauri::{AppHandle, SystemTrayEvent, WindowEvent};

pub fn handle_tray_event(app: &AppHandle, event: SystemTrayEvent) {
    match event {
        SystemTrayEvent::LeftClick {
            position: _,
            size: _,
            ..
        } => {
            let window = app.get_window("main");
            if let Some(window) = window {
                let _ = window.show();
                let _ = window.set_focus();
            }
        }
        SystemTrayEvent::RightClick {
            position: _,
            size: _,
            ..
        } => {
            // Right click menu is handled by tauri automatically
        }
        SystemTrayEvent::DoubleClick {
            position: _,
            size: _,
            ..
        } => {
            let window = app.get_window("main");
            if let Some(window) = window {
                let _ = window.show();
                let _ = window.set_focus();
            }
        }
        SystemTrayEvent::MenuItemClick { id, .. } => {
            match id.as_str() {
                "quit" => {
                    std::process::exit(0);
                }
                "hide" => {
                    let window = app.get_window("main");
                    if let Some(window) = window {
                        let _ = window.hide();
                    }
                }
                "show" => {
                    let window = app.get_window("main");
                    if let Some(window) = window {
                        let _ = window.show();
                        let _ = window.set_focus();
                    }
                }
                "settings" => {
                    let window = app.get_window("main");
                    if let Some(window) = window {
                        let _ = window.show();
                        let _ = window.set_focus();
                        // Emit event to navigate to settings
                        let _ = window.emit("navigate", "/settings");
                    }
                }
                _ => {}
            }
        }
        _ => {}
    }
}
