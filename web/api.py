"""
FRIDAY Web API — Extended Routes for New Features
Provides API endpoints for calendar, weather, notes, and automations.
"""

from flask import jsonify, request
from datetime import datetime
from assistant.features import (
    system_monitor, weather, calendar, notes,
    remote, automations
)


def register_api_routes(app):
    """Register all API routes with Flask app."""

    # ════════════════════════════════════════════════════════════
    # SYSTEM & STATUS ENDPOINTS
    # ════════════════════════════════════════════════════════════

    @app.route("/api/system/status", methods=["GET"])
    def get_system_status():
        """Get comprehensive system status."""
        status = system_monitor.get_system_status()
        return jsonify(status)

    @app.route("/api/system/processes", methods=["GET"])
    def get_running_processes():
        """Get list of running applications."""
        apps = system_monitor.get_running_apps()
        return jsonify({"applications": apps})

    # ════════════════════════════════════════════════════════════
    # WEATHER ENDPOINTS
    # ════════════════════════════════════════════════════════════

    @app.route("/api/weather", methods=["GET"])
    def get_weather():
        """Get weather for a city."""
        city = request.args.get("city", "auto")
        weather_data = weather.get_weather(city)
        return jsonify(weather_data)

    # ════════════════════════════════════════════════════════════
    # CALENDAR ENDPOINTS
    # ════════════════════════════════════════════════════════════

    @app.route("/api/calendar/events", methods=["GET"])
    def get_calendar_events():
        """Get all calendar events."""
        events = calendar.get_all_events()
        return jsonify({"events": events})

    @app.route("/api/calendar/upcoming", methods=["GET"])
    def get_upcoming_events():
        """Get upcoming events."""
        hours = request.args.get("hours", 24, type=int)
        events = calendar.get_upcoming_events(hours)
        return jsonify({"events": events})

    @app.route("/api/calendar/event", methods=["POST"])
    def add_calendar_event():
        """Add a new calendar event."""
        data = request.get_json()
        try:
            event = calendar.add_event(
                title=data.get("title"),
                description=data.get("description", ""),
                date_time=data.get("date_time"),
                priority=data.get("priority", "normal")
            )
            return jsonify({"success": True, "event": event}), 201
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400

    @app.route("/api/calendar/event/<int:event_id>", methods=["DELETE"])
    def delete_calendar_event(event_id):
        """Delete a calendar event."""
        try:
            calendar.delete_event(event_id)
            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400

    # ════════════════════════════════════════════════════════════
    # NOTES ENDPOINTS
    # ════════════════════════════════════════════════════════════

    @app.route("/api/notes", methods=["GET"])
    def get_notes():
        """Get all notes."""
        all_notes = notes.get_all_notes()
        return jsonify({"notes": all_notes})

    @app.route("/api/notes/search", methods=["GET"])
    def search_notes_route():
        """Search notes."""
        query = request.args.get("q", "")
        results = notes.search_notes(query)
        return jsonify({"notes": results})

    @app.route("/api/notes/tag", methods=["GET"])
    def search_by_tag():
        """Search notes by tag."""
        tag = request.args.get("tag", "")
        results = notes.search_by_tag(tag)
        return jsonify({"notes": results})

    @app.route("/api/notes", methods=["POST"])
    def add_note():
        """Add a new note."""
        data = request.get_json()
        try:
            note = notes.add_note(
                title=data.get("title"),
                content=data.get("content"),
                tags=data.get("tags", [])
            )
            return jsonify({"success": True, "note": note}), 201
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400

    # ════════════════════════════════════════════════════════════
    # AUTOMATIONS ENDPOINTS
    # ════════════════════════════════════════════════════════════

    @app.route("/api/automations", methods=["GET"])
    def get_automations():
        """Get all automations."""
        autos = automations.get_automations()
        return jsonify({"automations": autos})

    @app.route("/api/automations", methods=["POST"])
    def create_automation():
        """Create a new automation."""
        data = request.get_json()
        try:
            auto = automations.create_automation(
                name=data.get("name"),
                trigger=data.get("trigger"),
                actions=data.get("actions", [])
            )
            return jsonify({"success": True, "automation": auto}), 201
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400

    @app.route("/api/automations/<int:auto_id>/toggle", methods=["PUT"])
    def toggle_automation(auto_id):
        """Toggle an automation on/off."""
        try:
            automations.toggle_automation(auto_id)
            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400

    # ════════════════════════════════════════════════════════════
    # APPLICATION CONTROL ENDPOINTS
    # ════════════════════════════════════════════════════════════

    @app.route("/api/app/open", methods=["POST"])
    def open_app():
        """Open an application."""
        data = request.get_json()
        app_name = data.get("app_name", "")
        result = remote.open_application(app_name)
        return jsonify({"message": result})

    @app.route("/api/app/close", methods=["POST"])
    def close_app():
        """Close an application."""
        data = request.get_json()
        app_name = data.get("app_name", "")
        result = remote.close_application(app_name)
        return jsonify({"message": result})

    # ════════════════════════════════════════════════════════════
    # HEALTH CHECK
    # ════════════════════════════════════════════════════════════

    @app.route("/api/health", methods=["GET"])
    def health_check():
        """Health check endpoint."""
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0"
        })

    return app
