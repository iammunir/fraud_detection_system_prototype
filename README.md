# Fraud Detection System Prototype

## Setting Up and Running the App

**Prerequisites**

- **Docker**: Install Docker and Docker Compose on your system.

- **Python**: Install Python 3.x locally if running outside Docker. Version 3.10.12 is recommended.

- **NodeJS**: Install NodeJS locally if running outside Docker. Version 18.18.0 is recommended.

- **PostgreSQL**: Install PostgreSQL locally if running outside Docker.

- **Redis**: Install Redis locally if running outside Docker.

- **RethinkDB**: Install RethinkDB locally if running outside Docker.

### Running in Docker

- Clone the Repository:
```
git clone https://github.com/iammunir/fraud_detection_system_prototype.git
```

- Download the model in pickle format from [here](https://drive.google.com/file/d/1NXgzNhxQjMOlwGFaJx4YAWLntOF4F7Qu/view?usp=drive_link) and paste in `fraud_detection_backend/config/random_forest_adasyn.pkl`

- Build and Start Containers
```
docker compose up --build
```

- Accessing Services
    - Access Services API on http://localhost:5000
    - Access Web Dashboard on http://localhost:3000

- Stopping Services:
```
docker compose down
```

### Running Locally

- Clone the Repository:
```
git clone https://github.com/iammunir/fraud_detection_system_prototype.git
```

- Download the model in pickle format from [here](https://drive.google.com/file/d/1NXgzNhxQjMOlwGFaJx4YAWLntOF4F7Qu/view?usp=drive_link) and paste in `fraud_detection_backend/config/random_forest_adasyn.pkl`

- Set Up Python Virtual Environment:
```
python -m venv .venv
```

- Activate Virtual Environment
```
source .venv/bin/activate   # unix

venv\Scripts\activate.bat   # windows 
```

- Install Dependencies:
```
cd fraud_detection_backend
pip install -r requirements.txt
```

- Start **PostgreSQL**, **RethinkDB** and **Redis** Services: Ensure PostgreSQL, RethinkDB and Redis are running locally. Use Docker or local installations if required. Update settings.py or .env file with correct connection strings.

- Initial Setup for RethinkDB: Create a database named `fraud_detection` and a table named `transactions`

- Run Celery Worker: In a new terminal:
```
cd fraud_detection_backend
celery -A app.celery_app worker -l info
```

- Run Flask Development Server:
```
python run.py
```

- Install NextJS Dependencies:
```
cd fraud-detection-system 
npm install
```

- Run NextJS Dev Server:
```
npm run dev
```

- Accessing Services
    - Access Services API on http://localhost:5000
    - Access Web Dashboard on http://localhost:3000
