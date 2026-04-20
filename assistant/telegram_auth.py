"""
FRIDAY Telegram Bot Authentication & Security
Handles user validation and command logging
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)


def validate_user(user_id: int, admin_ids: list) -> bool:
    """
    Validate if user is authorized
    
    Args:
        user_id: Telegram user ID
        admin_ids: List of authorized admin IDs
    
    Returns:
        bool: True if authorized, False otherwise
    """
    is_authorized = user_id in admin_ids
    
    if not is_authorized:
        logger.warning(f"⚠️ Unauthorized access attempt from user ID: {user_id}")
        log_command(user_id, "UNKNOWN", "REJECTED", "User not in admin list")
    
    return is_authorized


def log_command(user_id: int, command: str, status: str, details: str = "") -> None:
    """
    Log command execution for security audit
    
    Args:
        user_id: Telegram user ID
        command: Command executed
        status: SUCCESS, FAILED, REJECTED, ERROR
        details: Additional details
    """
    try:
        log_dir = Path.home() / ".friday" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / "telegram_commands.log"
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "command": command,
            "status": status,
            "details": details
        }
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + "\n")
        
        logger.info(f"📝 Command logged: {command} - {status}")
    
    except Exception as e:
        logger.error(f"Failed to log command: {e}")


def get_command_history(limit: int = 100) -> list:
    """
    Get command history
    
    Args:
        limit: Number of recent commands to retrieve
    
    Returns:
        list: List of command log entries
    """
    try:
        log_file = Path.home() / ".friday" / "logs" / "telegram_commands.log"
        
        if not log_file.exists():
            return []
        
        with open(log_file, 'r') as f:
            lines = f.readlines()
        
        history = []
        for line in lines[-limit:]:
            try:
                history.append(json.loads(line))
            except:
                continue
        
        return history
    
    except Exception as e:
        logger.error(f"Failed to retrieve command history: {e}")
        return []


def get_unauthorized_attempts(limit: int = 50) -> list:
    """
    Get unauthorized access attempts
    
    Args:
        limit: Number of recent attempts to retrieve
    
    Returns:
        list: List of unauthorized attempts
    """
    history = get_command_history(limit * 2)
    return [entry for entry in history if entry.get("status") == "REJECTED"]


def rate_limit_check(user_id: int, max_commands_per_minute: int = 10) -> bool:
    """
    Check if user exceeded rate limit
    
    Args:
        user_id: Telegram user ID
        max_commands_per_minute: Max commands allowed per minute
    
    Returns:
        bool: True if within limit, False if exceeded
    """
    try:
        history = get_command_history(limit=100)
        now = datetime.now()
        one_minute_ago = now - timedelta(minutes=1)
        
        recent_commands = 0
        for entry in history:
            if entry.get("user_id") == user_id:
                try:
                    cmd_time = datetime.fromisoformat(entry.get("timestamp", ""))
                    if cmd_time > one_minute_ago:
                        recent_commands += 1
                except:
                    continue
        
        if recent_commands > max_commands_per_minute:
            logger.warning(f"⚠️ Rate limit exceeded for user {user_id}")
            log_command(user_id, "RATE_LIMIT", "REJECTED", f"Exceeded {max_commands_per_minute} commands/min")
            return False
        
        return True
    
    except Exception as e:
        logger.error(f"Rate limit check failed: {e}")
        return True  # Allow if check fails
