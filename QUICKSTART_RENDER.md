# Quick Start - Deploy to Render.com in 5 Minutes

## Prerequisites
- Git repository on GitHub
- Free Render.com account

## Step 1: Push to GitHub

```bash
git add .
git commit -m "Configure for Render.com deployment"
git push origin main
```

## Step 2: Deploy on Render

### Option A: Using Blueprint (Fastest - Automated)

1. Go to https://dashboard.render.com/
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Render will detect `render.yaml` automatically
5. Click **"Apply"**
6. Wait 2-5 minutes for deployment

### Option B: Manual Setup

1. Go to https://dashboard.render.com/
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name:** `wearable-biosignal-backend`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Click **"Create Web Service"**

## Step 3: Verify Deployment

Once deployed, test your endpoints:

```bash
# Replace YOUR-SERVICE-URL with your actual Render URL
curl https://YOUR-SERVICE-URL.onrender.com/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "services": {
    "ble_simulator": true,
    "timesystems": true,
    "ifrs": true,
    "clarity": true,
    "lia": true
  }
}
```

## Step 4: Test API Documentation

Visit in your browser:
- **Swagger UI:** `https://YOUR-SERVICE-URL.onrender.com/docs`
- **ReDoc:** `https://YOUR-SERVICE-URL.onrender.com/redoc`

## That's It!

Your FastAPI backend is now live and ready to receive connections from your mobile app.

## Update Your Mobile App

Update your API endpoint in your mobile app:

```typescript
const API_BASE_URL = 'https://YOUR-SERVICE-URL.onrender.com';
```

## Common Issues

### Port already in use (Local testing)
Use a different port:
```bash
export PORT=8001
python3 -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Import errors
Make sure you're running from the project root:
```bash
cd /path/to/wearable-backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Need More Details?

See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for comprehensive deployment guide with troubleshooting.
