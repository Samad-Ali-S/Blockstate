# BlockState Tauri Desktop Wrapper - Setup Guide

This guide explains how to build BlockState as a native Windows .exe application using Tauri.

## Prerequisites

### Required Software
- **Node.js 16+** - Download from https://nodejs.org/
- **Rust** - Download from https://rustup.rs/
- **Visual Studio Build Tools** - Required for Windows development
  - Download from: https://visualstudio.microsoft.com/downloads/
  - Select "Desktop development with C++"

### Verify Installation
```bash
node --version      # Should be v16 or higher
npm --version       # Should be v7 or higher
rustc --version     # Should be 1.56 or higher
cargo --version     # Should be 1.56 or higher
```

## Project Structure

```
blockstate-desktop/
├── src-tauri/                    # Tauri Rust backend
│   ├── src/
│   │   ├── main.rs              # Main Tauri app
│   │   ├── commands.rs          # Frontend commands
│   │   ├── python_manager.rs    # Python subprocess manager
│   │   └── system_tray.rs       # System tray integration
│   ├── Cargo.toml               # Rust dependencies
│   └── build.rs                 # Build script
├── tauri.conf.json              # Tauri configuration
├── package.json                 # Node.js dependencies
└── TAURI_SETUP_GUIDE.md        # This file
```

## Setup Instructions

### Step 1: Install Tauri CLI

```bash
npm install -g @tauri-apps/cli
```

### Step 2: Create Tauri Project Structure

```bash
# Navigate to the blockstate-desktop directory
cd blockstate-desktop

# Install Node.js dependencies
npm install

# Initialize Tauri (if not already done)
tauri init
```

### Step 3: Copy Files

Copy all files from this directory to your local machine:
- `tauri.conf.json` → Root directory
- `src-tauri/` → Root directory
- `package.json` → Root directory

### Step 4: Update Configuration

Edit `tauri.conf.json` to match your setup:

```json
{
  "build": {
    "beforeBuildCommand": "npm run build",
    "beforeDevCommand": "npm run dev",
    "devPath": "http://localhost:5173",
    "frontendDist": "../blockstate/dist"
  }
}
```

**Important**: Update `frontendDist` to point to your React build output directory.

### Step 5: Configure Python Backend Path

Edit `src-tauri/src/python_manager.rs` to set the correct path to your Python backend:

```rust
fn get_backend_path(&self) -> Result<PathBuf, String> {
    let possible_paths = vec![
        PathBuf::from("C:/path/to/blockstate-backend/main.py"),
        // ... other paths
    ];
    // ...
}
```

## Building

### Development Mode

Run the app in development mode with hot reload:

```bash
npm run dev
```

This will:
1. Start the React dev server on http://localhost:5173
2. Start the Tauri app
3. Automatically reload on code changes

### Production Build

Build the Windows .exe installer:

```bash
npm run build
```

This creates:
- `src-tauri/target/release/blockstate.exe` - Standalone executable
- `src-tauri/target/release/bundle/nsis/BlockState-1.0.0-setup.exe` - NSIS installer
- `src-tauri/target/release/bundle/msi/BlockState-1.0.0.msi` - MSI installer

### Build Specific Targets

```bash
# Build NSIS installer only
npm run build:nsis

# Build MSI installer only
npm run build:msi
```

## Features Implemented

### 1. System Tray Integration
- Click tray icon to show/hide window
- Right-click menu with options:
  - Show/Hide
  - Settings
  - Quit

### 2. Python Backend Management
- Automatically starts Python FastAPI backend on app launch
- Manages backend process lifecycle
- Handles graceful shutdown

### 3. Frontend-Backend Communication
- Tauri commands for enforcer control
- HTTP requests to Python backend
- Real-time status updates

### 4. Window Management
- Minimize to system tray
- Remember window size/position
- Responsive design (1200x800 default)

### 5. Auto-Updates
- Check for updates on startup
- Download and install updates
- Configurable update endpoint

## API Commands

### Available Tauri Commands

These commands are exposed to the React frontend:

#### `start_enforcer(workflow_id, duration_minutes)`
Starts the focus enforcer

