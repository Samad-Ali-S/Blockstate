# BlockState: Complete Local Setup Guide

## Step-by-Step Instructions to Run on Your Laptop

**Target**: Windows 10/11 with VS Code**Time Required**: 30-45 minutes**Difficulty**: Beginner-Friendly

---

## 📋 Prerequisites Checklist

Before starting, make sure you have:

- [x] Windows 10 or Windows 11

- [x] At least 4GB RAM available

- [x] 2GB free disk space

- [x] Internet connection

- [x] Administrator access (for hosts file modification)

---

## Step 1: Install Required Software

### 1.1 Install Node.js (Required for Frontend)

1. Go to [https://nodejs.org/](https://nodejs.org/)

1. Download **LTS version** (Long Term Support)

1. Run the installer

1. **Important**: Check the box "Automatically install the necessary tools for native modules"

1. Click "Install"

1. Accept the User Account Control prompt

1. Wait for installation to complete (5-10 minutes)

**Verify Installation**:

```bash
node --version
npm --version
```

You should see version numbers like `v22.x.x` and `10.x.x`

---

### 1.2 Install Python (Required for Backend)

1. Go to [https://www.python.org/downloads/](https://www.python.org/downloads/)

1. Download **Python 3.11 or higher**

1. Run the installer

1. **IMPORTANT**: Check the box **"Add Python to PATH"** (at the bottom)

1. Click "Install Now"

1. Wait for installation to complete

**Verify Installation**:

```bash
python --version
pip --version
```

You should see version numbers like `Python 3.11.x` and `pip 23.x.x`

---

### 1.3 Install Git (Required for Version Control)

1. Go to [https://git-scm.com/download/win](https://git-scm.com/download/win)

1. Download the installer

1. Run the installer

1. Click "Next" through all prompts (default settings are fine)

1. Click "Install"

**Verify Installation**:

```bash
git --version
```

You should see version like `git version 2.x.x`

---

### 1.4 Install VS Code (Required for Development)

1. Go to [https://code.visualstudio.com/](https://code.visualstudio.com/)

1. Download for Windows

1. Run the installer

1. Click "Next" through all prompts

1. Click "Install"

1. Launch VS Code

**Recommended VS Code Extensions**:

- Python (by Microsoft)

- Pylance (by Microsoft)

- ES7+ React/Redux/React-Native snippets (by dsznajder.es7-react-js-snippets)

- Tailwind CSS IntelliSense (by bradlc.vscode-tailwindcss)

- Thunder Client or REST Client (for API testing)

---

## Step 2: Download BlockState Project Files

### 2.1 Create Project Folder

1. Open File Explorer

1. Navigate to a location where you want to store the project (e.g., `C:\Users\YourName\Documents`)

1. Create a new folder called `blockstate-project`

---

### 2.2 Download Files from Sandbox

I'll provide you with the project files. You have two options:

**Option A: Download as ZIP (Easier)**

- I'll create a ZIP file with all project files

- Extract it to `C:\Users\YourName\Documents\blockstate-project`

**Option B: Clone from GitHub (If you set up a repo)**

```bash
cd C:\Users\YourName\Documents
git clone https://github.com/yourusername/blockstate.git blockstate-project
cd blockstate-project
```

---

## Step 3: Set Up Frontend (React Dashboard )

### 3.1 Open Frontend Project in VS Code

1. Open VS Code

1. Click **File → Open Folder**

1. Navigate to `blockstate-project\blockstate`

1. Click **Select Folder**

---

### 3.2 Install Frontend Dependencies

1. In VS Code, open the Terminal: **Ctrl + `** (backtick)

1. You should see the terminal at the bottom

1. Make sure you're in the `blockstate` folder (you should see `blockstate>` in terminal)

1. Type the following command and press Enter:

```bash
pnpm install
```

**What this does**: Downloads all React libraries and dependencies (takes 2-5 minutes)

**If you get an error about "pnpm not found"**:

```bash
npm install -g pnpm
```

Then try `pnpm install` again.

---

### 3.3 Start Frontend Development Server

In the same terminal, type:

```bash
pnpm dev
```

**Expected Output**:

```
VITE v7.1.9  ready in 412 ms

➜  Local:   http://localhost:3000/
➜  Network: use --host to expose
```

**✅ Frontend is now running!** You can access it at `http://localhost:3000`

---

## Step 4: Set Up Backend (Python FastAPI )

### 4.1 Open New Terminal for Backend

1. In VS Code, click the **+** button in the terminal to open a new terminal

1. You now have two terminals: one for frontend, one for backend

---

### 4.2 Navigate to Backend Folder

In the new terminal, type:

```bash
cd ..\blockstate-backend
```

**Verify**: You should see `blockstate-backend>` in the terminal

---

### 4.3 Create Python Virtual Environment

A virtual environment keeps Python packages isolated for this project.

```bash
python -m venv venv
```

**This creates a ****`venv`**** folder** (takes 30 seconds)

---

### 4.4 Activate Virtual Environment

**On Windows**:

```bash
venv\Scripts\activate
```

**Expected Output**: You should see `(venv)` at the start of the terminal line:

```
(venv) blockstate-backend>
```

---

### 4.5 Install Backend Dependencies

```bash
pip install -r requirements.txt
```

**What this does**: Installs FastAPI, psutil, and other Python libraries (takes 2-5 minutes)

---

### 4.6 Start Backend Server

```bash
python main.py
```

**Expected Output**:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit )
INFO:     Application startup complete
```

**✅ Backend is now running!** You can access the API at `http://localhost:8000`

---

## Step 5: Test the Full Application

### 5.1 Open Frontend in Browser

1. Open your web browser (Chrome, Edge, Firefox )

1. Go to `http://localhost:3000`

1. You should see the BlockState dashboard with:
  - Sidebar on the left
  - Circular timer in the center
  - Enforcer status banner at the top

---

### 5.2 Test Backend Connection

1. In another browser tab, go to `http://localhost:8000/docs`

1. You should see the **Swagger UI** - interactive API documentation

1. Try clicking on one of the endpoints (e.g., `/api/enforcer/status` )

1. Click **"Try it out"** → **"Execute"**

1. You should see a response with status and data

---

### 5.3 Test Frontend-Backend Connection

1. Go back to `http://localhost:3000`

1. Click **"Start Focus"** button

1. Check the terminal running the backend - you should see API requests logged

1. The timer should start counting down

---

## Step 6: Development Workflow

### 6.1 Making Changes to Frontend

1. Edit any file in `blockstate/client/src/`

1. Save the file (Ctrl + S )

1. The browser will **automatically refresh** with your changes

1. Check the terminal for any TypeScript errors

---

### 6.2 Making Changes to Backend

1. Edit any file in `blockstate-backend/`

1. Save the file

1. The backend will **automatically reload** (you'll see "Application startup complete" in terminal)

1. Refresh the browser to see changes

---

### 6.3 Viewing Console Logs

**Frontend Logs**:

- Open browser DevTools: **F12**

- Go to **Console** tab

- You'll see all React logs and errors

**Backend Logs**:

- Check the terminal running `python main.py`

- All API requests and errors are logged there

---

## Step 7: Stopping the Application

### To Stop Frontend:

1. Click in the frontend terminal

1. Press **Ctrl + C**

1. Type **Y** and press Enter

### To Stop Backend:

1. Click in the backend terminal

1. Press **Ctrl + C**

---

## Step 8: Restarting the Application

### Next Time You Want to Work on BlockState:

1. Open VS Code

1. Open the `blockstate-project` folder

1. Open Terminal: **Ctrl + `**

1. Split terminal into two (click the split icon)

**Terminal 1 - Frontend**:

```bash
cd blockstate
pnpm dev
```

**Terminal 2 - Backend**:

```bash
cd blockstate-backend
venv\Scripts\activate
python main.py
```

1. Open browser to `http://localhost:3000`

---

## Troubleshooting

### Problem: "pnpm: command not found"

**Solution**:

```bash
npm install -g pnpm
```

Then try `pnpm install` again.

---

### Problem: "Python: command not found"

**Solution**:

1. Make sure Python is installed

1. Restart VS Code completely

1. Open a new terminal in VS Code

1. Try `python --version` again

If still not working:

- Go to Settings → Environment Variables

- Add Python to PATH manually

- Restart VS Code

---

### Problem: "Port 3000 already in use"

**Solution**: Another application is using port 3000

```bash
# Find what's using port 3000
netstat -ano | findstr :3000

# Kill the process (replace PID with the number shown )
taskkill /PID <PID> /F
```

Then try `pnpm dev` again.

---

### Problem: "Port 8000 already in use"

**Solution**: Another application is using port 8000

```bash
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill the process
taskkill /PID <PID> /F
```

Then try `python main.py` again.

---

### Problem: "Cannot modify hosts file - Permission denied"

**Solution**: Run VS Code as Administrator

1. Right-click VS Code icon

1. Click **"Run as administrator"**

1. Click **"Yes"** on the User Account Control prompt

1. Try again

---

### Problem: Frontend shows blank page

**Solution**:

1. Press **F12** to open DevTools

1. Check the **Console** tab for errors

1. Check the **Network** tab to see if API calls are failing

1. Make sure backend is running on port 8000

---

### Problem: "Cannot connect to backend"

**Solution**:

1. Make sure backend is running: `python main.py`

1. Check if port 8000 is open: `http://localhost:8000/docs`

1. Check browser console (F12 ) for CORS errors

1. Restart both frontend and backend

---

## Advanced: VS Code Settings

### 4.1 Format Code on Save

1. Open VS Code Settings: **Ctrl + ,**

1. Search for "format on save"

1. Check the box for **"Editor: Format On Save"**

Now your code will automatically format when you save!

---

### 4.2 Set Up Python Linting

1. Open VS Code Terminal: **Ctrl + `**

1. Install pylint:

```bash
pip install pylint
```

1. Open Settings: **Ctrl + ,**

1. Search for "python linting"

1. Check **"Python › Linting: Enabled"**

---

### 4.3 Useful Keyboard Shortcuts

| Shortcut | Action |
| --- | --- |
| Ctrl + ` | Toggle Terminal |
| Ctrl + S | Save File |
| Ctrl + Shift + P | Command Palette |
| Ctrl + / | Comment/Uncomment |
| Alt + Up/Down | Move Line Up/Down |
| Ctrl + D | Select Next Occurrence |
| F12 | Open Browser DevTools |

---

## Next Steps After Setup

### 1. Explore the Dashboard

- Try starting a focus session

- Check the circular timer

- Look at the workflow cards

### 2. Test the Workflows Page

- Create a new workflow

- Add some apps and sites

- Edit and delete workflows

### 3. Check the API

- Go to `http://localhost:8000/docs`

- Try different API endpoints

- See the request/response format

### 4. Make Your First Change

- Edit `blockstate/client/src/pages/Dashboard.tsx`

- Change the timer duration from 25 to 30 minutes

- Save and see the change in browser

### 5. Read the Handover Document

- Open `BLOCKSTATE_HANDOVER_DOCUMENT.md`

- Understand the architecture

- Learn about all components

---

## Quick Reference: Terminal Commands

```bash
# Frontend
cd blockstate
pnpm install          # Install dependencies
pnpm dev             # Start dev server
pnpm build           # Build for production
pnpm check           # Check TypeScript errors

# Backend
cd blockstate-backend
python -m venv venv  # Create virtual environment
venv\Scripts\activate # Activate virtual environment
pip install -r requirements.txt  # Install dependencies
python main.py       # Start server
```

---

## Quick Reference: URLs

| URL | Purpose |
| --- | --- |
| `http://localhost:3000` | Frontend Dashboard |
| `http://localhost:8000` | Backend API |
| `http://localhost:8000/docs` | Swagger API Documentation |
| `http://localhost:8000/redoc` | ReDoc API Documentation |

---

## Quick Reference: File Locations

| Location | Purpose |
| --- | --- |
| `blockstate/client/src/pages/` | React pages |
| `blockstate/client/src/components/` | React components |
| `blockstate/client/src/contexts/` | Global state |
| `blockstate-backend/routes/` | API endpoints |
| `blockstate-backend/services/` | Business logic |

---

## Getting Help

### If Something Goes Wrong:

1. **Check the error message** - Read it carefully, it usually tells you what's wrong

1. **Check the terminal** - Look for error logs

1. **Check browser console** - Press F12, go to Console tab

1. **Google the error** - Copy the error message and search

1. **Restart everything** - Close terminals, restart VS Code, try again

1. **Check this guide** - Look in the Troubleshooting section

### If You're Still Stuck:

- Take a screenshot of the error

- Share the error message

- Share the terminal output

- Share what you were trying to do

- Ask Claude Opus with the handover document

---

## Congratulations! 🎉

You now have BlockState running locally on your laptop!

**Next Steps**:

1. Explore the application

1. Make some changes

1. Test the API

1. Read the handover document

1. Start building new features!

**Happy coding!**

---

**Document Version**: 1.0**Last Updated**: June 2026**Status**: Ready for local setup

