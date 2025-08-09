import subprocess

scripts = [
    "players_data.py",
    "analysis.py", 
    "players_scores.py",
    "bar_chart.py",
    "radar_diagram.py",
    # Add more scripts as needed
]

for script in scripts:
    print(f"Running {script}...")
    subprocess.run(["python", f"scripts/{script}"], check=True)
