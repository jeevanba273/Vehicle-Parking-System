# Vehicle Parking System

A complete vehicle parking management system built with Vue.js frontend and Flask backend.

## 🚀 Features

- **User Authentication**: Login/Signup with role-based access
- **Admin Dashboard**: Manage parking lots, users, and analytics
- **User Dashboard**: Book parking spots and view booking history
- **Real-time Updates**: Live parking spot availability
- **Analytics**: Revenue tracking and occupancy metrics
- **Responsive Design**: Works on mobile, tablet, and desktop

## 🛠️ Tech Stack

### Frontend
- Vue.js 3 with TypeScript
- Bootstrap 5 for styling
- Pinia for state management
- Vue Router for navigation
- Chart.js for analytics

### Backend
- Flask with SQLAlchemy
- SQLite database
- Flask-Security for authentication
- Redis for caching (optional)
- Celery for background tasks

## 📁 Project Structure

```
├── frontend/          # Vue.js frontend application
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── netlify.toml   # Netlify deployment config
├── backend/           # Flask backend API
│   ├── app.py
│   ├── requirements.txt
│   ├── railway.json   # Railway deployment config
│   └── Procfile       # Process configuration
└── README.md
```

## 🚀 Deployment

### Frontend (Netlify)

1. **Connect Repository**: Link your GitHub repository to Netlify
2. **Build Settings**:
   - Build command: `npm run build`
   - Publish directory: `dist`
   - Base directory: `frontend`
3. **Environment Variables**:
   - `VITE_API_URL`: Your Railway backend URL (e.g., `https://your-app.railway.app`)
4. **Deploy**: Netlify will automatically deploy on every push

### Backend (Railway)

1. **Connect Repository**: Link your GitHub repository to Railway
2. **Root Directory**: Set to `backend`
3. **Environment Variables**:
   ```
   SECRET_KEY=your-secret-key-here
   SECURITY_PASSWORD_SALT=your-salt-here
   FRONTEND_URL=https://your-netlify-app.netlify.app
   ```
4. **Deploy**: Railway will automatically deploy using the `railway.json` config

## 🔧 Local Development

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## 📝 Environment Variables

### Frontend (.env.local)
```
VITE_API_URL=http://localhost:5000
```

### Backend (.env)
```
SECRET_KEY=your-secret-key
SECURITY_PASSWORD_SALT=your-salt
DATABASE_URL=sqlite:///parking_system.db
REDIS_URL=redis://localhost:6379/0
FRONTEND_URL=http://localhost:5173
```

## 🔐 Demo Credentials

- **Admin**: admin@parking.com / admin
- **User**: Register a new account

## 🎯 API Endpoints

- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/parking-lots` - Get all parking lots
- `POST /api/parking-lots` - Create parking lot (admin)
- `GET /api/parking-lots/{id}/spots` - Get parking spots
- `POST /api/bookings` - Create booking
- `GET /api/users/{id}/bookings` - Get user bookings
- `GET /api/analytics` - Get analytics data (admin)

## 📱 Features by Role

### Admin
- Manage parking lots (CRUD operations)
- View all registered users
- Analytics dashboard with charts
- Real-time parking grid visualization

### User
- Browse available parking lots
- Book parking spots interactively
- View booking history
- Release active bookings

## 🎨 Design Features

- Clean, minimalistic interface
- Smooth animations and transitions
- Glassmorphism effects
- Responsive grid layouts
- Interactive parking spot visualization
- Real-time data updates

## 🔄 Deployment URLs

After deployment, update these URLs:

1. **Frontend**: Update `VITE_API_URL` in Netlify environment variables
2. **Backend**: Update `FRONTEND_URL` in Railway environment variables
3. **CORS**: Backend automatically handles CORS for Netlify domains

## 📞 Support

For deployment issues:
- **Netlify**: Check build logs and environment variables
- **Railway**: Check deployment logs and database connectivity
- **CORS**: Ensure frontend URL is correctly set in backend environment