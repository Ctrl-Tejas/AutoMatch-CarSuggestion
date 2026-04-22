# AutoMatch India - Used Car Recommendation System

AutoMatch India is a sophisticated web application designed to help users find the perfect used car in the Indian market based on their lifestyle, budget, and preferences.

## 🚀 Features

- **Personalized Recommendations**: Uses a weighted matching algorithm to suggest the top 5 cars from our database.
- **Smart Survey**: A multi-step interactive survey capturing user needs (usage, safety, budget, etc.).
- **Admin Dashboard**: Real-time analytics on user preferences, budget distribution, and recent submissions.
- **Robust Backend**: Powered by FastAPI with SQLAlchemy ORM and structured logging.
- **Responsive Design**: Modern, glassmorphic UI built with Vanilla CSS and JS.

## 🛠️ Technology Stack

- **Backend**: Python 3.10+, FastAPI, SQLAlchemy, Pydantic, MySQL (via PyMySQL)
- **Frontend**: HTML5, Vanilla JavaScript, CSS3
- **Configuration**: Dotenv for environment management
- **Analytics**: Chart.js for data visualization

## 📂 Project Structure

```text
DissPro/
├── backend/            # FastAPI application logic
│   ├── data/           # Configurable data storage (CSV backups)
│   ├── main.py         # Entry point and API routes
│   ├── models.py       # SQL Alchemy database models
│   ├── schemas.py      # Pydantic data schemas
│   ├── database.py    # Database connection logic
│   └── recommendation.py # Recommendation algorithm
├── frontend/           # Static web assets
│   ├── assets/         # CSS, JS, and image assets
│   ├── index.html      # Landing page
│   ├── survey.html     # Recommendation survey
│   ├── admin.html      # Admin dashboard
│   ├── results.html    # Match results
│   └── cars.html       # Car database
├── docs/               # Project documentation and assets
├── .env                # Local environment secrets
├── .gitignore          # Git exclusion rules
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## ⚙️ Setup and Installation

### 1. Database Setup
- Ensure XAMPP is running and MySQL is active.
- Create a database named `used_cars_db`.

### 2. Backend Setup
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
- Copy `.env.example` to `.env`.
- Update `DATABASE_URL` if your MySQL configuration differs from the default.

### 4. Running the Application
Run the backend manually from the root:
```bash
python -m uvicorn backend.main:app --reload
```
Or from the backend folder:
```bash
cd backend
uvicorn main:app --reload
```

Open `frontend/index.html` in your browser to start using AutoMatch India!

## 🔐 Configuration

The application uses environment variables for easy deployment. See `.env.example` for details on available options including:
- `DATABASE_URL`: Connection string for MySQL.
- `SERVER_PORT`: Port for the FastAPI backend.
- `DATA_DIR`: Directory for CSV backups of survey results.

## 📝 License
This project was developed as part of a BCA Semester VI dissertation.
