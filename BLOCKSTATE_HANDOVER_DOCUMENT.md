# BlockState: Complete Project Handover Document
## Comprehensive Guide for Claude Opus

**Project Owner**: [Your Name]  
**Project Status**: Phase 5 Complete - Frontend Integration Done  
**Date Created**: June 2026  
**Next Owner**: Claude Opus (via screenshots and code snippets)

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Business Context & Vision](#business-context--vision)
3. [Technical Architecture](#technical-architecture)
4. [What Has Been Built](#what-has-been-built)
5. [Technology Stack](#technology-stack)
6. [Project Structure](#project-structure)
7. [Key Components & Features](#key-components--features)
8. [API Integration](#api-integration)
9. [Database & Data Models](#database--data-models)
10. [Deployment Strategy](#deployment-strategy)
11. [Known Issues & Workarounds](#known-issues--workarounds)
12. [Future Roadmap](#future-roadmap)
13. [How to Continue Development](#how-to-continue-development)

---

## 1. Project Overview

### What is BlockState?

**BlockState** is a **desktop productivity application** that creates a "hard" focus environment by enforcing system-level process control and network blocking. It's designed for students, professionals, and anyone who struggles with digital distractions during deep work sessions.

### Core Problem It Solves

Users want to focus but:
- Social media apps (Discord, Twitter, YouTube) are always one click away
- Willpower-based solutions don't work long-term
- Existing tools are either too weak (browser extensions) or too invasive (parental controls)

**BlockState's Solution**: System-level enforcement that actually terminates distracting processes and blocks domains at the OS level.

### Target Users

1. **Students** - Exam prep, thesis writing, coding assignments
2. **Developers** - Deep coding sessions, debugging marathons
3. **Writers** - Novel writing, content creation, research
4. **Professionals** - Report writing, project management, strategic planning

### Business Model

**Freemium with Premium Features**:
- **Free Tier**: Basic workflows, 5 focus sessions/day limit
- **Premium** ($4.99/month): Unlimited sessions, AI categorization, advanced analytics, team collaboration
- **Enterprise** (custom): Multi-device sync, admin controls, team management

---

## 2. Business Context & Vision

### Entrepreneurship Project Framework

This project is built as part of an **entrepreneurship course** with the following components:

#### A. Business Plan
- Market size: 50M+ students + 100M+ knowledge workers globally
- Addressable market: $2B+ annually
- Competitive advantage: System-level enforcement (hard to replicate)

#### B. Business Model Canvas
- **Value Proposition**: Guaranteed focus through system-level enforcement
- **Customer Segments**: Students, developers, remote workers
- **Revenue Streams**: Subscription (Premium), one-time purchase (Desktop app)
- **Key Resources**: Software infrastructure, AI algorithms, community
- **Key Activities**: Development, marketing, community building
- **Key Partnerships**: Educational institutions, productivity tools, payment processors

#### C. Feasibility Study
- **Technical Feasibility**: ✅ High (all technologies proven)
- **Market Feasibility**: ✅ High (strong demand for focus tools)
- **Financial Feasibility**: ✅ High (low infrastructure costs, high margins)

### Strategic Goals

1. **MVP Launch** (Q3 2026): Desktop app with basic workflows
2. **Community Building** (Q4 2026): 10K+ active users
3. **Premium Launch** (Q1 2027): Subscription model with AI features
4. **Enterprise Sales** (Q2 2027): B2B partnerships with universities

---

## 3. Technical Architecture

### High-Level System Design

```
┌─────────────────────────────────────────────────────────────┐
│                    BlockState Ecosystem                      │
└─────────────────────────────────────────────────────────────┘

┌──────────────────┐         ┌──────────────────┐
│  React Frontend  │◄────────►│ FastAPI Backend  │
│  (Dashboard UI)  │  HTTP    │  (System Logic)  │
└──────────────────┘         └──────────────────┘
        ▲                            ▲
        │                            │
    Tauri Wrapper              Python Services
    (Desktop App)              ├─ Hosts Manager
                               ├─ Process Enforcer
                               ├─ Session Manager
                               └─ AI Categorizer

┌──────────────────────────────────────────────────┐
│  Windows OS Level                                │
├──────────────────────────────────────────────────┤
│ • Hosts File Modification (Domain Blocking)     │
│ • Process Termination (App Blocking)            │
│ • System Tray Integration                       │
│ • Registry Access (Future: Firewall Rules)      │
└──────────────────────────────────────────────────┘
```

### Architecture Layers

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Presentation** | React 19 + Tailwind CSS | User interface, real-time updates |
| **Desktop Wrapper** | Tauri | Package React as Windows .exe |
| **Frontend State** | React Context + AppContext | Global state management |
| **API Layer** | HTTP REST API | Communication between frontend and backend |
| **Backend** | FastAPI (Python) | Business logic, system integration |
| **System Integration** | psutil, Windows API | Process monitoring, hosts file management |
| **Data Storage** | JSON (local) / SQLite (backend) | Session data, workflows, user preferences |
| **AI/ML** | Keyword analysis + rule-based | URL/app categorization |

---

## 4. What Has Been Built

### Phase 1: React Dashboard (Complete) ✅

**Components Created**:
- `Dashboard.tsx` - Main focus timer interface with circular progress
- `Workflows.tsx` - Workflow management (CRUD operations)
- `SessionHistory.tsx` - Productivity analytics with charts
- `Statistics.tsx` - Overview of focus metrics
- `Settings.tsx` - Configuration and preferences
- `Sidebar.tsx` - Navigation component

**Features**:
- ✅ Circular progress timer (MM:SS format)
- ✅ Focus/Break timer with automatic transitions
- ✅ Enforcer status banner with process count
- ✅ Session summary showing real-time metrics
- ✅ Workflow selection and editing
- ✅ Session history with charts (recharts)
- ✅ Streak tracking and achievements
- ✅ Settings for notifications and boot behavior

**Design Philosophy**: Minimalist Academic Precision (inspired by Notion/Linear)
- Royal blue accent color (#2563EB)
- Soft off-white background (#F9FAFB)
- Monospaced timer for precision
- Smooth animations and transitions

### Phase 2: Python FastAPI Backend (Complete) ✅

**Services Created**:

#### A. Hosts Manager (`services/hosts_manager.py`)
- Modifies Windows hosts file to block domains
- Safely manages BlockState entries with markers
- Graceful error handling for permission issues
- Supports cross-platform paths

**Key Methods**:
```python
add_blocked_domains(domains: List[str])  # Add domains to hosts file
remove_blocked_domains(domains: List[str])  # Remove domains
clear_all_blocked()  # Clear all BlockState entries
get_blocked_domains() -> List[str]  # Get current blocked domains
```

#### B. Process Enforcer (`services/process_enforcer.py`)
- Monitors all running processes using psutil
- Identifies and terminates blocked applications
- Tracks enforcement statistics
- Handles graceful timeout + force kill

**Key Methods**:
```python
start_monitoring(blocked_processes: List[str])  # Start monitoring
stop_monitoring()  # Stop monitoring
get_running_processes() -> List[dict]  # Get all running processes
terminate_process(process_name: str)  # Terminate specific process
get_enforcement_stats() -> dict  # Get statistics
```

#### C. Session Manager (`services/session_manager.py`)
- Creates and tracks focus sessions
- Stores session data in JSON (upgradeable to database)
- Logs distractions blocked, processes terminated
- Generates session statistics and analytics

**Key Methods**:
```python
create_session(workflow_id: str, duration_minutes: int) -> Session
end_session(session_id: str, reason: str) -> Session
get_sessions(limit: int = 50) -> List[Session]
get_session_stats() -> dict
get_session_metrics(days: int = 7) -> dict
```

#### D. AI Categorizer (`services/ai_categorizer.py`)
- Categorizes URLs as "Productive" or "Distracting"
- Categorizes apps as "Productive" or "Distracting"
- Pre-loaded database of 43 URLs + 37 apps
- Keyword analysis fallback for unknown items
- Continuous learning via user feedback

**Key Methods**:
```python
categorize_url(url: str) -> dict  # Returns category + confidence
categorize_app(app_name: str) -> dict  # Returns category + confidence
categorize_urls_batch(urls: List[str]) -> List[dict]  # Batch processing
categorize_apps_batch(apps: List[str]) -> List[dict]  # Batch processing
submit_feedback(item: str, category: str, item_type: str)  # Learning
```

**API Endpoints** (30+ endpoints):

| Category | Endpoints | Count |
|----------|-----------|-------|
| Enforcer | `/api/enforcer/start`, `/api/enforcer/stop`, `/api/enforcer/status`, etc. | 9 |
| Workflows | `/api/workflows/`, `/api/workflows/{id}`, etc. | 7 |
| Sessions | `/api/sessions/`, `/api/sessions/{id}`, `/api/sessions/stats`, etc. | 8 |
| System | `/api/system/stats`, `/api/system/processes`, etc. | 8 |
| Categorization | `/api/categorization/url`, `/api/categorization/app`, etc. | 9 |

### Phase 3: AI Categorization Engine (Complete) ✅

**Capabilities**:
- ✅ Exact match database (fastest, most accurate)
- ✅ Keyword analysis engine (fallback for unknown items)
- ✅ Batch processing (categorize multiple items at once)
- ✅ Continuous learning (user feedback improves accuracy)
- ✅ Confidence scoring (0-1 scale)
- ✅ Reasoning provided (explains categorization)

**Pre-loaded Database**:
- **Productive URLs** (22): github.com, stackoverflow.com, docs.python.org, etc.
- **Distracting URLs** (21): twitter.com, youtube.com, reddit.com, etc.
- **Productive Apps** (19): VS Code, GitHub Desktop, Notion, etc.
- **Distracting Apps** (18): Discord, Steam, Spotify, etc.

### Phase 4: Tauri Desktop Wrapper (Complete) ✅

**Configuration Files Created**:
- `tauri.conf.json` - Full Tauri configuration
- `Cargo.toml` - Rust dependencies
- `package.json` - Node.js dependencies
- `src-tauri/src/main.rs` - Application entry point
- `src-tauri/src/python_manager.rs` - Python subprocess management
- `src-tauri/src/system_tray.rs` - System tray integration
- `src-tauri/src/commands.rs` - Tauri commands for frontend

**Features**:
- ✅ System tray integration (minimize to tray)
- ✅ Python backend auto-start
- ✅ Frontend-backend communication via Tauri commands
- ✅ Window management (minimize/maximize/close)
- ✅ Auto-update support
- ✅ Code signing ready
- ✅ Multiple installer formats

### Phase 5: Frontend Integration (Complete) ✅

**API Service Layer** (`client/src/lib/api.ts`):
- Centralized API communication
- Error handling and response formatting
- Support for both HTTP (web) and Tauri (desktop) modes
- 30+ API methods for all backend operations

**AppContext Integration** (`client/src/contexts/AppContext.tsx`):
- Global state management for timer, enforcer, workflows
- Async operations for backend API calls
- Session tracking and metrics
- Settings persistence

**Component Integration**:
- Dashboard connected to enforcer API
- Workflows page with CRUD operations
- Session History with real-time data
- All pages with loading states and error handling

---

## 5. Technology Stack

### Frontend

| Technology | Version | Purpose |
|-----------|---------|---------|
| React | 19.2.1 | UI framework |
| TypeScript | 5.6.3 | Type safety |
| Tailwind CSS | 4.1.14 | Styling |
| shadcn/ui | Latest | Component library |
| Wouter | 3.3.5 | Client-side routing |
| Recharts | 2.15.2 | Charts and analytics |
| Framer Motion | 12.23.22 | Animations |
| Sonner | 2.0.7 | Toast notifications |
| Lucide React | 0.453.0 | Icons |

### Backend

| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.11+ | Backend language |
| FastAPI | Latest | Web framework |
| psutil | Latest | Process monitoring |
| Pydantic | Latest | Data validation |
| SQLite | Latest | Database (optional) |
| Uvicorn | Latest | ASGI server |

### Desktop

| Technology | Version | Purpose |
|-----------|---------|---------|
| Tauri | 1.5+ | Desktop wrapper |
| Rust | Latest | Tauri backend |
| Node.js | 22.13.0 | Build tools |

### Build & Deployment

| Tool | Purpose |
|------|---------|
| Vite | Frontend build tool |
| pnpm | Package manager |
| Cargo | Rust package manager |
| GitHub Actions | CI/CD (future) |

---

## 6. Project Structure

### Frontend Project (`/home/ubuntu/blockstate/`)

```
blockstate/
├── client/
│   ├── public/
│   │   ├── favicon.ico
│   │   └── __manus__/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Sidebar.tsx              # Navigation component
│   │   │   ├── CircularTimer.tsx        # Animated progress timer
│   │   │   ├── EnforcerStatusBanner.tsx # Status display
│   │   │   ├── SessionSummary.tsx       # Real-time metrics
│   │   │   ├── BreakTimer.tsx           # Break timer component
│   │   │   ├── ErrorBoundary.tsx        # Error handling
│   │   │   ├── ManusDialog.tsx          # Dialog component
│   │   │   ├── Map.tsx                  # Google Maps integration
│   │   │   └── ui/                      # shadcn/ui components
│   │   ├── contexts/
│   │   │   └── AppContext.tsx           # Global state management
│   │   ├── hooks/
│   │   │   ├── useComposition.ts
│   │   │   ├── useMobile.tsx
│   │   │   ├── usePersistFn.ts
│   │   │   └── useTauri.ts              # Tauri integration hook
│   │   ├── lib/
│   │   │   ├── api.ts                   # API service layer
│   │   │   └── utils.ts
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx            # Main focus timer page
│   │   │   ├── Workflows.tsx            # Workflow management
│   │   │   ├── Statistics.tsx           # Overview stats
│   │   │   ├── SessionHistory.tsx       # Analytics & history
│   │   │   ├── Settings.tsx             # Configuration
│   │   │   ├── Home.tsx                 # Legacy (deprecated)
│   │   │   └── NotFound.tsx             # 404 page
│   │   ├── App.tsx                      # Main app component with routing
│   │   ├── main.tsx                     # React entry point
│   │   └── index.css                    # Global styles & Tailwind
│   ├── index.html                       # HTML template
│   └── tsconfig.json
├── server/
│   └── index.ts                         # Express server (placeholder)
├── shared/
│   └── const.ts                         # Shared constants
├── package.json
├── vite.config.ts
├── tsconfig.json
└── README.md
```

### Backend Project (`/home/ubuntu/blockstate-backend/`)

```
blockstate-backend/
├── main.py                              # FastAPI app entry point
├── models.py                            # Pydantic data models
├── requirements.txt                     # Python dependencies
├── .env                                 # Environment variables
├── .env.example                         # Example env file
├── services/
│   ├── __init__.py
│   ├── hosts_manager.py                 # Domain blocking service
│   ├── process_enforcer.py              # Process monitoring service
│   ├── session_manager.py               # Session tracking service
│   └── ai_categorizer.py                # AI categorization service
├── routes/
│   ├── __init__.py
│   ├── enforcer.py                      # Enforcer API routes
│   ├── sessions.py                      # Session API routes
│   ├── workflows.py                     # Workflow API routes
│   ├── system.py                        # System monitoring routes
│   └── categorization.py                # Categorization API routes
├── data/
│   ├── sessions.json                    # Session storage
│   ├── workflows.json                   # Workflow storage
│   └── categorization_feedback.json     # Learning data
└── README.md
```

### Desktop Wrapper (`/home/ubuntu/blockstate-desktop/`)

```
blockstate-desktop/
├── src-tauri/
│   ├── src/
│   │   ├── main.rs                      # Tauri app entry point
│   │   ├── python_manager.rs            # Python subprocess manager
│   │   ├── system_tray.rs               # System tray handler
│   │   ├── commands.rs                  # Tauri commands
│   │   └── build.rs                     # Build script
│   ├── Cargo.toml                       # Rust dependencies
│   └── icons/                           # App icons
├── tauri.conf.json                      # Tauri configuration
├── package.json                         # Node.js dependencies
├── TAURI_SETUP_GUIDE.md                 # Setup instructions
└── README.md
```

---

## 7. Key Components & Features

### 7.1 Dashboard Page

**Purpose**: Main interface for starting/stopping focus sessions

**Components**:
- `CircularTimer` - Animated progress ring showing time remaining
- `EnforcerStatusBanner` - Shows enforcer status (ACTIVE/STANDBY) with process count
- `SessionSummary` - Real-time metrics (time elapsed, distractions blocked, workflow)
- `BreakTimer` - Post-focus break management
- Control buttons (Start Focus, Stop Focus, Reset)

**State Management**:
- Timer countdown (25 minutes default)
- Enforcer activation/deactivation
- Break timer trigger
- Session metrics tracking

**API Calls**:
```typescript
// Start focus session
await apiService.startEnforcer(workflowId, durationMinutes, strictMode);

// Stop focus session
await apiService.stopEnforcer(sessionId, reason);

// Get enforcer status
await apiService.getEnforcerStatus();
```

### 7.2 Workflows Page

**Purpose**: Create and manage focus workflows

**Features**:
- Create new workflows with custom names
- Edit allowed apps, allowed sites, blocked processes
- Delete workflows
- Quick workflow switching from dashboard

**Data Model**:
```typescript
interface Workflow {
  id: string;                    // Unique identifier
  name: string;                  // Display name
  allowedApps: string[];         // Apps that can run
  allowedSites: string[];        // Websites that can load
  blockedProcesses: string[];    // Processes to terminate
}
```

**API Calls**:
```typescript
// Get all workflows
await apiService.getWorkflows();

// Create workflow
await apiService.createWorkflow({ name, blocked_processes, blocked_domains });

// Update workflow
await apiService.updateWorkflow(workflowId, updatedWorkflow);

// Delete workflow
await apiService.deleteWorkflow(workflowId);
```

### 7.3 Session History Page

**Purpose**: Track productivity over time with analytics

**Features**:
- Total sessions counter
- Total focus time tracker
- Current streak counter
- Distractions blocked counter
- Focus time trend chart (last 7 days)
- Distractions blocked chart
- Workflow distribution pie chart
- Recent sessions table

**Charts Used**:
- LineChart (focus time trend)
- BarChart (distractions blocked)
- PieChart (workflow distribution)

**API Calls**:
```typescript
// Get all sessions
await apiService.getSessions(limit);

// Get session metrics
await apiService.getSessionMetrics(days);
```

### 7.4 Settings Page

**Purpose**: Configure application behavior

**Settings Available**:
- **Focus Duration Presets**: 25 min (Pomodoro), 45 min (Deep Work), 90 min (Flow State)
- **Notifications**: Enable/disable notifications, sound alerts
- **Boot Behavior**: Start app at system startup
- **Strict Mode**: Aggressive blocking (harder to disable)
- **Backend Status**: Shows if Python backend is connected

### 7.5 Sidebar Navigation

**Purpose**: Global navigation between pages

**Navigation Items**:
- Dashboard (main timer interface)
- Workflows (workflow management)
- Statistics (overview metrics)
- Session History (analytics)
- Settings (configuration)

**Active State Indicator**: Current page highlighted in blue

---

## 8. API Integration

### API Base URL

**Development**: `http://localhost:8000/api`  
**Production**: `https://api.blockstate.app/api` (future)

### Authentication

Currently **no authentication** (local development). For production:
- JWT tokens for user sessions
- OAuth2 for third-party integrations
- API keys for programmatic access

### Request/Response Format

**Request**:
```json
{
  "method": "POST",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": {
    "workflow_id": "deep-coding",
    "duration_minutes": 25,
    "strict_mode": false
  }
}
```

**Response**:
```json
{
  "success": true,
  "message": "Focus session started",
  "data": {
    "session_id": "sess_12345",
    "workflow_id": "deep-coding",
    "start_time": "2026-06-06T12:00:00Z",
    "duration_minutes": 25
  }
}
```

### Error Handling

**Error Response**:
```json
{
  "success": false,
  "message": "Failed to start enforcer",
  "error": "Permission denied: Cannot modify hosts file"
}
```

**Common Errors**:
- `403 Forbidden` - Permission denied (hosts file, process termination)
- `404 Not Found` - Workflow/session not found
- `500 Internal Server Error` - Backend service failure
- `503 Service Unavailable` - Backend service not running

### API Methods Reference

#### Enforcer Endpoints

```python
POST /api/enforcer/start
Body: {
  "workflow_id": "deep-coding",
  "duration_minutes": 25,
  "strict_mode": false
}
Response: { "session_id": "...", "status": "active" }

POST /api/enforcer/stop
Body: {
  "session_id": "sess_12345",
  "reason": "User stopped session"
}
Response: { "status": "stopped", "duration": 1500 }

GET /api/enforcer/status
Response: {
  "is_active": true,
  "processes_blocked": 3,
  "domains_blocked": 5,
  "current_session": { ... }
}
```

#### Workflow Endpoints

```python
GET /api/workflows/
Response: [ { "id": "...", "name": "...", ... } ]

POST /api/workflows/
Body: { "name": "Deep Coding", "blocked_processes": [...] }
Response: { "id": "...", "name": "..." }

PUT /api/workflows/{workflow_id}
Body: { "name": "...", "blocked_processes": [...] }
Response: { "id": "...", "name": "..." }

DELETE /api/workflows/{workflow_id}
Response: { "success": true }
```

#### Session Endpoints

```python
GET /api/sessions/?limit=50
Response: [ { "id": "...", "duration": 1500, ... } ]

GET /api/sessions/{session_id}
Response: { "id": "...", "duration": 1500, ... }

GET /api/sessions/stats
Response: {
  "total_sessions": 42,
  "total_focus_time": 63000,
  "current_streak": 7
}

GET /api/sessions/metrics?days=7
Response: {
  "daily_data": [ { "date": "...", "sessions": 3, ... } ]
}
```

#### Categorization Endpoints

```python
POST /api/categorization/url?url=github.com
Response: {
  "category": "productive",
  "confidence": 0.95,
  "reasoning": "GitHub is a code repository platform"
}

POST /api/categorization/app?app_name=Discord.exe
Response: {
  "category": "distracting",
  "confidence": 0.98,
  "reasoning": "Discord is a communication/social platform"
}

POST /api/categorization/feedback
Body: {
  "item": "github.com",
  "category": "productive",
  "item_type": "url"
}
Response: { "success": true, "learning_updated": true }
```

---

## 9. Database & Data Models

### Current Data Storage

**Frontend**: React Context (in-memory) + localStorage (optional)  
**Backend**: JSON files (development) + SQLite (production-ready)

### Data Models

#### Session Model

```python
class Session(BaseModel):
    id: str                          # Unique session ID
    workflow_id: str                 # Workflow used
    start_time: datetime             # Session start
    end_time: Optional[datetime]     # Session end
    duration: int                    # Duration in seconds
    distractions_blocked: int        # Count of blocked items
    processes_terminated: List[str]  # Terminated processes
    domains_blocked: List[str]       # Blocked domains
    completed: bool                  # Was session completed?
    reason_stopped: Optional[str]    # Why was it stopped?
```

#### Workflow Model

```python
class Workflow(BaseModel):
    id: str                          # Unique workflow ID
    name: str                        # Display name
    description: Optional[str]       # Description
    blocked_processes: List[str]     # Processes to block
    blocked_domains: List[str]       # Domains to block
    allowed_processes: List[str]     # Whitelist (optional)
    created_at: datetime             # Creation timestamp
    updated_at: datetime             # Last update
```

#### Categorization Model

```python
class CategorizationResult(BaseModel):
    item: str                        # URL or app name
    item_type: str                   # "url" or "app"
    category: str                    # "productive" or "distracting"
    confidence: float                # 0-1 confidence score
    reasoning: str                   # Explanation
    is_custom: bool                  # User-defined category?
```

### Data Storage Locations

**Frontend**:
- `localStorage` - User preferences, workflows (if implemented)
- `sessionStorage` - Temporary session data

**Backend**:
- `/data/sessions.json` - Session history
- `/data/workflows.json` - Workflow definitions
- `/data/categorization_feedback.json` - User feedback for learning

### Database Schema (Future - SQLite)

```sql
-- Sessions table
CREATE TABLE sessions (
  id TEXT PRIMARY KEY,
  workflow_id TEXT NOT NULL,
  start_time TIMESTAMP NOT NULL,
  end_time TIMESTAMP,
  duration INTEGER NOT NULL,
  distractions_blocked INTEGER DEFAULT 0,
  completed BOOLEAN DEFAULT FALSE,
  reason_stopped TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Workflows table
CREATE TABLE workflows (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  blocked_processes TEXT,  -- JSON array
  blocked_domains TEXT,    -- JSON array
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categorization feedback table
CREATE TABLE categorization_feedback (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  item TEXT NOT NULL,
  item_type TEXT NOT NULL,  -- "url" or "app"
  category TEXT NOT NULL,   -- "productive" or "distracting"
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 10. Deployment Strategy

### Development Environment

**Local Setup**:
```bash
# Frontend
cd blockstate
pnpm install
pnpm dev  # Runs on http://localhost:3000

# Backend
cd blockstate-backend
pip install -r requirements.txt
python main.py  # Runs on http://localhost:8000

# Desktop (Tauri)
cd blockstate-desktop
npm install
npm run tauri dev
```

### Production Deployment

#### Frontend (Web)
- **Hosting**: Vercel, Netlify, or custom server
- **Build**: `pnpm build` → outputs to `dist/`
- **Domain**: blockstate.app (future)

#### Backend (API)
- **Hosting**: Railway, Render, AWS EC2, or custom server
- **Database**: PostgreSQL (production) or SQLite (small scale)
- **API Domain**: api.blockstate.app (future)

#### Desktop (Tauri)
- **Build**: `npm run tauri build` → outputs `.exe` installer
- **Distribution**: GitHub Releases, website download, Microsoft Store (future)
- **Auto-updates**: Tauri built-in updater

### Environment Variables

**Backend** (`.env`):
```
PYTHON_ENV=development
DATABASE_URL=sqlite:///blockstate.db
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000,https://blockstate.app
```

**Frontend** (`.env.local`):
```
VITE_API_URL=http://localhost:8000/api
VITE_APP_TITLE=BlockState
VITE_APP_LOGO=https://blockstate.app/logo.png
```

---

## 11. Known Issues & Workarounds

### Issue 1: Nested Anchor Tags Error ✅ FIXED

**Problem**: React error "cannot contain a nested <a>"  
**Root Cause**: Wouter's `<Link>` component wrapped with `<a>` tag  
**Solution**: Pass className directly to Link component, remove inner `<a>`

```typescript
// ❌ WRONG
<Link href="/path">
  <a className="...">Content</a>
</Link>

// ✅ CORRECT
<Link href="/path" className="...">
  Content
</Link>
```

### Issue 2: API Service Not Found

**Problem**: `Cannot find module '@/lib/api'`  
**Root Cause**: File not saved in previous session  
**Solution**: Recreated `client/src/lib/api.ts` with complete API service layer

### Issue 3: TypeScript Missing Properties

**Problem**: `Property 'sessions' does not exist on type 'AppContextType'`  
**Root Cause**: AppContext interface and value object out of sync  
**Solution**: Added `sessions` and `loadSessions` to both interface and value object

### Issue 4: Windows Hosts File Permissions

**Problem**: "Permission denied" when modifying hosts file  
**Workaround**: Run app as administrator (Tauri handles this automatically)  
**Future Solution**: Use Windows API directly instead of file modification

### Issue 5: Process Termination Limitations

**Problem**: Some processes (system services) cannot be terminated  
**Workaround**: Maintain whitelist of terminable processes  
**Future Solution**: Use Windows Job Objects for more granular control

---

## 12. Future Roadmap

### Phase 6: Local Storage & Persistence (Next)
- [ ] Save workflows to localStorage
- [ ] Persist user settings
- [ ] Offline mode support
- [ ] Sync with backend when online

### Phase 7: Real-Time WebSocket Updates
- [ ] WebSocket connection for live status
- [ ] Real-time distraction notifications
- [ ] Live process monitoring
- [ ] Reduced polling overhead

### Phase 8: Advanced Features
- [ ] Focus zones (soft/medium/hard blocking)
- [ ] Distraction blocking visualization
- [ ] Focus buddy mode (social competition)
- [ ] Leaderboards and achievements
- [ ] Browser extension integration

### Phase 9: Mobile App
- [ ] React Native mobile app
- [ ] Cross-device sync
- [ ] Mobile notifications
- [ ] Remote session control

### Phase 10: Enterprise Features
- [ ] Team management
- [ ] Admin dashboard
- [ ] Usage analytics
- [ ] Compliance reporting
- [ ] SSO integration

### Phase 11: AI Enhancements
- [ ] Machine learning model for categorization
- [ ] Personalized focus recommendations
- [ ] Predictive distraction detection
- [ ] Natural language workflow creation

### Phase 12: Monetization
- [ ] Premium subscription tier
- [ ] Team plans
- [ ] Enterprise licensing
- [ ] Payment processing (Stripe)

---

## 13. How to Continue Development

### For Claude Opus: Initial Context

When the user sends you a screenshot or code snippet, here's what you should know:

#### 1. **Always Ask for Context**
- What page/component is this?
- What's the error or desired behavior?
- What have they tried already?

#### 2. **Reference This Document**
- Architecture is in Section 3
- Component structure is in Section 7
- API endpoints are in Section 8
- Data models are in Section 9

#### 3. **Common Tasks & Solutions**

**Adding a New Page**:
1. Create `client/src/pages/NewPage.tsx`
2. Add route in `client/src/App.tsx`
3. Add navigation item in `client/src/components/Sidebar.tsx`
4. Use `useApp()` hook for global state
5. Use `apiService` for backend calls

**Adding a New API Endpoint**:
1. Create route file in `blockstate-backend/routes/`
2. Add methods in appropriate service
3. Register route in `main.py`
4. Add method to `client/src/lib/api.ts`
5. Use in components via `apiService.methodName()`

**Fixing TypeScript Errors**:
1. Check if interface is updated
2. Check if value object includes all properties
3. Check if imports are correct
4. Run `pnpm check` to see all errors

**Debugging Backend Issues**:
1. Check if FastAPI server is running on port 8000
2. Check logs in terminal
3. Test endpoints with curl or Postman
4. Check `.env` file for configuration

#### 4. **Key Files to Know**

| File | Purpose | When to Edit |
|------|---------|-------------|
| `client/src/App.tsx` | Routing & layout | Adding pages |
| `client/src/contexts/AppContext.tsx` | Global state | Adding state properties |
| `client/src/lib/api.ts` | API communication | Adding API methods |
| `blockstate-backend/main.py` | Backend entry | Registering routes |
| `blockstate-backend/services/` | Business logic | Core functionality |

#### 5. **Testing Checklist**

Before considering a feature complete:
- [ ] No TypeScript errors (`pnpm check`)
- [ ] No React console errors
- [ ] Component renders without errors
- [ ] API calls work (check network tab)
- [ ] Loading states display correctly
- [ ] Error states display correctly
- [ ] Mobile responsive (if applicable)

#### 6. **Performance Considerations**

- Use `useMemo` for expensive calculations
- Use `useCallback` for event handlers
- Avoid unnecessary re-renders
- Batch API calls when possible
- Use pagination for large lists

#### 7. **Security Considerations**

- Never store sensitive data in localStorage
- Validate all user inputs
- Use HTTPS in production
- Implement CORS properly
- Rate limit API endpoints
- Sanitize user-generated content

---

## 14. Quick Reference

### Common Commands

```bash
# Frontend
pnpm dev              # Start dev server
pnpm build            # Build for production
pnpm check            # TypeScript check
pnpm format           # Format code

# Backend
python main.py        # Start FastAPI server
pip install -r requirements.txt  # Install dependencies

# Desktop
npm run tauri dev     # Dev mode
npm run tauri build   # Build .exe
```

### Important URLs

- Frontend (dev): `http://localhost:3000`
- Backend (dev): `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Swagger UI: `http://localhost:8000/redoc`

### Important Directories

- Frontend code: `/home/ubuntu/blockstate/client/src/`
- Backend code: `/home/ubuntu/blockstate-backend/`
- Desktop code: `/home/ubuntu/blockstate-desktop/src-tauri/`

### Key Dependencies

**Frontend**:
- React 19 - UI framework
- Tailwind CSS 4 - Styling
- Recharts - Charts
- Wouter - Routing

**Backend**:
- FastAPI - Web framework
- psutil - Process monitoring
- Pydantic - Data validation

---

## 15. Contact & Support

**Project Owner**: [Your Name]  
**Email**: [Your Email]  
**GitHub**: [Your GitHub]  
**Discord**: [Your Discord] (for team communication)

### For Claude Opus

When helping with this project:
1. **Always refer back to this document** for context
2. **Ask clarifying questions** before making changes
3. **Test thoroughly** before delivering
4. **Document changes** in code comments
5. **Keep this document updated** with new information

---

## Appendix A: Glossary

| Term | Definition |
|------|-----------|
| **Enforcer** | The system-level process that blocks apps and domains |
| **Workflow** | A configuration of allowed/blocked apps and sites |
| **Session** | A single focus period with a start time and duration |
| **Distraction** | A blocked app or domain attempt |
| **Tauri** | Framework for packaging web apps as desktop apps |
| **FastAPI** | Python web framework for building APIs |
| **Context** | React feature for global state management |
| **Hosts File** | Windows system file that maps domains to IP addresses |
| **psutil** | Python library for monitoring system processes |

---

## Appendix B: Useful Resources

### Documentation
- [React Documentation](https://react.dev)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Tauri Documentation](https://tauri.app)
- [Tailwind CSS Documentation](https://tailwindcss.com)

### Tools
- [Postman](https://www.postman.com) - API testing
- [VS Code](https://code.visualstudio.com) - Code editor
- [GitHub](https://github.com) - Version control
- [Figma](https://figma.com) - Design tool

### Learning Resources
- [React Hooks Guide](https://react.dev/reference/react)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Tauri Getting Started](https://tauri.app/v1/guides/getting-started/setup/)

---

**Document Version**: 1.0  
**Last Updated**: June 2026  
**Status**: Ready for handover to Claude Opus  
**Next Review**: After Phase 6 completion

