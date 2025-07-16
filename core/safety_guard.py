import re

# 🛑 Patterns to warn the user about
DANGEROUS_PATTERNS = [
    r"rm\s+-rf\s+/",                      # Deletes root directory
    r"rm\s+-rf\s+\*",                     # Deletes all files in current directory
    r"shutdown\\b",                       # Shutdown system
    r"reboot\\b",                         # Reboot system
    r"mkfs\\b",                           # Format file system
    r":\\(\\)\\s*{\\s*:\\s*\\|\\s*:\\s*&\\s*};:",  # Fork bomb
    r"dd\\s+if=.*",                       # Disk overwrite
    r"mv\\s+/.*",                         # Move system files
    r"curl\\s+.*\\|\\s+sh",               # Pipe to shell (could execute malicious script)
    r"wget\\s+.*\\|\\s+sh",
    r"chmod\\s+777\\s+/.*",               # Too permissive on root files
]

# ✅ Whitelisted safe commands
SAFE_COMMANDS = [
    "ls", "pwd", "cd", "echo", "cat", "find", "whoami", "date", "dir"
]

def is_command_dangerous(command: str) -> bool:
    """
    Check if a command matches any known dangerous pattern.
    Returns True if it's risky.
    """
    command = command.strip().lower()

    if any(command.startswith(safe) for safe in SAFE_COMMANDS):
        return False

    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, command):
            return True

    return False

def danger_reason(command: str) -> str:
    """
    Returns a reason why the command is marked dangerous.
    """
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, command):
            return f"⚠️ Command matches a dangerous pattern → `{pattern}`.\nYou must confirm before execution."
    return "⚠️ This command is potentially unsafe and may alter or delete system files."
