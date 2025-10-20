# Render.com Deployment Guide

## Overview
This guide provides step-by-step instructions to deploy the Wearable Biosignal Analysis Backend to Render.com.

## Prerequisites
1. A GitHub account with this repository
2. A Render.com account (free tier available)
3. Git repository pushed to GitHub

## Project Structure (Optimized for Render.com)
```
wearable-backend/
├── app/
│   ├── __init__.py              # Package initializer (NEW)
│   ├── main.py                  # FastAPI app (UPDATED imports)
│   ├── models/
│   ├── services/
│   └── utils/
├── requirements.txt             # Python dependencies (UPDATED)
├── runtime.txt                  # Python version
├── render.yaml                  # Render.com config (NEW)
├── build.sh                     # Build script (NEW)
└── RENDER_DEPLOYMENT.md         # This file
```

## Key Changes Made for Render.com

### 1. Fixed Import Structure
- Updated `app/main.py` to use absolute imports (`from app.models...`)
- Created `app/__init__.py` to make it a proper Python package

### 2. Dynamic Port Binding
- Modified main.py to use `PORT` environment variable from Render
- Falls back to 8000 for local development

### 3. Production Configuration
- Disabled auto-reload in production
- Added gunicorn as alternative production server
- Configured proper health check endpoint

## Deployment Options

### Option 1: Using render.yaml (Recommended - Infrastructure as Code)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Configure for Render.com deployment"
   git push origin main
   ```

2. **Create New Web Service on Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`
   - Click "Apply" to create the service

3. **Service will be created with:**
   - Name: wearable-biosignal-backend
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Health Check: `/api/v1/health`

### Option 2: Manual Web Service Setup

1. **Push your code to GitHub**

2. **Create New Web Service**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your repository

3. **Configure the Service**
   - **Name:** `wearable-biosignal-backend` (or your choice)
   - **Region:** Choose closest to your users (Oregon, Frankfurt, Singapore, Ohio)
   - **Branch:** `main`
   - **Root Directory:** Leave empty (use root)
   - **Runtime:** `Python 3`
   - **Build Command:**
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command:**
     ```bash
     uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```

4. **Environment Variables** (Optional but recommended)
   Add these in the "Environment" section:
   - `PYTHON_VERSION` = `3.10.12`
   - `ENVIRONMENT` = `production`
   - `LOG_LEVEL` = `info`

5. **Advanced Settings**
   - **Health Check Path:** `/api/v1/health`
   - **Auto-Deploy:** `Yes` (deploys automatically on git push)

6. **Click "Create Web Service"**

## Verification Steps

### 1. Monitor Deployment
- Watch the build logs in Render dashboard
- Deployment typically takes 2-5 minutes

### 2. Check Service Status
Once deployed, your service will be available at:
```
https://wearable-biosignal-backend.onrender.com
```
(Replace with your actual service name)

### 3. Test Endpoints

#### Health Check
```bash
curl https://your-service.onrender.com/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00",
  "services": {
    "ble_simulator": true,
    "timesystems": true,
    "ifrs": true,
    "clarity": true,
    "lia": true
  },
  "connected_clients": 0,
  "active_sessions": 0
}
```

#### Root Endpoint
```bash
curl https://your-service.onrender.com/
```

#### API Documentation
Visit in browser:
- Swagger UI: `https://your-service.onrender.com/docs`
- ReDoc: `https://your-service.onrender.com/redoc`

## Common Issues and Solutions

### Issue 1: Import Errors
**Error:** `ModuleNotFoundError: No module named 'models'`

**Solution:**
- Ensure `app/__init__.py` exists
- Verify imports in main.py use `from app.models...` format
- Check start command is `uvicorn app.main:app` (not `main:app`)

### Issue 2: Port Binding Error
**Error:** `Address already in use` or port binding issues

**Solution:**
- Start command MUST use `--port $PORT`
- Render provides PORT environment variable dynamically
- Code reads: `port = int(os.environ.get("PORT", 8000))`

### Issue 3: Build Failures
**Error:** Dependency installation fails

**Solution:**
- Check `requirements.txt` is in root directory
- Verify Python version in `runtime.txt` matches requirements
- Check build logs for specific package errors

### Issue 4: Application Won't Start
**Error:** Service shows as "Deploying" indefinitely

**Solution:**
- Check start command syntax: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Verify health check endpoint `/api/v1/health` is accessible
- Review application logs in Render dashboard

### Issue 5: Free Tier Sleep
**Note:** Render free tier services sleep after 15 minutes of inactivity

**Solution:**
- First request after sleep will take 30-60 seconds (cold start)
- Consider upgrading to paid tier for always-on service
- Or use external service to ping periodically (be mindful of terms)

## Performance Optimization

### 1. Worker Configuration
For better performance on paid plans, you can use Gunicorn with multiple workers:

Update start command to:
```bash
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

### 2. Health Check Optimization
The health check endpoint is lightweight and responds quickly:
- Path: `/api/v1/health`
- Interval: 30 seconds (Render default)

### 3. CORS Configuration
Currently set to allow all origins. For production, update in `app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend.com",
        "https://your-mobile-app.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Environment Variables

### Required
- `PORT` - Automatically provided by Render

