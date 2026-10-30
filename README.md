# 🚀 TubePredict: YouTube Video CTR & Virality Predictor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Chrome Extension](https://img.shields.io/badge/Chrome_Extension-Manifest_V3-4285F4.svg?logo=googlechrome&logoColor=white)](https://developer.chrome.com/docs/extensions/mv3/)

> **TubePredict** is an end-to-end Machine Learning web extension and FastAPI microservice designed to help content creators forecast whether a planned YouTube upload will rank in the **top quartile of viewership (top 25%)** before hitting publish.

---

## 🌟 Key Features

* **⚡ Real-Time Virality Scoring**: Generates an algorithmic potential score ($0-100\%$) indicating likelihood of outperforming channel benchmarks.
* **🎯 Live YouTube Studio Integration**: Automatically parses draft titles directly from the upload and edit dialogs inside `studio.youtube.com`.
* **🧠 Linguistic & Heuristic Feature Extraction**:
  * Capitalization ratio and visual contrast analysis.
  * Curated title polarity and sentiment scoring.
  * Power/hook keyword detection (`Ultimate`, `Secret`, `Must`, `Fast`).
  * Numerical curiosity patterns.
* **📅 Scheduling & Temporal Intelligence**: Evaluates publish hour and day-of-week impact on initial velocity.
* **💡 Actionable Recommendations**: Returns immediate optimization tips for boosting click-through rates (CTR).

---

## 📂 Repository Architecture

```text
youtube-predictor-extension/
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions automated test workflow
├── backend/
│   ├── main.py                # FastAPI microservice with global CORS support
│   ├── feature_engineering.py # NLP, sentiment, and metadata extraction engine
│   ├── model.joblib           # Pre-trained Gradient Boosted decision model
│   ├── features.joblib        # Model feature schema
│   ├── Dockerfile             # Production container definition
│   └── requirements.txt       # Python dependencies
├── extension/
│   ├── manifest.json          # Chrome/Brave/Edge Manifest V3 specification
│   ├── popup.html             # Clean dark-themed popup UI
│   ├── popup.js               # Frontend extension state & API caller
│   ├── content.js             # DOM extractor for YouTube Studio & YouTube
│   └── icons/                 # 16px, 48px, 128px high-resolution icons
├── .gitignore                 # Standard Python & OS ignore rules
├── LICENSE                    # MIT License
└── README.md                  # Project documentation
```

---

## 🛠️ Quickstart Guide

### 1. Backend API Setup

Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/your-username/tube-predict.git
cd tube-predict/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Interactive OpenAPI Swagger documentation will be available at: **`http://localhost:8000/docs`**

---

### 2. Chrome / Brave / Edge Extension Installation

1. Open your browser and navigate to the extensions page:
   * **Chrome**: `chrome://extensions/`
   * **Brave**: `brave://extensions/`
   * **Edge**: `edge://extensions/`
2. Enable **Developer mode** in the top right corner.
3. Click **Load unpacked** and select the **`extension/`** folder from this repository.
4. Pin **TubePredict** to your browser toolbar.

---

## 🌐 Deploying to Production (Worldwide Access)

### Backend Deployment (Docker / Cloud Host)
You can deploy the backend container instantly to **Render**, **Railway**, **Google Cloud Run**, or **AWS EC2**:

```bash
cd backend
docker build -t tubepredict-api .
docker run -p 8000:8000 tubepredict-api
```

### Chrome Web Store Distribution
1. Update `extension/popup.js` line `40` to point to your live cloud URL instead of `localhost`:
   ```javascript
   const res = await fetch("https://your-api-domain.com/predict", { ... });
   ```
2. Compress the contents of `extension/` into a `.zip` file.
3. Upload to the [Chrome Developer Dashboard](https://chrome.google.com/webstore/devconsole).

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a PR:
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.
