# 🚀 Complete Deployment Guide

## Backend Deployment on Railway.app

### 📋 Railway Deployment Settings

When deploying to Railway, use these exact settings:

#### **1. Repository Settings**
- **Root Directory**: `backend`
- **Branch**: `main` (or your default branch)

#### **2. Build Settings**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`
- **Runtime**: Python 3.11

#### **3. Environment Variables** (Required)
```bash
SECRET_KEY=your-super-secret-key-change-this-in-production
SECURITY_PASSWORD_SALT=your-security-salt-change-this-too
FRONTEND_URL=https://your-netlify-app.netlify.app
FLASK_ENV=production
```

#### **4. Optional Environment Variables**
```bash
# If using Redis (Railway Redis addon)
REDIS_URL=redis://default:password@host:port

# If using PostgreSQL (Railway PostgreSQL addon)
DATABASE_URL=postgresql://user:password@host:port/dbname
```

### 🔧 Railway Configuration Files

The following files are automatically configured for Railway:

1. **`railway.json`** - Railway deployment configuration
2. **`Procfile`** - Process definitions (web, worker, beat)
3. **`nixpacks.toml`** - Build configuration
4. **`requirements.txt`** - Python dependencies
5. **`runtime.txt`** - Python version

### 📝 Step-by-Step Railway Deployment

1. **Connect Repository**
   - Go to [Railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository

2. **Configure Settings**
   - Set **Root Directory** to `backend`
   - Railway will auto-detect Python and use our configuration files

3. **Set Environment Variables**
   - Go to your project → Variables tab
   - Add the required environment variables listed above

4. **Deploy**
   - Railway will automatically build and deploy
   - You'll get a URL like: `https://your-app.railway.app`

### 🔍 Health Check

Your backend includes a health check endpoint:
```
GET https://your-app.railway.app/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00.000Z",
  "environment": "production"
}
```

---

## Frontend Deployment on Netlify

### 📋 Netlify Deployment Settings

#### **1. Build Settings**
- **Base Directory**: `frontend`
- **Build Command**: `npm run build`
- **Publish Directory**: `dist`
- **Node Version**: 18

#### **2. Environment Variables** (Required)
```bash
VITE_API_URL=https://your-railway-app.railway.app
```

### 📝 Step-by-Step Netlify Deployment

1. **Connect Repository**
   - Go to [Netlify.com](https://netlify.com)
   - Click "New site from Git"
   - Connect your GitHub repository

2. **Configure Build Settings**
   - **Base directory**: `frontend`
   - **Build command**: `npm run build`
   - **Publish directory**: `dist`

3. **Set Environment Variables**
   - Go to Site settings → Environment variables
   - Add: `VITE_API_URL` = `https://your-railway-app.railway.app`

4. **Deploy**
   - Netlify will automatically build and deploy
   - You'll get a URL like: `https://your-app.netlify.app`

---

## 🔄 Post-Deployment Configuration

### 1. Update Backend CORS
After getting your Netlify URL, update the Railway environment variable:
```bash
FRONTEND_URL=https://your-actual-netlify-app.netlify.app
```

### 2. Update Frontend API URL
After getting your Railway URL, update the Netlify environment variable:
```bash
VITE_API_URL=https://your-actual-railway-app.railway.app
```

### 3. Test the Connection
1. Visit your Netlify frontend URL
2. Try logging in with: `admin@parking.com` / `admin`
3. Check if data loads properly

---

## 🛠️ Troubleshooting

### Common Issues:

#### **CORS Errors**
- Ensure `FRONTEND_URL` is set correctly in Railway
- Check that your Netlify URL is exact (no trailing slash)

#### **API Connection Failed**
- Verify `VITE_API_URL` in Netlify environment variables
- Check Railway app is running: visit `/health` endpoint

#### **Database Issues**
- Railway automatically provides SQLite
- For PostgreSQL: add Railway PostgreSQL addon

#### **Build Failures**
- Check build logs in Railway/Netlify dashboards
- Ensure all environment variables are set

### **Railway Specific:**
- Check logs: Railway Dashboard → Deployments → View Logs
- Restart service: Railway Dashboard → Settings → Restart

### **Netlify Specific:**
- Check build logs: Netlify Dashboard → Deploys → Build Log
- Clear cache: Netlify Dashboard → Deploys → Clear Cache

---

## 🎯 Production Checklist

### Before Going Live:

- [ ] Change `SECRET_KEY` to a strong, unique value
- [ ] Change `SECURITY_PASSWORD_SALT` to a unique value
- [ ] Set correct `FRONTEND_URL` in Railway
- [ ] Set correct `VITE_API_URL` in Netlify
- [ ] Test admin login: `admin@parking.com` / `admin`
- [ ] Test user registration and booking flow
- [ ] Verify CORS is working (no console errors)
- [ ] Check health endpoint: `/health`
- [ ] Test on mobile devices

### Optional Enhancements:

- [ ] Add Railway Redis addon for caching
- [ ] Add Railway PostgreSQL addon for production database
- [ ] Set up custom domain names
- [ ] Configure SSL certificates (automatic on both platforms)
- [ ] Set up monitoring and alerts

---

## 📞 Support

If you encounter issues:

1. **Check the logs** in Railway/Netlify dashboards
2. **Verify environment variables** are set correctly
3. **Test the health endpoint** to ensure backend is running
4. **Check CORS configuration** if frontend can't connect to backend

Your parking system should now be fully deployed and accessible worldwide! 🌍