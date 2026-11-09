# MarketMosaic — AI-Powered Commercial Intelligence and Marketing Budget Optimization Platform

## 🎯 Project Overview

MarketMosaic is an advanced analytics platform designed to help businesses optimize their marketing spend across multiple channels using statistical modeling, machine learning, and mathematical optimization techniques.

## 📊 Business Problem

Modern businesses allocate budgets across diverse marketing channels (Google Ads, Facebook Ads, Email Campaigns, TV Ads, etc.) but struggle to answer critical questions:

1. **Which marketing channels perform best?**
2. **How does marketing spend relate to revenue?**
3. **How can future sales be forecast accurately?**
4. **How should marketing budgets be optimally distributed?**
5. **How reliable are the model's recommendations?**

## 🎯 Project Objectives

- **Quantify ROI** of each marketing channel
- **Forecast sales** using historical data
- **Optimize budget allocation** across channels
- **Provide uncertainty quantification** for recommendations
- **Create interactive visualizations** for business users
- **Build a scalable, production-ready** analytics platform

## 🏗️ Proposed System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Ingestion │───▶│  Data Processing │───▶│   Statistical   │
│   (CSV, APIs,    │    │  (Cleaning,      │    │    Modeling    │
│    Databases)    │    │   Transformation) │    │   (MMM, ML)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │                           │
                              ▼                           ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Visualization  │◀───│  Optimization   │◀───│   Forecasting   │
│   (Dashboards,  │    │  (Budget        │    │  (Time Series,  │
│     Reports)    │    │   Allocation)   │    │    ML Models)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Planned Technology Stack

### Core Technologies
- **Python 3.9+** - Primary programming language
- **Pandas/NumPy** - Data manipulation
- **Scikit-learn** - Machine learning
- **Statsmodels** - Statistical modeling
- **Matplotlib/Seaborn** - Visualization
- **Jupyter** - Exploratory analysis

### Future Additions
- **FastAPI** - REST API development
- **MySQL 8.x** - Relational data storage
- **SQLAlchemy/PyMySQL** - Database access
- **Docker** - Containerization
- **AWS/GCP** - Cloud deployment
- **Streamlit/Dash** - Interactive dashboards

## 📁 Repository Structure

```
MarketMosaic/
├── data/                    # Data directory
│   ├── raw/                # Original, immutable data
│   ├── interim/            # Intermediate data during processing
│   └── processed/          # Final, analysis-ready data
├── notebooks/              # Jupyter notebooks for exploration
├── src/                    # Source code
├── tests/                  # Test files
├── reports/                # Analysis reports and documentation
├── docs/                   # Project documentation
├── README.md               # This file
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
└── pyproject.toml         # Project configuration
```

## 🚀 Installation Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/bhumishah28/MarketMosaic.git
cd MarketMosaic
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
```

### 3. Activate Virtual Environment
**Windows:**
```bash
.venv\Scripts\activate
```
**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

## 📈 Development Roadmap

### Phase 1: Project Setup & Data Inspection ✅
- [x] Initialize repository structure
- [x] Set up Python environment
- [x] Download and inspect dataset
- [x] Create basic data inspection module
- [x] Implement data quality checks

### Phase 2: Data Preprocessing & EDA
- [x] Exploratory data analysis
- [x] Statistical summary generation
- [x] Correlation analysis
- [ ] Data cleaning and transformation for modelling

### Phase 3: Statistical Modeling
- [ ] Implement Marketing Mix Modeling (MMM)
- [ ] Time series decomposition
- [ ] Channel contribution analysis
- [ ] ROI calculation

### Phase 4: Machine Learning & Forecasting
- [ ] Sales forecasting models
- [ ] Budget optimization algorithms
- [ ] Uncertainty quantification

### Phase 5: Production Deployment
- [ ] API development
- [ ] Dashboard creation
- [ ] Cloud deployment
- [ ] CI/CD pipeline

## 🏗️ Current Implementation Status

### ✅ Implemented Features
- **Project structure** with organized directories
- **Git repository** linked to GitHub
- **MIT License** for open-source development
- **Python environment** setup instructions

### ✅ Completed in Week 1
- **Data inspection module** - Basic data quality checks
- **EDA module and notebook** - Descriptive statistics, channel/geography/time summaries, correlations, and visualisations
- **Test suite** - Unit tests for inspection and EDA functionality
- **Documentation** - Numerical data-audit and beginner-friendly milestone walkthrough

### 📋 Planned Features
- **Marketing Mix Modeling** - Statistical analysis of channel effectiveness
- **Budget optimization** - Mathematical optimization of spend allocation
- **Interactive dashboards** - Business user visualization interface
- **Production API** - REST API for integration with other systems

### Current ETL implementation

Reusable ETL modules live under `src/database` and `src/ingestion`. Run an
offline extraction/transformation reconciliation with:

```bash
python -m src.ingestion.run --dry-run
```

Set `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_DATABASE`, `MYSQL_USER`, and
`MYSQL_PASSWORD` (or use a local `.env` file) before running the database load.

## 🔍 Dataset Information

We're using **Google's Meridian simulated Marketing Mix Modeling dataset**:
- **Source**: https://github.com/google/meridian
- **File**: `geo_all_channels.csv`
- **Location**: `data/raw/geo_all_channels.csv`
- **Purpose**: Simulated data representing multi-channel marketing performance across different geographies

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_inspect_data.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Bhumi Shah** - [GitHub](https://github.com/bhumishah28)

## 🙏 Acknowledgments

- **Google Meridian Project** for the simulated MMM dataset
- **Open-source community** for the amazing libraries and tools
- **Data science community** for best practices and methodologies

---
*"Data is a precious thing and will last longer than the systems themselves." - Tim Berners-Lee*