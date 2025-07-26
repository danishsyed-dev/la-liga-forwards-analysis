# La Liga Forwards Analysis

This project analyzes the greatest forwards in La Liga history using Python scripts. It includes statistical analysis and visualizations like bar charts and radar diagrams.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Workflow](#workflow)
- [Project Structure](#project-structure)
- [Files Included](#files-included)
- [License](#license)

## Introduction

The project compares legendary players based on goals, assists, titles, and awards, using custom scoring systems and visualizations.

## Features

- Calculate player scores using a custom points system.
- Generate bar charts comparing player scores.
- Create radar diagrams to visualize player stats across multiple metrics.

## Installation

**Prerequisites:**

- Python 3.x installed on your computer.
- Libraries: `pandas`, `numpy`, `matplotlib`.

**Install Required Libraries:**

```bash
pip install -r requirements.txt
```

## Usage

Your analysis is split into modular Python scripts in the `scripts/` folder. 
Each script was originally a Jupyter notebook cell, now converted for easier version control and reproducibility.

**To run all scripts in order:**
```bash
python scripts/01_load_data.py
python scripts/02_calculate_scores.py
python scripts/03_visualize_barcharts.py
python scripts/04_visualize_radar.py
# ...and so on
```
Alternatively, create a `main.py` or bash script to automate this sequence.

**Viewing Outputs:**
- Plots and tables are saved in the `outputs/` folder.
- Example: `outputs/player_scores_bar.png`, `outputs/radar_chart.png`

## Workflow

- Original analysis was performed in Jupyter notebooks for inline visualization.
- For better version control, each notebook cell is now a standalone `.py` script.
- Visual outputs are saved to disk (see `outputs/`) and can be referenced or previewed in the README.

## Project Structure

```
la-liga-forwards-analysis/
├── data/         # datasets, CSVs, raw or processed
├── scripts/      # analysis scripts (one per original notebook cell)
├── outputs/      # generated plots, tables, etc.
├── requirements.txt
└── README.md
```

## Files Included

- `scripts/`: All analysis code
- `data/`: Data files (not included in repo if too large)
- `outputs/`: Example plots and result tables
- `requirements.txt`: Dependencies
- `README.md`

## License

MIT License
