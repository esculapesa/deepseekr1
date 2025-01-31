
import subprocess
import os

def run_git_command(command):
    try:
        return subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return None

def commit_and_push(message="Update"):
    """Add all changes, commit, and push to remote"""
    commands = [
        "git add .",
        f'git commit -m "{message}"',
        "git push origin main"
    ]
    
    for cmd in commands:
        result = run_git_command(cmd)
        if result is None:
            return False
    return True

if __name__ == "__main__":
    from datetime import datetime
    commit_msg = f"Update {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    if commit_and_push(commit_msg):
        print(f"Successfully committed and pushed changes: {commit_msg}")
    else:
        print("Failed to commit and push changes")
