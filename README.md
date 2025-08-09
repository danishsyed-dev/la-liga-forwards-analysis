# La Liga Forwards Analysis

This project analyzes the greatest forwards in La Liga history using Python scripts and an interactive web dashboard. It includes statistical analysis and visualizations like bar charts and radar diagrams.

## 🌟 Features

- **Interactive Web Dashboard**: Explore data through an interactive Streamlit app
- **Comprehensive Scoring System**: Custom points system based on goals, assists, titles, and awards
- **Multiple Visualizations**: Bar charts, radar charts, scatter plots, and detailed statistics
- **Season-by-Season Analysis**: Deep dive into individual player performances
- **Real-time Comparisons**: Compare multiple players side-by-side

## 🚀 Quick Start - Web App

### Run Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Run the web app
streamlit run app.py
```

**Alternative:**
- Windows: Double-click `run_app.bat`
- Linux/Mac: Run `./run_app.sh`

The app will open at `http://localhost:8501`

## 📊 Live Demo

🔗 **[Access Live Dashboard](https://la-liga-forwards-analysis.streamlit.app)** *(Coming soon)*

## 🛠️ Installation

**Prerequisites:**
- Python 3.7+ installed on your computer
- Libraries: `pandas`, `numpy`, `matplotlib`, `streamlit`, `plotly`

**Install Required Libraries:**
```bash
pip install -r requirements.txt
```

## 💻 Usage

### Web Dashboard (Recommended)
1. Run `streamlit run app.py`
2. Open your browser to `http://localhost:8501`
3. Use the sidebar controls to:
   - Select players to compare
   - Choose visualization types
   - Explore different metrics

### Command Line Scripts
Your analysis is split into modular Python scripts in the `scripts/` folder.

**To run all scripts in order:**
```bash
python scripts/main.py
```

**Or run individually:**
```bash
python scripts/players_data.py
python scripts/players_scores.py
python scripts/bar_chart.py
python scripts/radar_diagram.py
```

## 🎯 Interactive Features

- **Player Selection**: Choose which players to analyze and compare
- **Visualization Types**: 
  - Bar charts for overall rankings
  - Radar charts for multi-dimensional comparison  
  - Detailed statistics with scatter plots
  - Season-by-season performance analysis
- **Real-time Updates**: All charts update instantly based on your selections
- **Export Options**: Save charts and download data

## 📈 Deployment

### Streamlit Cloud (Free)
1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Deploy from your forked repository
5. Set the main file path to `app.py`

### Other Platforms
- **Heroku**: Use the included `Procfile`
- **Railway**: Deploy directly from GitHub
- **Replit**: Import repository and run

## 🏗️ Project Structure

```
la-liga-forwards-analysis/
├── app.py              # Main Streamlit web application
├── scripts/            # Analysis scripts
│   ├── players_data.py # Player data and scoring system
│   ├── analysis.py     # Scoring calculation functions
│   ├── players_scores.py # Score computation
│   ├── bar_chart.py    # Bar chart generation
│   ├── radar_diagram.py # Radar chart generation
│   └── main.py         # Script runner
├── outputs/            # Generated plots and data
├── .streamlit/         # Streamlit configuration
├── requirements.txt    # Python dependencies
├── run_app.bat        # Windows launcher
├── run_app.sh         # Linux/Mac launcher
└── README.md          # This file
```

## 📊 Scoring System

The analysis uses a comprehensive points system:

| Achievement | Points |
|------------|--------|
| Ballon d'Or Win | 5 |
| Champions League Win | 5 |
| CL Top Scorer | 5 |
| La Liga Best Player Award | 4 |
| La Liga Golden Boot | 3 |
| 200+ La Liga Goals | 5 |
| 20+ Goal La Liga Season | 2 |
| Most Assists in La Liga | 2 |
| 100+ La Liga Goals | 2 |
| La Liga Title | 1 |
| 10+ Assist La Liga Season | 1 |
| Cup Final Winner | 1 |
| Other Trophies | 1 |

## 🎮 How to Use the Web App

1. **Select Players**: Use the sidebar to choose which players to compare
2. **Choose Visualization**: Pick from Bar Chart, Radar Chart, Detailed Stats, or Season Analysis
3. **Explore Data**: Click on different elements to see detailed information
4. **Compare Players**: Select multiple players to see side-by-side comparisons
5. **Season Analysis**: Deep dive into individual player's season-by-season performance

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

MIT License - see LICENSE file for details

---

**🚀 Ready to explore? Run `streamlit run app.py` and discover the greatest La Liga forwards!**