```javascript
import { invoke } from '@tauri-apps/api/tauri';

const result = await invoke('start_enforcer', {
  workflowId: 'deep-coding',
  durationMinutes: 25
});
```

#### `stop_enforcer(session_id)`
Stops the focus enforcer

```javascript
const result = await invoke('stop_enforcer', {
  sessionId: 'session-123'
});
```

#### `get_enforcer_status()`
Gets current enforcer status

```javascript
const status = await invoke('get_enforcer_status');
```

#### `get_system_stats()`
Gets system statistics

```javascript
const stats = await invoke('get_system_stats');
```

## Troubleshooting

### "Python backend not found"
- Ensure Python backend is in the expected location
- Update `python_manager.rs` with correct path
- Check that `main.py` exists in the backend directory

### "Failed to start Python backend"
- Verify Python 3.8+ is installed
- Check that FastAPI dependencies are installed
- Run backend manually to test: `python main.py`

### Build fails with "Rust not found"
- Install Rust from https://rustup.rs/
- Restart terminal after installation
- Run `rustup update`

### "Visual Studio Build Tools not found"
- Download and install from: https://visualstudio.microsoft.com/downloads/
- Select "Desktop development with C++"
- Restart terminal after installation

### App won't start in development mode
- Ensure React dev server is running on port 5173
- Check `tauri.conf.json` has correct `devPath`
- Run `npm install` to ensure dependencies are installed

## Customization

### Change App Icon

1. Replace icon files in `src-tauri/icons/`:
   - `icon.ico` - Windows icon
   - `32x32.png`, `128x128.png`, etc. - Various sizes

2. Update `tauri.conf.json`:
```json
"icon": [
  "icons/32x32.png",
  "icons/128x128.png",
  "icons/icon.ico"
]
```

### Change App Name

1. Update `tauri.conf.json`:
```json
"package": {
  "productName": "Your App Name",
  "version": "1.0.0"
}
```

2. Update `Cargo.toml`:
```toml
[package]
name = "your-app-name"
```

### Change Window Size

Edit `tauri.conf.json`:
```json
"windows": [
  {
    "width": 1200,
    "height": 800,
    "minWidth": 800,
    "minHeight": 600
  }
]
```

## Distribution

### Create Installer

The build process automatically creates installers:

1. **NSIS Installer** (Recommended for Windows)
   - File: `BlockState-1.0.0-setup.exe`
   - Supports custom installation directory
   - Creates Start Menu shortcuts
   - Creates Desktop shortcut

2. **MSI Installer**
   - File: `BlockState-1.0.0.msi`
   - Enterprise-friendly
   - Windows Update compatible

### Sign Installer (Optional)

For production, sign the installer with a code signing certificate:

1. Update `tauri.conf.json`:
```json
"windows": {
  "certificateThumbprint": "YOUR_CERT_THUMBPRINT",
  "signingIdentity": "YOUR_IDENTITY"
}
```

2. Rebuild: `npm run build`

## Performance Optimization

### Reduce Bundle Size

1. Enable LTO in `Cargo.toml`:
```toml
[profile.release]
lto = true
opt-level = "z"
strip = true
```

2. Minimize React bundle:
```bash
npm run build -- --minify
```

### Startup Time

- Python backend starts asynchronously
- React frontend loads while backend initializes
- Typical startup: 2-3 seconds

## Next Steps

1. **Test the build**: Run `npm run dev` and verify all features work
2. **Create installer**: Run `npm run build` to create .exe
3. **Distribute**: Share the installer with users
4. **Collect feedback**: Monitor user issues and iterate

## Additional Resources

- [Tauri Documentation](https://tauri.app/docs/)
- [Tauri API Reference](https://tauri.app/docs/api/)
- [Rust Book](https://doc.rust-lang.org/book/)
- [React Documentation](https://react.dev/)

## Support

For issues or questions:
1. Check Tauri documentation
2. Review error logs in console
3. Test Python backend separately
4. Verify all prerequisites are installed

---

**BlockState Desktop v1.0.0** - Ready for distribution!
