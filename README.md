## 🌍 Project Overview  
This project is part of my MSc in *Applied Computing and IT with Project Management* at the **University of Bedfordshire**.  
The goal is to design and implement an **IoT-based smart energy monitoring system** that:  
- Collects simulated energy usage data from multiple sensors.  
- Stores and processes data efficiently using a time-series database.  
- Predicts future energy consumption using a trained **LSTM deep learning model**.  
- Provides RESTful APIs to deliver real-time and predictive insights to a web dashboard (ReactJS frontend).  

---

## ⚙️ Tech Stack  
| Layer | Technology |
|-------|-------------|
| **Backend Framework** | FastAPI (Python) |
| **Database** | PostgreSQL + TimescaleDB |
| **Cache / Queue** | Redis |
| **Machine Learning** | TensorFlow, Pandas, NumPy, Scikit-learn |
| **Containerization** | Docker, Docker Compose |
| **Frontend** | ReactJS *(under development)* |
| **Version Control** | Git + GitHub |

---

## 🧩 Project Architecture  

backend/
├── app/
│ ├── api/ # FastAPI routes and endpoints
│ ├── services/ # Business logic and ML integrations
│ ├── db/ # Database models and connections
│ ├── core/ # Schemas and custom exceptions
│ └── main.py # FastAPI app entry point
├── ml/
│ ├── training/ # LSTM model training scripts
│ ├── models/ # Saved ML models and scalers
│ └── reports/ # Training metrics and logs
├── docker/
│ ├── Dockerfile
│ ├── Dockerfile.dev
│ └── docker-compose.yml
└── tests/
└── unit/ and integration tests

yaml
Copy code

---

## 🚀 Features  
✔️ Real-time energy data simulation and storage  
✔️ RESTful API endpoints for data access  
✔️ Predictive analytics using LSTM  
✔️ Dockerized services for easy deployment  
✔️ Structured logging and environment-based configuration  

---

## 🔧 How to Run Locally  

### 1️⃣ Clone the repository
```bash
git clone https://github.com/orjiugo/Smart-energy-Monitoring.git
cd Smart-energy-Monitoring