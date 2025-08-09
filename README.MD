# 🎿 **SlopeVision**

> *All the ski resort webcams you need, in one app. Real-time views. Historical data. Fresh powder, found.*

[![Vue.js](https://img.shields.io/badge/Vue.js-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white)](https://vuejs.org/)
[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

---

## 📖 **Table of Contents**
- [Overview](#-overview)
- [Live Demo](#-live-demo)
- [Features](#-features)
- [Tech Stack](#️-tech-stack)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Development](#-development)
- [Deployment](#-deployment)
- [API Documentation](#-api-documentation)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🏔️ **Overview**

SlopeVision is a comprehensive ski resort webcam aggregation platform that provides real-time and historical webcam feeds from ski resorts worldwide. The application combines a Vue.js frontend with a Django REST API backend, complemented by a Node.js data service for automated webcam data collection.

### **Why SlopeVision?**
- **Centralized Access**: No more jumping between multiple resort websites
- **Historical Data**: Track snow conditions over time with archived webcam feeds
- **Interactive Maps**: Discover new ski resorts and webcams through an intuitive map interface
- **User Management**: Create accounts, save favorite places, and customize your experience
- **Real-time Updates**: Automated data collection ensures fresh content

---

## 🌐 **Live Demo**

🚀 **Try SlopeVision now**: [https://slopevision-608659285974.us-east1.run.app/](https://slopevision-608659285974.us-east1.run.app/) (Note: The live demo may take a moment to start.)

Experience the full functionality of SlopeVision with the live deployment. Browse webcams from ski resorts worldwide, explore the interactive map, and see real-time snow conditions!

---

## 🌟 **Features**

### 📹 **Webcam Management**
- **Multi-source Aggregation**: Automatically collects webcam feeds from various ski resort websites
- **Real-time Updates**: Continuous monitoring and updating of webcam status
- **Historical Archives**: Browse past webcam captures to track snow conditions
- **Video Support**: Both static images and live video streams

### 🗺️ **Interactive Experience**
- **Interactive Map**: Leaflet-powered map showing webcam locations worldwide
- **Search & Filter**: Find webcams by location, country, or resort name
- **Place Details**: Comprehensive information about each ski resort
- **Responsive Design**: Optimized for desktop and mobile devices

### 👤 **User Features**
- **Account Management**: User registration, login, and profile management
- **Favorites System**: Save and organize your favorite ski resorts
- **Premium Accounts**: Advanced features for premium users
- **Dark Mode**: Toggle between light and dark themes

### 🔧 **Administrative Tools**
- **Data Management**: Django admin interface for content management
- **Automated Collection**: Scheduled tasks for webcam data harvesting
- **API Endpoints**: RESTful API for data access and manipulation


---

## 🛠️ **Tech Stack**

### **Frontend** (`vue-frontend/`)
- **Framework**: Vue.js 3 with Composition API
- **Build Tool**: Vite for fast development and building
- **Styling**: TailwindCSS for utility-first CSS
- **State Management**: Vuex for application state
- **Routing**: Vue Router for SPA navigation
- **Maps**: Leaflet for interactive mapping
- **Icons**: Heroicons for consistent iconography
- **HTTP Client**: Axios for API communication

### **Backend** (`slopevision_django/`)
- **Framework**: Django 4.2 with Django REST Framework
- **Database**: PostgreSQL (production) / SQLite (development)
- **Authentication**: Django Allauth + dj-rest-auth
- **API Documentation**: drf-spectacular (OpenAPI/Swagger)
- **Media Storage**: Google Cloud Storage integration
- **Task Scheduling**: Django-cron for automated tasks
- **Image Processing**: Pillow for image manipulation

### **Data Service** (`data-service/`)
- **Runtime**: Node.js with TypeScript
- **Framework**: Hono for lightweight HTTP server
- **Database**: Drizzle ORM with PostgreSQL
- **Web Scraping**: Playwright and Puppeteer
- **Cloud Storage**: Google Cloud Storage SDK
- **HTTP Client**: Axios for external API calls

### **DevOps & Deployment**
- **Containerization**: Docker & Docker Compose
- **Orchestration**: Ansible for server provisioning
- **Web Server**: Nginx for reverse proxy
- **Process Management**: Gunicorn for Django, systemd services
- **Cloud Platform**: Google Cloud Platform ready

---

## 📁 **Project Structure**

```
slopevision/
├── 📁 vue-frontend/           # Vue.js frontend application
│   ├── src/
│   │   ├── components/        # Reusable Vue components
│   │   ├── views/            # Page-level components
│   │   ├── router/           # Vue Router configuration
│   │   ├── store/            # Vuex store modules
│   │   ├── services/         # API service layers
│   │   └── assets/           # Static assets
│   ├── public/               # Public static files
│   └── package.json          # Frontend dependencies
│
├── 📁 slopevision_django/     # Django REST API backend
│   ├── rest_api/             # Main Django app
│   │   ├── models.py         # Database models
│   │   ├── views.py          # API endpoints
│   │   ├── serializers.py    # DRF serializers
│   │   ├── management/       # Custom Django commands
│   │   └── migrations/       # Database migrations
│   ├── slopevision_django/   # Django project settings
│   └── requirements.txt      # Python dependencies
│
├── 📁 data-service/           # Node.js data collection service
│   ├── src/
│   │   ├── tasks/            # Automated data collection tasks
│   │   ├── db/               # Database configuration
│   │   └── utils/            # Utility functions
│   └── package.json          # Node.js dependencies
│
├── 📁 deploy/                 # Deployment configurations
│   ├── playbook.yml          # Ansible deployment playbook
│   ├── inventory.py          # Server inventory
│   └── templates/            # Configuration templates
│
├── 📁 scripts/                # Utility scripts
│   ├── deploy.sh             # Deployment script
│   ├── server_init.sh        # Server initialization
│   └── *.sh                  # Various automation scripts
│
└── 📄 README.md              # This file
```

---

##  **Quick Start**

### **Prerequisites**
- Node.js 18+ and npm
- Python 3.9+
- PostgreSQL (for production)
- Docker & Docker Compose (optional)

### **1. Clone the Repository**
```bash
git clone https://github.com/tomc02/slopevision.git
cd slopevision
```

### **2. Environment Setup**

**Backend Environment:**
```bash
cd slopevision_django
cp env-pattern .env
# Edit .env with your configuration
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Frontend Environment:**
```bash
cd vue-frontend
cp env-pattern .env
npm install
```

**Data Service Environment:**
```bash
cd data-service
cp env-pattern .env
npm install
```

### **3. Database Setup**
```bash
cd slopevision_django
python manage.py migrate
python manage.py createsuperuser
```

### **4. Start Development Servers**

**Terminal 1 - Django Backend:**
```bash
cd slopevision_django
python manage.py runserver
```

**Terminal 2 - Vue Frontend:**
```bash
cd vue-frontend
npm run dev
```

**Terminal 3 - Data Service:**
```bash
cd data-service
npm run dev
```

### **5. Access the Application**
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/
- **Data Service**: http://localhost:8080

---

## 💻 **Development**

### **Frontend Development**
```bash
cd vue-frontend

# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run serve

# Linting
npm run lint
```

### **Backend Development**
```bash
cd slopevision_django

# Run development server
python manage.py runserver

# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run custom commands
python manage.py fetch_hzs_images
python manage.py save_history
```

### **Data Service Development**
```bash
cd data-service

# Development mode
npm run dev

# Manual data updates
curl http://localhost:8080/update/hzs
curl http://localhost:8080/update/scrape
curl http://localhost:8080/capture
```

### **Using Docker**
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## 🚀 **Deployment**

Will be available soon!

---

## 📚 **API Documentation**

### **Available Endpoints**

- **Base URL**: http://localhost:8000/api/

**Interactive API Documentation:**
- **Swagger UI**: http://localhost:8000/docs/
- **OpenAPI Schema**: http://localhost:8000/schema/

### **Data Service Endpoints**
- `GET /update/hzs` - Update HZS webcam data
- `GET /update/scrape` - Update scraped webcam data  
- `GET /capture` - Capture all webcam images

---

<div align="center">

**⭐ If you find SlopeVision useful, please consider giving it a star! ⭐**

Made with ❤️ for the skiing community

</div>