# ⚽ La Liga Forwards Analysis

[![Build and Deploy](https://github.com/danishsyed-dev/la-liga-forwards-analysis/actions/workflows/deploy.yml/badge.svg)](https://github.com/danishsyed-dev/la-liga-forwards-analysis/actions/workflows/deploy.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)

Comprehensive data-driven analysis of the greatest forwards in La Liga history using Python, featuring an interactive web dashboard and advanced scoring metrics.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎯 **Interactive Dashboard** | Explore data through a beautiful Streamlit web app |
| 📊 **Multiple Visualizations** | Bar charts, radar charts, scatter plots, and season analysis |
| 🏆 **Comprehensive Scoring** | Custom points system based on goals, assists, titles, and awards |
| 📤 **Custom Data Upload** | Upload your own CSV data for analysis |
| 🌐 **Static Site** | GitHub Pages deployment with interactive Plotly charts |

---

## 🚀 Quick Start

### Option 1: Run Locally

```bash
# Clone the repository
git clone https://github.com/danishsyed-dev/la-liga-forwards-analysis.git
cd la-liga-forwards-analysis

# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the web app
streamlit run app.py
```

**Alternative launchers:**
- **Windows**: Double-click `run_app.bat`
- **Linux/Mac**: Run `./run_app.sh`

The app will open at `http://localhost:8501`

### Option 2: View Static Site

🔗 **[Live Demo on GitHub Pages](https://danishsyed-dev.github.io/la-liga-forwards-analysis/)**

---

## 📁 Project Structure

```
la-liga-forwards-analysis/
├── 📂 src/                          # Main source code
│   ├── core/                        # Core analysis modules
│   │   ├── analysis.py              # Score calculation logic
│   │   └── players_data.py          # Player data & scoring system
│   ├── handlers/                    # Data handlers
│   │   └── csv_handler.py           # CSV upload & validation
│   └── visualizations/              # Chart generation
│       ├── bar_chart.py             # Bar chart module
│       └── radar_diagram.py         # Radar chart module
├── 📂 tests/                        # Test suite
│   ├── test_analysis.py             # Analysis tests
│   └── test_csv_handler.py          # CSV handler tests
├── 📂 docs/                         # Generated static site
├── 📂 outputs/                      # Generated charts & data
├── 📂 .github/workflows/            # CI/CD pipeline
│   └── deploy.yml                   # Build, test & deploy
├── 📂 .streamlit/                   # Streamlit configuration
├── 📄 app.py                        # Main Streamlit application
├── 📄 generate_static.py            # Static site generator
├── 📄 requirements.txt              # Python dependencies
├── 📄 pyproject.toml                # Modern Python config
└── 📄 LICENSE                       # MIT License
```

---

## 📊 Using Custom Data

### Step 1: Prepare Your Data

Download the CSV template from the app or create your own with these required columns:

| Column | Type | Description |
|--------|------|-------------|
| `player_name` | string | Player's full name |
| `career_goals` | integer | Total La Liga goals |
| `total_la_liga_titles` | integer | Number of league titles |
| `total_champions_league_titles` | integer | Number of CL titles |

**Optional columns:**
- `ballon_dor_wins` - Number of Ballon d'Or awards
- `season_X_goals`, `season_X_assists` - Season stats (X = 1, 2, 3)
- `season_X_awards` - Comma-separated awards

### Step 2: Upload & Analyze

1. Select **"📊 Upload Custom CSV"** in the sidebar
2. Upload your CSV file
3. View automatic analysis and visualizations!

### Example CSV

```csv
player_name,career_goals,total_la_liga_titles,total_champions_league_titles,ballon_dor_wins
Lionel Messi,474,10,4,4
Cristiano Ronaldo,311,2,4,4
Luis Suárez,147,4,1,0
```

---

## 🏆 Scoring System

| Achievement | Points |
|-------------|--------|
| Ballon d'Or Win | 5 |
| Champions League Win | 5 |
| CL Top Scorer | 5 |
| 200+ La Liga Goals | 5 |
| La Liga Best Player Award | 4 |
| La Liga Golden Boot | 3 |
| 100+ La Liga Goals | 2 |
| 20+ Goal La Liga Season | 2 |
| Most Assists in La Liga Season | 2 |
| La Liga Title | 1 |
| 10+ Assist La Liga Season | 1 |
| Cup Final Winner | 1 |
| Other Trophies | 1 |

---

## 🛠️ Development

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Setup Development Environment

```bash
# Clone and setup
git clone https://github.com/danishsyed-dev/la-liga-forwards-analysis.git
cd la-liga-forwards-analysis

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v
```

### Running Scripts

```bash
# Run Streamlit app
streamlit run app.py

# Generate static site
python generate_static.py
```

---

## 🚀 Deployment

### GitHub Pages (Automatic)

The static site automatically deploys via GitHub Actions on every push to `main`:

1. Tests run on all pushes and PRs
2. Static HTML generates on merge to main
3. Deploys to: `https://danishsyed-dev.github.io/la-liga-forwards-analysis/`

### Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub account
3. Select this repository
4. Set main file: `app.py`
5. Deploy!

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Danish Syed**
- GitHub: [@danishsyed-dev](https://github.com/danishsyed-dev)

---

<div align="center">
  <p>
    <strong>⚽ Discover the Greatest La Liga Forwards!</strong>
  </p>
  <p>
    <a href="https://danishsyed-dev.github.io/la-liga-forwards-analysis/">View Live Demo</a>
    ·
    <a href="https://github.com/danishsyed-dev/la-liga-forwards-analysis/issues">Report Bug</a>
    ·
    <a href="https://github.com/danishsyed-dev/la-liga-forwards-analysis/issues">Request Feature</a>
  </p>
</div>
