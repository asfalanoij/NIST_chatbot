import subprocess

def run_security_scan():
    """
    Runs a basic security scan using 'pip-audit' or simulates one if not installed.
    """
    try:
        # Check if pip-audit is installed
        result = subprocess.run(
            ["pip-audit"], 
            capture_output=True, 
            text=True
        )
        if result.returncode == 0:
            return "✅ No known vulnerabilities found."
        else:
            return f"⚠️ Vulnerabilities found:\n{result.stdout}"
    except FileNotFoundError:
        return "ℹ️ pip-audit not installed. Install it via 'pip install pip-audit' to run scans."
    except Exception as e:
        return f"Error running security scan: {e}"

def check_secret_exposure(text):
    """
    Simple heuristic to check for potential secrets in text.
    """
    keywords = ["API_KEY", "SECRET", "PASSWORD", "private_key"]
    found = [kw for kw in keywords if kw in text.upper()]
    
    if found:
        return f"⚠️ POTENTIAL SECRET EXPOSURE DETECTED: {', '.join(found)}"
    return "✅ No obvious secrets detected."
