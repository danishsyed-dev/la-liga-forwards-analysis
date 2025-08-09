import subprocess
import os

# Only run scripts that are meant to be executed standalone
executable_scripts = [
    "players_scores.py",
    "bar_chart.py", 
    "radar_diagram.py",
]

# Change to scripts directory to ensure relative imports work
original_dir = os.getcwd()
scripts_dir = os.path.join(original_dir, 'scripts')

for script in executable_scripts:
    print(f"Running {script}...")
    try:
        # Run from the scripts directory for proper imports
        subprocess.run(["python", script], cwd=scripts_dir, check=True)
        print(f"✅ {script} completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ {script} failed with exit code {e.returncode}")
        raise
