# ⚽ La Liga Forwards Analysis

[![Build and Deploy](https://github.com/danishsyed-dev/la-liga-forwards-analysis/actions/workflows/deploy.yml/badge.svg)](https://github.com/danishsyed-dev/la-liga-forwards-analysis/actions/workflows/deploy.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)

A comprehensive, data-driven analysis of the greatest forwards in **La Liga history** built with Python and Streamlit. The project features an interactive web dashboard with advanced scoring metrics comparing legendary players — powered by **verified data** scraped from [FBref](https://fbref.com/) and [Wikipedia](https://en.wikipedia.org/).

---

## ✨ Features and Capabilities

| Feature | Description |
|---------|-------------|
| 🎯 **Interactive Dashboard** | Explore historical data seamlessly through a Streamlit web interface with a responsive, modern UI layout. |
| 📊 **Multiple Visualizations** | Analyze using Bar Charts, comparative Radar Charts, Goals vs Titles scatter plots, and Season-by-Season analyses. |
| 🏆 **Advanced Scoring System** | Players are ranked via a granular points algorithm evaluating goals, assists, titles, Top Scorer awards, and Ballon d'Or podiums. |
| 📤 **4 Flexible Data Sources** | Use Default Legends, Verified CSV datasets, dynamically Generate Sample Data, or Upload your custom CSV for processing. |
| 🔄 **Automated Data Pipeline** | Wikipedia awards/honours data auto-scraped; FBref stats importable via CSV export. Monthly CI refresh supported. |
| 🌐 **Static Generation** | Ability to output analysis graphs to static HTML and deploy automatically to GitHub Pages. |

---

## 🚀 Quick Start

### Run the App Locally

```bash
# Clone the repository
git clone https://github.com/danishsyed-dev/la-liga-forwards-analysis.git
cd la-liga-forwards-analysis

# Create virtual environment (recommended)
python -m venv .venv
# Activate environment
# On Windows:
.venv\Scripts\activate
# On Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the web app
streamlit run app.py
```

**Alternative Windows Launcher:**
- Double-click `run_app.bat` to launch automatically.

*(The Streamlit application will start at `http://localhost:8501`)*

### View Deployed Web Version

🔗 **[Live Demo on GitHub Pages](https://danishsyed-dev.github.io/la-liga-forwards-analysis/)**  
🔗 **[Live on Streamlit](https://la-liga-forwards-analysis.streamlit.app/)**

---

## 📁 Project Structure

```text
la-liga-forwards-analysis/
├── 📂 src/                              # Main source code directory
│   ├── core/                            # Core analysis logic
│   │   ├── analysis.py                  # Scoring algorithm: calculates player scores from achievements
│   │   └── players_data.py              # Data loader: reads JSON dataset or falls back to built-in data
│   ├── handlers/                        # Data I/O handlers
│   │   ├── builtin_data_handler.py      # Loader for validated built-in datasets
│   │   └── csv_handler.py               # Robust CSV processing, validation, and template generation
│   └── visualizations/                  # Plotly chart drawing components
│       ├── bar_chart.py                 # Bar Chart generation logic
│       └── radar_diagram.py             # Multi-metric Radar comparison logic
├── 📂 scripts/                          # Data pipeline scripts
│   ├── config.py                        # Centralised configuration (URLs, paths, points system)
│   ├── scrape_wikipedia.py              # Wikipedia scraper (Pichichi, Ballon d'Or, titles, CL)
│   ├── scrape_fbref.py                  # FBref Selenium scraper (Cloudflare-protected)
│   ├── import_fbref_csv.py              # Manual FBref CSV importer (recommended workflow)
│   └── merge_data.py                    # Merges FBref stats + Wikipedia awards → unified JSON
├── 📂 data/                             # All datasets
│   ├── raw/                             # Raw scraped data
│   │   ├── wikipedia/*.json             # Scraped award data (pichichi, ballon_dor, etc.)
│   │   └── fbref/*.csv                  # Season-by-season player stats
│   ├── processed/                       # Unified datasets
│   │   ├── la_liga_all_players.json     # ⭐ Final merged dataset used by the app
│   │   └── players_summary.csv          # Quick-view summary table
│   └── verified_players.csv             # Legacy built-in dataset
├── 📂 tests/                            # Automated Pytest suite
│   ├── test_analysis.py                 # Unit tests for scoring logic accuracy
│   └── test_csv_handler.py              # Unit tests for CSV validation
├── 📂 docs/                             # GitHub Pages content (auto-generated)
├── 📂 .github/workflows/               # CI/CD pipelines
│   └── deploy.yml                       # Build, test, deploy + monthly data refresh
├── 📄 app.py                            # Streamlit web app entry point
├── 📄 generate_static.py                # Converts analysis into static interactive HTML
├── 📄 pyproject.toml                    # Modern Python tooling configs
└── 📄 requirements.txt                  # Python dependencies
```

---

## 🔄 Data Pipeline

The project uses a **two-source extraction pipeline** to gather verified data:

### Data Flow

```
┌─────────────┐     ┌──────────────────┐     ┌──────────────────────────┐
│  Wikipedia   │────▶│ scrape_wikipedia │────▶│ data/raw/wikipedia/*.json│
│  (Awards)    │     │      .py         │     │  • pichichi.json         │
└─────────────┘     └──────────────────┘     │  • ballon_dor.json       │
                                              │  • la_liga_titles.json   │
                                              │  • champions_league.json │
┌─────────────┐     ┌──────────────────┐     │  • la_liga_best_player   │
│   FBref      │────▶│ import_fbref_csv │────▶│ data/raw/fbref/*.csv     │
│  (Stats)     │     │      .py         │     └─────────┬────────────────┘
└─────────────┘     └──────────────────┘               │
                                                        ▼
                                              ┌──────────────────┐
                                              │  merge_data.py   │
                                              └────────┬─────────┘
                                                       ▼
                                              ┌──────────────────────────────┐
                                              │ data/processed/              │
                                              │   la_liga_all_players.json   │
                                              │   players_summary.csv        │
                                              └──────────────────────────────┘
```

### Running the Pipeline

```bash
# Step 1: Scrape Wikipedia awards (automated)
python scripts/scrape_wikipedia.py --force

# Step 2: Import FBref stats (manual CSV export — see instructions below)
python scripts/import_fbref_csv.py

# Step 3: Merge everything into the final dataset
python scripts/merge_data.py
```

### Getting FBref Data

FBref uses Cloudflare protection that blocks automated scrapers. To get stats data:

1. Open your browser and navigate to the [FBref La Liga Stats page](https://fbref.com/en/comps/12/stats/La-Liga-Stats)
2. Find the **"Standard Stats"** table
3. Click **"Share & Export" → "Get table as CSV (for Excel)"**
4. Save the CSV as `data/raw/fbref/<season>.csv` (e.g., `2023-2024.csv`)
5. Run `python scripts/import_fbref_csv.py` to process the CSVs

### Data Sources & Verification

| Source | Data Extracted | Method |
|--------|---------------|--------|
| **[FBref](https://fbref.com/)** (StatsBomb) | Season stats: goals, assists, matches, minutes | Manual CSV export |
| **[Wikipedia](https://en.wikipedia.org/)** — Pichichi Trophy | La Liga top scorer winners (1929–present) | Automated scraping |
| **[Wikipedia](https://en.wikipedia.org/)** — Ballon d'Or | Winners & podium finishers (1956–present) | Automated scraping |
| **[Wikipedia](https://en.wikipedia.org/)** — La Liga Awards | Best Player award winners | Automated scraping |
| **[Wikipedia](https://en.wikipedia.org/)** — Spanish Champions | La Liga title winners by season | Automated scraping |
| **[Wikipedia](https://en.wikipedia.org/)** — Champions League | UEFA CL winners by season | Automated scraping |

---

## 📊 Providing Your Own Data

You can supply your own player statistics directly inside the app using the sidebar. 

### Custom CSV Upload

1. Select **"📊 Upload Custom CSV"** in the sidebar.
2. Download a provided **Template** to see required columns.
3. Upload your CSV - the internal validation engine (`src/handlers/csv_handler.py`) will check it.
4. Download new insights directly inside the app after generation!

**Required standard columns:**
- `player_name` - Player's full name
- `career_goals` - Total La Liga goals
- `total_la_liga_titles` - Amount of La Liga league titles
- `total_champions_league_titles` - Amount of Champions League titles

**Optional deeper columns:**
- `ballon_dor_wins`
- `season_X_goals` & `season_X_assists` (For historical timeline charts)
- `season_X_awards` (Comma-separated values)

---

## 🏆 How the Scoring Engine Works

The core ranking evaluates everything from legacy to micro-achievements (defined in `src/core/players_data.py`).

| Achievement Category | Points |
|----------------------|--------|
| **Ballon d'Or Win**  | 5      |
| Ballon d'Or 2nd/3rd Place | 3 / 1 |
| **Champions League Win** | 5 |
| CL Top Scorer / Most Assists | 5 / 2 |
| **200+ / 100+ Career La Liga Goals** | 5 / 2 |
| La Liga Best Player Award | 4 |
| La Liga Golden Boot | 3    |
| 20+ Goal Season      | 2      |
| Most Assists in La Liga Season | 2 |
| **La Liga Title**    | 1      |
| Cup / Other Trophies | 1 (per trophy) |

*(Points logic explicitly prevents double-counting if an attribute is derived from something else).*

---

## 🛠️ Development & Contributions

### Code Setup

```bash
git clone https://github.com/danishsyed-dev/la-liga-forwards-analysis.git
cd la-liga-forwards-analysis

# Isolate environment 
python -m venv .venv
source .venv/bin/activate  # (.venv\Scripts\activate on Windows)

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v
```

### Pull Requests Are Welcome!

1. **Fork** the repository
2. Create a clean branch (`git checkout -b feature/cool-idea`)
3. Commit neatly (`git commit -m 'feat: Added cool idea'`)
4. **Push** branch and submit a PR to `main`.

---

## 📄 License and Author

- **Author**: Danish Syed ([@danishsyed-dev](https://github.com/danishsyed-dev))  
- **License**: MIT License ([LICENSE](LICENSE))
