# 🚀 Performance Testing with Locust, Prometheus & Grafana

---

## 📌 Overview

This project integrates **Locust** 🐍 for load testing, **Prometheus** 📊 for metric collection, and **Grafana** 📈 for real-time visualization. The goal is to simulate high-traffic scenarios, monitor system performance, and analyze results efficiently.

---

## 🛠️ Tech Stack

- **Locust** 🐍 - Load testing framework (Python)
- **Prometheus** 📊 - Metrics collection and monitoring
- **Grafana** 📈 - Dashboard visualization
- **Docker** 🐳 - Containerization
- **Jaeger** 🕵️ - Distributed tracing
- **Playwright** 🎭 - UI automation testing

---

## 📂 Project Structure

 ```bash
 📁 locust-prometheus-grafana
  ├── 📁 locust
  │   ├── locustfile.py        # Locust test scenarios
  │   ├── requirements.txt     # Python dependencies
  │   ├── config.yaml          # Config file
  ├── 📁 prometheus
  │   ├── prometheus.yml       # Prometheus configuration
  ├── 📁 grafana
  │   ├── grafana.ini          # Grafana settings
  ├── 📁 tracing
  │   ├── docker-compose.yml   # Jaeger setup
  ├── docker-compose.yml       # Full stack deployment
  ├── README.md                # Documentation
 ```

---

## 🚀 Getting Started

### 1️⃣ Prerequisites

Ensure you have the following installed:

- **Docker** 🐳
- **Python 3.x** 🐍

### 2️⃣ Install Dependencies

 ```bash
 cd locust
 pip install -r requirements.txt
 ```

### 3️⃣ Run Locust Load Test

 ```bash
 locust -f locustfile.py --headless --users 1000 --spawn-rate 5 --host=https://your-app.com
 ```

### 4️⃣ Run Prometheus & Grafana

Using **Docker Compose**:

 ```bash
 docker-compose up -d
 ```

Access **Grafana** at: [http://localhost:3000](http://localhost:3000)

---

## 📊 Monitoring & Observability

### 🔹 **Prometheus Metrics Endpoint**

Locust exposes metrics at: `http://localhost:8000/metrics`

### 🔹 **Jaeger Distributed Tracing**

 ```bash
 docker run -d --name jaeger -p 16686:16686 jaegertracing/all-in-one:latest
 ```

Access **Jaeger UI** at: [http://localhost:16686](http://localhost:16686)

---

## 🧪 UI Automation Testing

Run Playwright tests:

 ```python
 from playwright.sync_api import sync_playwright

 with sync_playwright() as p:
     browser = p.chromium.launch()
     page = browser.new_page()
     page.goto("https://your-app.com")
     print(page.title())
     browser.close()
 ```

---

## 📢 Alerts & Notifications

Configure **Prometheus Alertmanager** to send Slack alerts:

 ```yaml
 receivers:
   - name: 'slack'
     slack_configs:
       - channel: '#alerts'
         api_url: 'https://hooks.slack.com/services/...'
 ```

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 🤝 Contributing

Pull requests are welcome! Feel free to **fork** this repo and submit improvements. 🚀

---

🔥 **Happy Testing!** 🏆

---
