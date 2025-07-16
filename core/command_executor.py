import subprocess
from config.settings import DRY_RUN_MODE

def execute_command(command: str, cwd: str = None, dry_run: bool = DRY_RUN_MODE) -> dict:
    """
    Executes a shell command and returns structured output.

    Parameters:
    - command (str): The shell command to execute.
    - cwd (str): The directory in which to run the command.
    - dry_run (bool): If True, returns a simulated result without running.

    Returns:
    - dict with keys:
        - success (bool): True if command executed successfully.
        - output (str): Captured standard output.
        - error (str): Captured error output (if any).
    """
    if dry_run:
        return {
            "success": True,
            "output": f"[DRY RUN] The command would be: {command}",
            "error": ""
        }

    try:
        # Execute the command through the shell to support built-ins like cd, del, etc.
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10  # Limit to 10 seconds to prevent hanging
        )

        return {
            "success": result.returncode == 0,
            "output": result.stdout.strip(),
            "error": result.stderr.strip()
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": "⏱️ Command timed out after 10 seconds."
        }

    except FileNotFoundError:
        return {
            "success": False,
            "output": "",
            "error": "🚫 Command not found. Are you sure it's installed?"
        }

    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": f"❌ An unexpected error occurred: {str(e)}"
        }
