import subprocess

scripts = [
    "01_players_data.py",
    "02_players_score.py",
    "03_analysis.py",
    "04_bar_charts.py",
    "05_radar_diagram.py",
    # Add more scripts as needed
]

for script in scripts:
    print(f"Running {script}...")
    subprocess.run(["python", f"scripts/{script}"], check=True)
