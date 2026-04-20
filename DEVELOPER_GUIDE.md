# FRIDAY Developer Guide — Extension & Customization

> This guide is for developers who want to extend FRIDAY with custom features or integrate it with other services.

## 🏗️ Architecture Overview

FRIDAY uses a modular architecture:

```
Input Layer          Processing Layer        Output Layer
────────────────────────────────────────────────────────
Microphone  ──┐
System Tray ──┼──→ Enhanced Brain ──→ Features System ──→ Voice Output
Web UI      ──┤    (Gemini AI)      (System Monitor,   ├──→ Text Output
Rest API    ──┤    + Features       Weather, Calendar) ├──→ Web UI
Global HotKey ┘                                        └──→ REST API
```

## 📦 Module Structure

### Core Modules

#### `assistant/enhanced_brain.py`
The AI brain with feature integration
- **Class**: `EnhancedFridayBrain`
- **Key Methods**:
  - `think(user_input)` - Main processing
  - `_process_feature_request()` - Feature routing
  - `add_calendar_event()` - Calendar API
  - `add_note()` - Notes API
  - `create_automation()` - Automation API

```python
from assistant.enhanced_brain import EnhancedFridayBrain

brain = EnhancedFridayBrain()
response = brain.think("What's the weather?")
brain.add_calendar_event("Meeting", "2026-04-21T14:00:00")
```

#### `assistant/features.py`
All feature implementations
- **Classes**:
  - `SystemMonitor` - System info
  - `WeatherFeature` - Weather API
  - `CalendarFeature` - Calendar management
  - `NotesFeature` - Note storage
  - `RemoteControl` - App control
  - `Automations` - Automation engine

```python
from assistant.features import weather, calendar, notes

# Get weather
weather_data = weather.get_weather("London")

# Add calendar event
event = calendar.add_event("Meeting", "", "2026-04-21T14:00:00")

# Add note
note = notes.add_note("My Note", "Content", ["tag1", "tag2"])
```

#### `background_service.py`
Background service with system tray and hotkeys
- **Class**: `FridayBackgroundService`
- **Key Methods**:
  - `run()` - Start with tray icon
  - `run_in_background()` - No UI mode
  - `setup_global_hotkey()` - Register hotkey
  - `on_voice_click()` - Handle voice button

#### `web/api.py`
REST API endpoints
- **Function**: `register_api_routes(app)`
- **Endpoints**: 30+ REST endpoints for all features

#### `web/app.py`
Flask web server
- **Functions**:
  - `socketio` - WebSocket connections
  - Route handlers for web UI
  - API route registration

---

## 🔧 Adding New Features

### Step 1: Create Feature Class

```python
# In assistant/features.py

class MyNewFeature:
    def __init__(self):
        self.data = {}
    
    def do_something(self, param):
        """Do something with the parameter."""
        result = f"Processing {param}"
        return result
    
    def get_status(self):
        """Return feature status."""
        return {"status": "active"}

# Export it
my_feature = MyNewFeature()
```

### Step 2: Integrate with Brain

```python
# In assistant/enhanced_brain.py

from assistant.features import my_feature

class EnhancedFridayBrain:
    def __init__(self):
        # ... existing code ...
        self.features["my_feature"] = my_feature
    
    def _process_feature_request(self, text: str) -> str:
        text_lower = text.lower()
        
        # Add detection for your feature
        if "my feature" in text_lower:
            param = self._extract_param(text)
            result = my_feature.do_something(param)
            return f"My feature result: {result}"
        
        # ... rest of method ...
```

### Step 3: Add REST API Endpoint

```python
# In web/api.py

def register_api_routes(app):
    # ... existing routes ...
    
    @app.route("/api/myfeature", methods=["GET"])
    def my_feature_get():
        status = my_feature.get_status()
        return jsonify(status)
    
    @app.route("/api/myfeature", methods=["POST"])
    def my_feature_post():
        data = request.get_json()
        result = my_feature.do_something(data.get("param"))
        return jsonify({"result": result}), 201
```

### Step 4: Add Web UI Component

```html
<!-- In web/templates/index.html, add tab -->

<div id="myfeature-tab" class="tab-content">
    <h2>My Feature</h2>
    <input id="param-input" type="text" placeholder="Enter parameter">
    <button onclick="callMyFeature()">Execute</button>
    <div id="result"></div>
</div>
```

```javascript
// In web/static/script.js

function callMyFeature() {
    const param = document.getElementById('param-input').value;
    fetch('/api/myfeature', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({param: param})
    })
    .then(r => r.json())
    .then(data => {
        document.getElementById('result').textContent = data.result;
    });
}
```

---

## 🔌 Creating Plugins

Plugins extend FRIDAY without modifying core code.

### Plugin Structure

```python
# plugins/my_plugin.py

class MyPlugin:
    def __init__(self, friday_core):
        self.core = friday_core
        self.name = "My Plugin"
        self.version = "1.0.0"
    
    def on_load(self):
        """Called when plugin loads."""
        print(f"Loaded {self.name}")
    
    def process_command(self, text):
        """Process custom commands."""
        if "plugin command" in text:
            return "Plugin response"
        return None
    
    def get_features(self):
        """Return plugin features."""
        return {
            "custom_feature": self.custom_feature
        }
    
    def custom_feature(self):
        return "Custom implementation"
```

### Load Plugin

