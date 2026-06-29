# BlockState Backend

Production-ready Python FastAPI backend for the BlockState focus enforcement system.

## Features

- **System Enforcer**: Terminate blocked applications and monitor processes
- **Hosts File Manager**: Block distracting domains at the system level
- **Session Tracking**: Track focus sessions with detailed metrics
- **Workflow Management**: Create and manage focus workflows
- **Real-time Monitoring**: Monitor system resources and active processes
- **RESTful API**: Complete API for frontend integration

## Architecture

```
blockstate-backend/
├── main.py                 # FastAPI application entry point
├── models.py              # Pydantic data models
├── requirements.txt       # Python dependencies
├── services/
│   ├── hosts_manager.py   # Hosts file management
│   ├── process_enforcer.py # Process monitoring and termination
│   └── session_manager.py  # Session tracking and storage
├── routes/
│   ├── enforcer.py        # Enforcer API endpoints
│   ├── workflows.py       # Workflow management endpoints
│   ├── sessions.py        # Session tracking endpoints
│   └── system.py          # System monitoring endpoints
└── data/                  # Data storage directory
    ├── sessions.json      # Session records
    └── workflows.json     # Workflow definitions
```

## Installation

### Prerequisites
- Python 3.8+
- pip or conda
- Administrator privileges (for hosts file and process management)

### Setup

1. **Clone the repository**
```bash
cd /home/ubuntu/blockstate-backend
```

2. **Create virtual environment** (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create data directory**
```bash
mkdir -p data
```

## Running the Backend

### Development Mode
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

Once the server is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## API Endpoints

### Enforcer Endpoints
- `POST /api/enforcer/start` - Start the enforcer for a focus session
- `POST /api/enforcer/stop` - Stop the enforcer
- `GET /api/enforcer/status` - Get current enforcer status
- `POST /api/enforcer/enforce` - Manually trigger enforcement
- `GET /api/enforcer/processes/blocked` - Get blocked processes
- `GET /api/enforcer/domains/blocked` - Get blocked domains
- `POST /api/enforcer/domains/block` - Block domains
- `POST /api/enforcer/domains/unblock` - Unblock domains

### Workflow Endpoints
- `POST /api/workflows/` - Create a new workflow
- `GET /api/workflows/` - Get all workflows
- `GET /api/workflows/{workflow_id}` - Get a specific workflow
- `PUT /api/workflows/{workflow_id}` - Update a workflow
- `DELETE /api/workflows/{workflow_id}` - Delete a workflow
- `POST /api/workflows/{workflow_id}/apply` - Apply a workflow
- `GET /api/workflows/{workflow_id}/stats` - Get workflow statistics

### Session Endpoints
- `GET /api/sessions/` - Get all sessions
- `GET /api/sessions/{session_id}` - Get a specific session
- `GET /api/sessions/{session_id}/stats` - Get session statistics
- `GET /api/sessions/workflow/{workflow_id}` - Get sessions by workflow
- `GET /api/sessions/date/{date_str}` - Get sessions by date
- `POST /api/sessions/{session_id}/distraction` - Log a distraction
- `POST /api/sessions/{session_id}/process-terminated` - Log terminated process
- `POST /api/sessions/{session_id}/app-used` - Log app usage

### System Endpoints
- `GET /api/system/info` - Get system information
- `GET /api/system/stats` - Get system statistics
- `GET /api/system/processes` - Get running processes
- `GET /api/system/process/{pid}` - Get process information
- `POST /api/system/process/{pid}/kill` - Terminate a process
- `GET /api/system/cpu/usage` - Get CPU usage
- `GET /api/system/memory/usage` - Get memory usage
- `GET /api/system/disk/usage` - Get disk usage

## Example Usage

### Start a Focus Session
```bash
curl -X POST "http://localhost:8000/api/enforcer/start" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_id": "deep-coding",
    "duration_minutes": 25,
    "strict_mode": false
  }'
```

### Get Enforcer Status
```bash
curl "http://localhost:8000/api/enforcer/status"
```

### Create a Workflow
```bash
curl -X POST "http://localhost:8000/api/workflows/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Deep Coding",
    "description": "Focus workflow for programming",
    "allowed_apps": ["VS Code", "GitHub", "StackOverflow"],
    "blocked_processes": ["Discord.exe", "Steam.exe", "Spotify.exe"],
    "blocked_domains": ["twitter.com", "facebook.com", "youtube.com"]
  }'
```

## Key Features

### 1. Hosts File Management
- Blocks domains by modifying the system hosts file
- Redirects blocked domains to 127.0.0.1
- Safely manages BlockState entries
- Requires administrator privileges

### 2. Process Enforcement
- Monitors running processes
- Terminates blocked applications
- Graceful termination with timeout
- Force kill if process doesn't respond

### 3. Session Tracking
- Records all focus sessions
- Tracks distractions blocked
- Logs terminated processes
- Stores session metrics for analytics

### 4. Workflow Management
- Create custom focus workflows
- Define allowed and blocked applications
- Manage blocked domains
- Apply workflows to sessions

## Security Considerations

1. **Administrator Privileges**: Hosts file modification and process termination require admin rights
2. **CORS Configuration**: Currently allows all origins (update for production)
3. **Input Validation**: All inputs validated using Pydantic models
4. **Error Handling**: Comprehensive error handling and logging
5. **Data Storage**: Session data stored locally (consider database for production)

## Performance

- **Process Monitoring**: Efficient using psutil library
- **Concurrent Requests**: FastAPI handles multiple concurrent requests
- **Memory Usage**: Minimal memory footprint
- **Scalability**: Can handle thousands of concurrent sessions

## Troubleshooting

### Permission Denied Error
- Run the backend with administrator privileges
- On Linux/Mac: `sudo python main.py`
- On Windows: Run Command Prompt as Administrator

### Hosts File Not Modified
- Check if running with sufficient privileges
- Verify hosts file path is correct for your OS
- Check logs for specific error messages

### Process Not Terminating
- Some system processes cannot be terminated
- Try force kill option: `force=true` parameter
- Check if process has elevated privileges

## Development

### Adding New Routes
1. Create a new file in `routes/` directory
2. Define router and endpoints
3. Include router in `main.py`

### Adding New Services
1. Create service file in `services/` directory
2. Implement service class with methods
3. Import and use in routes

### Testing
```bash
# Run with test data
python main.py --test-mode

# Run specific route tests
pytest routes/enforcer.py
```

## License

BlockState Backend © 2026. All rights reserved.

## Support

For issues, questions, or contributions, please contact the BlockState development team.
