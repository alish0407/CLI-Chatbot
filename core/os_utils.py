import platform

def get_os_type():
    os_name = platform.system().lower()
    if "windows" in os_name:
        return "windows"
    elif "linux" in os_name:
        return "linux"
    elif "darwin" in os_name:  # macOS is 'Darwin'
        return "mac"
    else:
        return "unknown"
