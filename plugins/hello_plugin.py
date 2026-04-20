"""
Example Plugin for FRIDAY
Save this in the 'plugins/' folder.
"""

def handle_command(text):
    if "hello world" in text.lower():
        return "The plugin says: Hello from the digital void!"
    return None
