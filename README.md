# 📊 Stock Price Analysis Dashboard

## 🚀 Overview

This project is a **Flask-based Web Dashboard** for analyzing stock market data. It provides an interactive interface for users to visualize stock price trends, analyze performance metrics, and generate strategy-based insights using user-defined configurations.

The dashboard is designed for both traders and data analysts to make informed decisions using real-time or historical financial data.

---

## ✨ Key Features

* 📈 Interactive stock price visualization (line charts, candlestick charts)
* 📊 Technical analysis indicators (EMA, SMA, RSI, MACD)
* 🔄 Customizable strategies using `config.json`
* 🗂 Modular design with separate backend (Flask) and frontend files
* 🌐 Web-based interface built using HTML, CSS, JavaScript

---

## 📂 Project Structure

```
📦 dashboard_for_stock_price_analysis/
├── 📁 artifacts/       # Stores model files or pre-calculated strategy data
├── 📁 src/             # Core backend logic (data fetching, indicator calculations)
├── 📁 static/          # Frontend assets (JS, CSS, images)
├── 📁 templates/       # HTML templates for UI rendering
├── app.py              # Main Flask application entry point
├── config.json         # Strategy and analysis configuration file
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## 🛠️ Technology Stack

| Component     | Technology Used                  |
| ------------- | -------------------------------- |
| Backend       | Flask (Python)                   |
| Frontend      | HTML, CSS, JavaScript            |
| Data Source   | yFinance / CSV / API integration |
| Visualization | Plotly / Matplotlib              |

---

## 📦 Installation & Setup

Follow these steps to run the project locally:

```bash
# 1. Clone the repository
git clone https://github.com/tusharkolekar24/dashboard_for_stock_price_analysis
cd dashboard_for_stock_price_analysis

# 2. Create and activate virtual environment (optional)
python -m venv venv
source venv/bin/activate     # Mac/Linux
venv\Scripts\activate       # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python app.py
```

Now open your browser and visit: **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

---

## ⚙️ Configuration

You can customize the dashboard behavior using `config.json`:

```json
{
  "stock_symbol": "AAPL",
  "interval": "1d",
  "strategies": ["SMA", "EMA", "RSI"]
}
```

---

## 📊 Dashboard Features Explained

| Feature             | Description                                                   |
| ------------------- | ------------------------------------------------------------- |
| Real-time Charts    | Get live visualizations of stock price movements              |
| Historical Analysis | Compare stock trends over selected date ranges                |
| Strategy Insights   | Apply technical indicators and view buy/sell signals          |
| Model Integration   | If provided in artifacts, predictive analytics can be enabled |

---

## 🤖 AI / ML Integration (Optional)

If the `artifacts/` folder contains saved ML models, the dashboard can use them to:

* Predict future price movement
* Generate entry/exit signals

---

## 🔮 Future Enhancements

* ✅ Add portfolio management
* ✅ Include sentiment analysis using news headlines
* ✅ Deploy on cloud platforms (AWS, Render, Railway)
* ✅ User authentication & personalized dashboard

---

## 🤝 Contributions

Contributions, issues, and feature requests are welcome! Feel free to open a PR.

---

## 📄 License

This project is licensed under the **MIT License**.

---

### ⭐ If you find this project helpful, please give it a star on GitHub to support further development!


Home page: Volume & Stock analysis to give buy and sell signals.
<img width="1900" height="943" alt="image" src="https://github.com/user-attachments/assets/15464079-6e9b-410d-9793-8100591a7ea8" />

Sector Page: Sector Analysis
<img width="1908" height="932" alt="image" src="https://github.com/user-attachments/assets/52ac24bf-4056-4b56-888a-be7900c9a921" />

Strategy page: Price action Analysis
<img width="1904" height="940" alt="image" src="https://github.com/user-attachments/assets/32345a17-cdfb-4541-bcd4-37a8cf9af970" />
