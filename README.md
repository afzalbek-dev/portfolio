# Multilingual Developer Portfolio & Telegram Order Management System 🚀

A modern, production-grade, full-stack developer portfolio and client order management system supporting **3 Languages (Uzbek 🇺🇿, Russian 🇷🇺, English 🇬🇧)** with dark theme glassmorphism design, FastAPI backend, Aiogram 3.x Telegram bot integration, and web Admin Panel.

---

## 🌟 Key Features

- **🌐 Multilingual Support (UZ / RU / EN)**: Full UI localization using `react-i18next` with language persistence in `localStorage`. Multilingual database fields (`title_uz`, `title_ru`, `title_en`, etc.).
- **💎 Premium Design**: Sleek dark mode glassmorphism panels, glowing gradients (`#3B82F6` -> `#8B5CF6`), smooth Framer Motion reveal animations, responsive layout across all mobile, tablet, and desktop viewports.
- **⚡ Hero & About Me**: Interactive headlines, floating tech pills, stats cards, and live counters.
- **🛠 Services Showcase**: Interactive cards for Telegram Bots, Web Apps, Mini Apps, Backend/API, AI Solutions, and Automation. "Order" button pre-fills the order form automatically.
- **💼 Portfolio & Video Showcase**: Category tabs filter (Bots, Web, Mini Apps, AI Video, AI Image, Automation), detail modal viewer, live links, and 9:16 vertical video support.
- **📝 Advanced Order Form**: Multi-contact validator (Phone, Telegram, WhatsApp, Instagram, Email), budget options, rate limiting & hidden honeypot spam protection.
- **🤖 Aiogram 3.x Telegram Bot Integration**:
  - Instant Markdown order alerts sent to developer's Telegram.
  - Interactive inline action buttons to call, message Telegram, WhatsApp, or update order status (`Accepted`, `In Progress`, `Completed`, `Cancelled`).
  - Interactive Telegram Admin keyboards.
- **🔒 Web Admin Panel**: JWT-authenticated web dashboard to manage customer orders, publish new portfolio projects, and update site settings.
- **🐳 Docker Ready**: Pre-configured `docker-compose.yml` linking PostgreSQL, FastAPI, Aiogram Bot, and Vite Frontend.

---

## 📁 System Architecture

```
portfolio/
├── frontend/                     # React + Vite + TypeScript + Tailwind CSS + Framer Motion
│   ├── src/
│   │   ├── components/           # Navbar, Hero, About, Services, Portfolio, VideoShowcase, TechStack, OrderForm, ContactSection, FloatingCTA, Footer, AdminPanel, SuccessModal
│   │   ├── i18n/                 # react-i18next setup & translations (uz.json, ru.json, en.json)
│   │   ├── services/             # Axios API client
│   │   ├── types/                # TypeScript interfaces
│   │   ├── App.tsx
│   │   └── main.tsx
│   └── package.json
│
├── backend/                      # Python FastAPI REST API
│   ├── app/
│   │   ├── core/                 # Settings, Security (JWT & Password Hashing)
│   │   ├── models/               # SQLAlchemy models (User, Service, Project, Order, SiteSettings)
│   │   ├── schemas/              # Pydantic schemas
│   │   ├── api/                  # REST Routers (auth, services, projects, orders, settings)
│   │   ├── services/             # Telegram notification sender module
│   │   └── main.py               # FastAPI entry point
│   ├── seed.py                   # Automatic database seeder
│   └── requirements.txt
│
├── bot/                          # Aiogram 3.x Telegram Admin & Notification Bot
│   ├── handlers/                 # Message & Callback handlers
│   ├── keyboards/                # Reply & Inline keymaps
│   ├── config.py
│   └── main.py
│
├── docker-compose.yml            # Multi-container orchestration
├── .env.example                  # Environment configuration template
└── README.md
```

---

## 🚀 Quickstart Guide

### 1. Environment Setup

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Configure your Telegram credentials in `.env`:
```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ
TELEGRAM_ADMIN_ID=123456789
```

---

### 2. Local Development (Without Docker)

#### A. Run FastAPI Backend & Database Seeder

```bash
cd backend

# Create virtual environment (optional)
python -m venv venv
# On Windows: venv\Scripts\activate
# On Linux/macOS: source venv/bin/activate

pip install -r requirements.txt

# Seed database with initial admin user and multilingual projects/services
python seed.py

# Start FastAPI server
uvicorn app.main:app --reload --port 8000
```
- API Docs: `http://localhost:8000/docs`
- Default Admin Credentials: `admin` / `admin123`

#### B. Run Aiogram 3.x Telegram Bot

In a new terminal:

```bash
cd bot
pip install -r requirements.txt
python main.py
```

#### C. Run React Frontend

In a new terminal:

```bash
cd frontend
npm install
npm run dev
```
- Web Application: `http://localhost:5173`

---

### 3. Docker Deployment

To launch all services (Postgres, FastAPI Backend, Aiogram Bot, Frontend) using Docker Compose:

```bash
docker-compose up --build -d
```

---

## 🔒 Admin Panel Access

1. Open website in browser at `http://localhost:5173`
2. Click the **Shield Icon (Admin Panel)** in the top navigation bar.
3. Login with credentials:
   - **Username**: `admin`
   - **Password**: `admin123`
4. Manage incoming client orders, change status, or publish new portfolio projects directly!

---

## 🛡️ License & Copyright

© 2026 Developer Portfolio. All rights reserved.
