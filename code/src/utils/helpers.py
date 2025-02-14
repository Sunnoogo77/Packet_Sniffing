# Fonctions d’analyse
import platform

def detect_os():
    """Detecte le système d'exploitation."""
    
    os_name = platform.system().lower()
    if "linux" in os_name:
        return "linux"
    elif "windows" in os_name:
        return "windows"
    return "unknown"