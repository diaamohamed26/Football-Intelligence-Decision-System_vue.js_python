# ⚽ FIDS — Football Intelligence Decision System

### AI-Powered Football Analytics & Decision Support Platform

FIDS (Football Intelligence Decision System) is an AI-powered football intelligence platform designed to transform football data into meaningful insights. It combines modern web technologies, football analytics, and AI-assisted analysis to support smarter decisions about matches, teams, and players.

The platform aims to bring football statistics, performance insights, tactical analysis, and AI-powered interaction together in one dashboard.

---

## 🚀 Project Overview

FIDS is designed to help football enthusiasts, analysts, scouts, and decision-makers explore football data and gain deeper insights through an intelligent analytics experience.

### Core Capabilities

- **Match Intelligence:** Explore match information and performance indicators.
- **AI Football Assistant:** Ask football-related questions and receive AI-generated insights.
- **Player Analytics:** Explore player performance and compare individual contributions.
- **Team Analysis:** Evaluate teams and compare their performance.
- **Competition Management:** Organize football competitions, teams, players, and matches.
- **Football News:** Access football news and updates.
- **User Management:** Authentication, user accounts, and role-based access.
- **Admin Dashboard:** Manage football data and platform resources.

*Note: Feature availability depends on the implementation and integration of each module.*

---

## 🧠 AI Integration

FIDS integrates with the Groq API to support AI-assisted football intelligence.

The AI layer is designed to support:
- Football-related questions and conversations.
- Match and team analysis.
- Player comparisons.
- Football insights based on available data.

**AI Provider:** Groq  
**Configurable Model:** `openai/gpt-oss-120b`

---

## 🛠️ Technology Stack

### Frontend
- Vue 3
- TypeScript
- Vite
- Tailwind CSS
- Vue Router
- Lucide Icons

### Backend
- Python
- Django
- Django REST Framework
- Django REST Framework Simple JWT
- SQLite (development database)

### AI
- Groq API
- Environment-based AI configuration

### Development Tools
- Git & GitHub
- VS Code
- REST API architecture

---

## 📁 Project Structure

```text
FIDS/
│
├── backend/
│   ├── config/
│   ├── accounts/
│   ├── football/
│   ├── intelligence/
│   ├── favorites/
│   ├── football_news/
│   └── manage.py
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
│
├── photos/
├── .gitignore
└── README.md
```

---

## ⚙️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/diaamohamed26/Football-Intelligence-Decision-System_vue.js_python.git

cd Football-Intelligence-Decision-System_vue.js_python
```

### 2. Backend Setup

```bash
cd backend

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

Configure your environment variables before starting Django.

For macOS/Linux, you can export them in your terminal:

```bash
export DJANGO_SECRET_KEY="your-secret-key"
export DJANGO_DEBUG="True"
export DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1"
export GROQ_API_KEY="your-groq-api-key"
export GROQ_MODEL="openai/gpt-oss-120b"
```

Run database migrations:

```bash
python manage.py migrate
```

Start the backend:

```bash
python manage.py runserver
```

Backend development URL:

```text
http://127.0.0.1:8000/
```

API base URL:

```text
http://127.0.0.1:8000/api/v1/
```

### 3. Frontend Setup

Open another terminal:

```bash
cd frontend

npm install

npm run dev
```

Frontend development URL:

```text
http://localhost:5173/
```

---

## 🔐 Environment Variables

| Variable | Description |
|---|---|
| `DJANGO_SECRET_KEY` | Django secret key |
| `DJANGO_DEBUG` | Debug mode |
| `DJANGO_ALLOWED_HOSTS` | Allowed backend hosts |
| `GROQ_API_KEY` | Groq API key |
| `GROQ_MODEL` | AI model identifier |

**Security:** Never commit API keys, `.env` files, database files, or production secrets to GitHub.

---

## 🔌 API Architecture

The frontend communicates with the Django backend through REST APIs.

```text
Vue 3 Frontend
      |
      | HTTP / REST API
      |
Django REST Framework
      |
      ├── Accounts
      ├── Football
      ├── Intelligence
      ├── Favorites
      └── Football News
             |
             └── Groq AI Integration
```

Authentication is implemented using JSON Web Tokens (JWT).

---

## 🎯 Project Goals

FIDS aims to evolve into a comprehensive football intelligence system that combines:

- Data-driven football analysis.
- AI-assisted decision support.
- Player scouting and performance insights.
- Match intelligence and tactical evaluation.
- Modern and scalable web architecture.

---

## 🔮 Future Development

- Advanced match prediction models.
- Real-time match data integration.
- Advanced player scouting and ranking.
- Tactical visualization and analysis.
- Historical performance analytics.
- More advanced AI-powered recommendations.
- Production deployment and scalable infrastructure.

---

## 👨‍💻 Developer

**Diaa Mohamed Abdelazize**

Full-Stack Developer | AI & Software Engineer

- GitHub: https://github.com/diaamohamed26
- LinkedIn: https://linkedin.com/in/diaa-mohamed-a50460125

---

## 📄 License

This project is currently maintained as a development project. A license can be added when its distribution terms are decided.

---

**FIDS — Turning Football Data into Intelligence.**