### Optional (Set in Render Dashboard)
- `PYTHON_VERSION` - Python version (default: 3.10.12)
- `ENVIRONMENT` - Deployment environment (default: production)
- `LOG_LEVEL` - Logging level (default: info)

### Adding Custom Variables
If you need to add API keys or secrets:
1. Go to your service in Render Dashboard
2. Navigate to "Environment" tab
3. Click "Add Environment Variable"
4. Add key-value pairs
5. Click "Save Changes" (triggers redeployment)

## Monitoring and Logs

### View Logs
1. Go to your service in Render Dashboard
2. Click "Logs" tab
3. View real-time application logs

### Key Log Patterns
```
✓ BLE Simulator started
✓ Timesystems™ layer initialized
✓ iFRS™ layer initialized
✓ Clarity™ layer initialized
✓ LIA Engine initialized
Backend ready to accept connections
```

## Scaling

### Free Tier Limitations
- 750 hours/month of runtime
- Services spin down after 15 min of inactivity
- Shared CPU and 512 MB RAM

### Upgrade Options
- **Starter:** $7/month - Always on, 0.5 GB RAM
- **Standard:** $25/month - 2 GB RAM, better performance
- **Pro:** $85/month - 4 GB RAM, priority support

## Local Testing Before Deployment

### Test the production configuration locally:

```bash
# Set PORT environment variable
export PORT=8000

# Run with production settings
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Test from project root:
```bash
cd /path/to/wearable-backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Verify imports work:
```bash
python -c "from app.main import app; print('✓ Imports working')"
```

## Continuous Deployment

### Automatic Deployment
Once configured, every push to your main branch triggers:
1. Automatic build on Render
2. Run build command
3. Deploy new version
4. Health check verification

### Manual Deployment
You can also manually deploy:
1. Go to service in Render Dashboard
2. Click "Manual Deploy" → "Deploy latest commit"

## Database Integration (Future)

If you add a database:

1. **Create Database Service**
   - Add to `render.yaml` or create in dashboard
   - Render provides PostgreSQL, Redis

2. **Update Code**
   - Add database connection in `app/main.py`
   - Store connection string in environment variables

3. **Example render.yaml addition:**
```yaml
databases:
  - name: wearable-db
    databaseName: biosignals
    user: biosignals_user
```

## Mobile App Integration

### Update your mobile app API endpoint:
```typescript
// React Native
const API_BASE_URL = 'https://your-service.onrender.com';
const WS_URL = 'wss://your-service.onrender.com/ws/stream';
```

### Test CORS:
Make a test request from your mobile app to ensure CORS is properly configured.

## Security Best Practices

1. **Environment Variables**
   - Never commit secrets to git
   - Use Render's environment variables for sensitive data

2. **CORS Configuration**
   - Restrict origins in production
   - Update `allow_origins` in main.py

3. **API Authentication** (Recommended for production)
   - Add API key authentication
   - Implement rate limiting
   - Use HTTPS only (Render provides this automatically)

4. **Health Monitoring**
   - Set up alerts in Render dashboard
   - Monitor error rates and response times

## Cost Estimation

### Free Tier (Recommended for Testing)
- Cost: $0/month
- Limitations: Sleep after 15 min inactivity
- Best for: Development, testing, demos

### Starter Plan (Recommended for Production)
- Cost: $7/month
- Always on, better performance
- Best for: Small production deployments

### Standard Plan
- Cost: $25/month
- More resources, better reliability
- Best for: Production with moderate traffic

## Support and Troubleshooting

### Render Support
- Documentation: https://render.com/docs
- Community: https://community.render.com
- Status Page: https://status.render.com

### Application Logs
Check application logs for detailed error messages:
1. Render Dashboard → Your Service → Logs
2. Look for Python stack traces
3. Check startup sequence completion

### Debug Mode
For troubleshooting, temporarily add to environment variables:
```
LOG_LEVEL=debug
```

## Next Steps After Deployment

1. ✅ Test all API endpoints
2. ✅ Verify WebSocket connections
3. ✅ Update mobile app with production URL
4. ✅ Set up monitoring and alerts
5. ✅ Configure custom domain (optional)
6. ✅ Implement authentication (recommended)
7. ✅ Set up CI/CD pipeline (optional)

## Custom Domain (Optional)

To use your own domain:

1. **In Render Dashboard:**
   - Go to your service → Settings
   - Click "Add Custom Domain"
   - Enter your domain (e.g., api.yourdomain.com)

2. **In Your DNS Provider:**
   - Add CNAME record pointing to Render's domain
   - Wait for DNS propagation (up to 48 hours)

3. **SSL Certificate:**
   - Render automatically provides free SSL via Let's Encrypt

## Conclusion

Your Wearable Biosignal Analysis Backend is now configured for deployment on Render.com!

The project structure has been optimized with:
- ✅ Proper Python package structure
- ✅ Absolute imports for reliability
- ✅ Dynamic port binding
- ✅ Production-ready configuration
- ✅ Comprehensive deployment files

**Quick Deploy Command:**
```bash
git add .
git commit -m "Ready for Render.com deployment"
git push origin main
```

Then follow Option 1 or Option 2 above to create your Render service.

---

**Need Help?**
- Check the troubleshooting section above
- Review Render logs in dashboard
- Verify all files are committed to git
- Ensure start command is exactly: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