```python
# In main.py

from plugins.my_plugin import MyPlugin

friday = FridayCore()
plugin = MyPlugin(friday)
plugin.on_load()

# Use plugin
response = plugin.process_command("plugin command")
```

---

## 🌐 REST API Extension

### Adding Authenticated Endpoints

```python
from functools import wraps

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token != "Bearer YOUR_TOKEN":
            return {"error": "Unauthorized"}, 401
        return f(*args, **kwargs)
    return decorated

@app.route("/api/protected", methods=["GET"])
@require_auth
def protected_endpoint():
    return {"data": "protected"}
```

### WebSocket Events

```python
from flask_socketio import emit, on, disconnect

@socketio.on('custom_event')
def handle_custom_event(data):
    """Handle custom WebSocket event."""
    result = brain.think(data['message'])
    emit('custom_response', {'result': result})
```

---

## 🧠 Customizing AI Behavior

### Custom System Instructions

```python
# In enhanced_brain.py

SYSTEM_TEMPLATE = """You are FRIDAY, a specialized assistant for [YOUR USE CASE].
Your expertise: [YOUR EXPERTISE]
When handling queries about [TOPIC], always [INSTRUCTION]
"""
```

### Adding Commands to Brain

```python
def _process_feature_request(self, text: str) -> str:
    text_lower = text.lower()
    
    # Add custom command
    if text_lower.startswith("custom:"):
        command = text_lower[7:].strip()
        # Process custom command
        return self._handle_custom(command)
    
    # Continue with existing features
    return None
```

---

## 🔐 Security Considerations

### Validating Input

```python
import re

def validate_filename(filename):
    """Prevent path traversal."""
    if ".." in filename or "/" in filename:
        raise ValueError("Invalid filename")
    return filename

def validate_sql(query):
    """Basic SQL injection prevention."""
    # Better: Use parameterized queries
    if "DROP" in query.upper() or "DELETE" in query.upper():
        raise ValueError("Dangerous query")
    return query
```

### Protecting API Endpoints

```python
from flask import request
import hmac
import hashlib

def verify_signature(request):
    """Verify request signature."""
    signature = request.headers.get('X-Signature')
    body = request.get_data()
    expected = hmac.new(
        b"secret", body, hashlib.sha256
    ).hexdigest()
    return signature == expected
```

---

## 📊 Data Management

### Extending Storage

Current storage:
- SQLite: Conversation history
- JSON: Notes, calendar, automations

### Database Queries

```python
# In assistant/db.py

def custom_query(query, params=None):
    """Execute custom query."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    result = cursor.execute(query, params or []).fetchall()
    conn.close()
    return result
```

### Backup & Restore

```python
import shutil
from datetime import datetime

def backup():
    """Backup all data."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copytree("data", f"backups/data_{timestamp}")

def restore(backup_path):
    """Restore from backup."""
    shutil.copytree(backup_path, "data", dirs_exist_ok=True)
```

---

## 🧪 Testing

### Unit Tests

```python
# test_features.py

import unittest
from assistant.features import weather

class TestWeather(unittest.TestCase):
    def test_get_weather(self):
        result = weather.get_weather("London")
        self.assertIn("temperature", result)
        self.assertIsNotNone(result["city"])

if __name__ == '__main__':
    unittest.main()
```

### Run Tests

```bash
python -m pytest test_features.py -v
```

---

## 🚀 Performance Optimization

### Caching Results

```python
from functools import lru_cache
from datetime import datetime, timedelta

class CachedFeature:
    def __init__(self):
        self.cache = {}
        self.cache_times = {}
    
    def get_with_cache(self, key, func, ttl=300):
        """Get data with TTL cache."""
        now = datetime.now()
        if key in self.cache:
            if now - self.cache_times[key] < timedelta(seconds=ttl):
                return self.cache[key]
        
        result = func()
        self.cache[key] = result
        self.cache_times[key] = now
        return result
```

### Async Operations

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=3)

def async_operation(func, *args):
    """Run function asynchronously."""
    return executor.submit(func, *args)
```

---

## 📚 Resources

### Official Documentation
- Gemini API: https://ai.google.dev/
- Flask: https://flask.palletsprojects.com/
- Flask-SocketIO: https://python-socketio.readthedocs.io/

### Libraries Used
- `pystray` - System tray
- `keyboard` - Global hotkeys
- `google-generativeai` - Gemini API
- `flask` - Web framework
- `psutil` - System monitoring

---

## 🐛 Debugging

### Enable Debug Mode

```python
# In background_service.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Logs

```bash
# View recent logs
tail -f logs/friday_service.log

# Search logs
grep "ERROR" logs/friday_service.log
```

### Debug API Calls

```bash
# Test endpoint
curl -X GET http://localhost:5000/api/health

# Post with data
curl -X POST http://localhost:5000/api/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","content":"Data"}'
```

---

## 🎓 Best Practices

1. **Keep features modular** - Each feature independent
2. **Use JSON for config** - Human-readable settings
3. **Document your code** - Clear docstrings
4. **Test thoroughly** - Unit and integration tests
5. **Handle errors gracefully** - Return meaningful messages
6. **Cache when possible** - Reduce API calls
7. **Validate input** - Prevent injection attacks
8. **Version your code** - Track changes
9. **Backup data regularly** - Prevent loss
10. **Monitor performance** - Track metrics

---

**Happy coding! 🚀**

For questions, check the main `README_ENHANCED.md` or review the source code examples in this guide.
