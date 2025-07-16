import json
import os

# Path to your persistent log file
CONTEXT_FILE = "data/logs/command_log.json"

class ContextManager:
    def __init__(self):
        self.context_data = []
        self._load()

    def _load(self):
        """Load existing context from the JSON file."""
        if os.path.exists(CONTEXT_FILE):
            try:
                with open(CONTEXT_FILE, "r") as f:
                    self.context_data = json.load(f)
            except Exception:
                self.context_data = []
        else:
            self.context_data = []

    def _save(self):
        """Save context to the JSON file."""
        os.makedirs(os.path.dirname(CONTEXT_FILE), exist_ok=True)
        with open(CONTEXT_FILE, "w") as f:
            json.dump(self.context_data, f, indent=2)

    def add(self, instruction, command, output):
        """Add a new command to the context and persist it."""
        self.context_data.append({
            "instruction": instruction,
            "command": command,
            "output": output
        })
        self._save()

    def get_all(self):
        """Return all stored context data."""
        return self.context_data

    def clear(self):
        """Clear all stored context data and persist empty file."""
        self.context_data = []
        self._save()
