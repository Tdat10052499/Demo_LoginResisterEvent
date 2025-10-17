# Login Register Event Application

A full-stack application with Flutter mobile app, React web frontend, FastAPI backend, and Nginx API gateway.

## Project Structure

```
.
├── frontend/
│   ├── mobile/    # Flutter mobile app
│   └── web/       # React web app
├── backend/       # FastAPI backend
└── nginx/         # Nginx API Gateway configuration
```

## Requirements

- Node.js v24+ and npm
- Flutter 3.35+
- Python 3.8+
- Nginx

## Setup Instructions

### Backend (FastAPI)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate # Linux/MacOS
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the backend server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Web Frontend (React)

1. Navigate to the web frontend directory:
   ```bash
   cd frontend/web
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

### Mobile App (Flutter)

1. Navigate to the mobile app directory:
   ```bash
   cd frontend/mobile
   ```

2. Get Flutter dependencies:
   ```bash
   flutter pub get
   ```

3. Run the app:
   ```bash
   flutter run
   ```

### API Gateway (Nginx)

1. Install Nginx on your system
2. Copy the nginx.conf file to your Nginx configuration directory
3. Reload Nginx:
   ```bash
   nginx -s reload
   ```

## API Endpoints

- `/api/*` - Backend API endpoints
- `/` - Web frontend