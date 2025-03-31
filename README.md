# 🚀 **Load Testing with Locust, InfluxDB, and Grafana**

## 📌 **Overview**

This project integrates **Locust** 🐍 for load testing, **InfluxDB** 📊 for metric collection, and **Grafana** 📈 for real-time visualization. The goal is to simulate high-traffic scenarios, monitor system performance, and analyze results efficiently. The entire environment is orchestrated with **Docker Compose** for easy deployment and execution.

---

## 📚 **Project Structure**

  ``` plaintext
  📂 load-testing-locust/
  │── 📂 app/                   # Source code of the application under test
  │── 📂 config/                # Configuration files for Docker, InfluxDB, Locust, and Grafana
  │── 📂 docs/                  # Documentation and reports
  │── 📂 observability/         # Metrics and tracing configuration
  │── 📂 scripts/               # Automation and execution scripts
  │── 📂 tests/                 # Load testing scripts with Locust
  │── 📂 Makefile               # Automation commands
  │── docker-compose.yml        # Service orchestration with Docker
  │── README.md                 # Main documentation
  │── setup.sh                  # Installation script
  ```

---

## ✅ **Prerequisites**

Ensure you have the following installed before running the project:

- 🐳 **[Docker](https://www.docker.com/)** and **Docker Compose**
- 🐍 **[Python 3.x](https://www.python.org/)** (for manual testing if needed)
- 💪 **[Make](https://www.gnu.org/software/make/)** (for automation)

---

## ⚙️ **Installation and Configuration**

1️⃣ Clone the repository:

   ```sh
   git clone https://github.com/omaciasd/load-testing-locust.git
   cd load-testing-locust
   ```

2️⃣ Copy the environment variables template:

   ```sh
   cp config/.env.example config/.env
   ```

   Then edit `config/.env` to customize settings.

3️⃣ Build and start the services:

   ```sh
   make up
   ```

---

## 🛠️ **Using the Makefile**

The `Makefile` provides simple commands for managing the environment:

- **Rebuild services:**

  ```sh
  make rebuild
  ```

- **View logs:**

  ```sh
  make logs
  ```

- **Run tests:**

  ```sh
  make test
  ```

---

## 🏁 **1️⃣ Access the Locust UI**

Open your browser and go to:
   👉 [http://localhost:8089](http://localhost:8089)
Here, you can define the number of users and the ramp-up rate to start the test.

## 📊 **2️⃣ Monitor Metrics in Grafana**

Access Grafana at:
   👉 [http://localhost:3000](http://localhost:3000)

A preconfigured dashboard for Locust metrics is available. Navigate to **Dashboards → Load Testing Overview** to analyze key metrics such as:

- Requests per second (RPS)
- Response times
- Error rates
- Active users

---

## 🔍 **Verify Data in InfluxDB**

To check if Locust is sending data to InfluxDB, run:

   ```sh
   docker exec -it influxdb influx query --org my-org 'from(bucket:"locust_metrics") |> range(start: -5m)'
   ```

You should see response times and HTTP status codes.

---

## 🛡️ **Stop and Clean Up the Environment**

To stop services:

   ```sh
   make down
   ```

To remove all stored volumes and data:

   ```sh
   make clean
   ```

---

## 🐜 **License**

This project is licensed under the **MIT License**.

---

## 🤝 **Contributing**

1. Fork the repository
2. Create a new branch (`git checkout -b feature-new`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature-new`)
5. Open a Pull Request

Pull requests are welcome! Feel free to **fork** this repo and submit improvements. 🚀

---

🔥 **Happy Testing!** 🏆

---
