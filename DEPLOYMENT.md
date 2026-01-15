# 🚀 VIT-ChainVote Deployment Guide for Render

Complete step-by-step guide to deploy VIT-ChainVote on Render with backend API and static frontend.

---

## 📋 Prerequisites

Before starting, ensure you have:
- ✅ GitHub account
- ✅ Render account (free tier works perfectly)
- ✅ Google Gemini API key ([Get it here](https://makersuite.google.com/app/apikey))
- ✅ SMTP credentials (already provided in code)

---

## 🎯 Deployment Strategy

We'll deploy in **TWO parts**:
1. **Backend API** → Render Web Service (Python)
2. **Frontend** → Render Static Site (HTML/CSS/JS)

---

## PART 1: Push Code to GitHub

### Step 1: Initialize Git Repository

Open terminal in your project folder:

```bash
cd "c:\PROGRAMMING\CWH\New folder"
git init
```

### Step 2: Create .gitignore

Create a file named `.gitignore` with this content:

```
# Environment variables
.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

### Step 3: Add and Commit Files

```bash
git add .
git commit -m "Initial commit: VIT-ChainVote blockchain voting system"
```

### Step 4: Create GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click **"New Repository"** (green button)
3. Repository name: `vit-chainvote`
4. Description: `Secure blockchain voting system for VIT institute`
5. Keep it **Public** (required for free Render deployment)
6. **DO NOT** initialize with README (we already have files)
7. Click **"Create Repository"**

### Step 5: Push to GitHub

Copy the commands from GitHub (they'll look like this):

```bash
git remote add origin https://github.com/YOUR-USERNAME/vit-chainvote.git
git branch -M main
git push -u origin main
```

✅ **Checkpoint**: Your code is now on GitHub!

---

## PART 2: Deploy Backend API on Render

### Step 1: Create Web Service

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Click **"Connect a repository"**
4. If first time: Click **"Configure account"** → Select your GitHub account → **"Install"**
5. Find and select your `vit-chainvote` repository

### Step 2: Configure Web Service

Fill in these settings:

| Field | Value |
|-------|-------|
| **Name** | `vit-chainvote-api` |
| **Region** | Choose closest to you (e.g., Singapore) |
| **Branch** | `main` |
| **Root Directory** | Leave empty |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python backend/app.py` |
| **Instance Type** | `Free` |

### Step 3: Add Environment Variables

Scroll down to **"Environment Variables"** and click **"Add Environment Variable"**. Add these **ONE BY ONE**:

| Key | Value |
|-----|-------|
| `API_KEY` | Your Gemini API key (paste it here) |
| `EMAIL_USER` | `otakuaniverseofficial@gmail.com` |
| `EMAIL_PASS` | `adxpxirxgwnrcjlo` |
| `FLASK_ENV` | `production` |
| `PORT` | `5000` |

> ⚠️ **IMPORTANT**: Click **"Add"** after each variable!

### Step 4: Deploy Backend

1. Click **"Create Web Service"** (bottom of page)
2. Wait 2-3 minutes for deployment
3. You'll see logs scrolling - wait for: `🗳️ VIT-ChainVote Server Starting...`
4. Status will change to **"Live"** with a green dot

### Step 5: Copy Backend URL

1. At the top of the page, you'll see your service URL
2. It looks like: `https://vit-chainvote-api.onrender.com`
3. **COPY THIS URL** - you'll need it for the frontend!

✅ **Test Backend**: Visit `https://your-backend-url.onrender.com/api/election/state`
   - You should see JSON response with `"success": true`

---

## PART 3: Deploy Frontend on Render

### Step 1: Update Frontend Configuration

**BEFORE deploying frontend**, update the API URL:

1. Open `frontend/js/config.js`
2. Find this line:
   ```javascript
   : 'https://your-backend-url.onrender.com/api';
   ```
3. Replace `your-backend-url` with your actual backend URL
4. Example:
   ```javascript
   : 'https://vit-chainvote-api.onrender.com/api';
   ```

### Step 2: Commit and Push Changes

```bash
git add frontend/js/config.js
git commit -m "Update API URL for production"
git push
```

### Step 3: Create Static Site

1. Go back to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Static Site"**
3. Select your `vit-chainvote` repository

### Step 4: Configure Static Site

| Field | Value |
|-------|-------|
| **Name** | `vit-chainvote` |
| **Branch** | `main` |
| **Root Directory** | Leave empty |
| **Build Command** | Leave empty |
| **Publish Directory** | `frontend` |

### Step 5: Deploy Frontend

1. Click **"Create Static Site"**
2. Wait 1-2 minutes
3. Status will change to **"Live"**

### Step 6: Get Frontend URL

Your frontend will be live at:
```
https://vit-chainvote.onrender.com
```

✅ **Checkpoint**: Both backend and frontend are now live!

---

## PART 4: Testing Your Deployment

### Test 1: Landing Page
1. Visit your frontend URL
2. You should see the VIT-ChainVote landing page
3. Check that the election status badge shows "WAITING"

### Test 2: Admin Login
1. Click **"Shadow Admin"**
2. Enter: `shadow70956@gmail.com`
3. Click **"Enter"**
4. You should be redirected to admin dashboard

### Test 3: Register Candidate
1. In admin dashboard:
   - Name: `Test Candidate`
   - Department: `CSE`
2. Click **"Generate Manifesto & Register"**
3. Wait 5-10 seconds (AI is generating manifesto)
4. Candidate card should appear with AI-generated manifesto

### Test 4: Start Election
1. Click **"Start Election"**
2. Status should change to **"LIVE"** with red dot

### Test 5: Voter Flow (Optional - requires VIT email)
1. Open new incognito window
2. Visit your frontend URL
3. Click **"Cast Your Vote"**
4. Enter a VIT email (if you have one)
5. Check email for OTP
6. Complete voting process

---

## 🔧 Post-Deployment Configuration

### Update CORS (if needed)

If you deploy frontend on a different platform (Netlify, Vercel, etc.), add the domain to CORS:

1. Edit `backend/app.py`
2. Find the CORS section
3. Add your domain to the `origins` list
4. Commit and push - Render will auto-redeploy

### Monitor Logs

**Backend Logs:**
1. Go to Render Dashboard → `vit-chainvote-api`
2. Click **"Logs"** tab
3. Watch for errors or issues

**Frontend Logs:**
1. Open browser DevTools (F12)
2. Check Console for errors
3. Check Network tab for failed API calls

---

## 🎨 Custom Domain (Optional)

### For Backend:
1. In Render Dashboard → `vit-chainvote-api`
2. Go to **"Settings"** → **"Custom Domains"**
3. Add your domain (e.g., `api.yourdomain.com`)
4. Follow DNS instructions

### For Frontend:
1. In Render Dashboard → `vit-chainvote`
2. Go to **"Settings"** → **"Custom Domains"**
3. Add your domain (e.g., `vote.yourdomain.com`)
4. Update `config.js` with new API URL

---

## 🐛 Troubleshooting

### Issue: "API_KEY environment variable not set"
**Solution:** 
- Go to Render Dashboard → Service → Settings → Environment
- Verify `API_KEY` is set
- Click **"Manual Deploy"** → **"Deploy latest commit"**

### Issue: Frontend shows "Failed to fetch"
**Solution:**
- Check if backend is live (green dot)
- Verify API URL in `config.js` is correct
- Check browser console for CORS errors
- Ensure backend URL ends with `/api`

### Issue: OTP not sending
**Solution:**
- Verify `EMAIL_USER` and `EMAIL_PASS` in environment variables
- Check backend logs for SMTP errors
- Gmail may block "less secure apps" - use app password instead

### Issue: "Chain integrity compromised"
**Solution:**
- This is normal after deployment restarts
- Click **"Reset Ledger"** in admin dashboard
- Re-register candidates and restart election

### Issue: Slow first request
**Solution:**
- Render free tier "spins down" after inactivity
- First request takes 30-60 seconds to wake up
- Subsequent requests are fast
- Consider upgrading to paid tier for always-on service

---

## 📊 Render Free Tier Limits

| Resource | Limit |
|----------|-------|
| **Web Services** | 750 hours/month (enough for 1 service 24/7) |
| **Static Sites** | Unlimited |
| **Build Minutes** | 500/month |
| **Bandwidth** | 100 GB/month |
| **Sleep After** | 15 minutes of inactivity |

> 💡 **Tip**: Free tier sleeps after 15 min. First request wakes it up (takes ~30 sec).

---

## 🔄 Making Updates

### Update Code:
```bash
git add .
git commit -m "Your update message"
git push
```

Render will **automatically redeploy** both services!

### Update Environment Variables:
1. Render Dashboard → Service → Settings → Environment
2. Edit variable
3. Click **"Save Changes"**
4. Service will automatically restart

---

## 🎯 Quick Reference URLs

After deployment, bookmark these:

| Service | URL |
|---------|-----|
| **Frontend** | `https://vit-chainvote.onrender.com` |
| **Backend API** | `https://vit-chainvote-api.onrender.com` |
| **API Health** | `https://vit-chainvote-api.onrender.com/api/election/state` |
| **Render Dashboard** | `https://dashboard.render.com` |
| **GitHub Repo** | `https://github.com/YOUR-USERNAME/vit-chainvote` |

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Backend deployed on Render
- [ ] Environment variables set
- [ ] Backend health check passes
- [ ] Frontend API URL updated
- [ ] Frontend deployed on Render
- [ ] Admin login tested
- [ ] Candidate registration tested
- [ ] Election start/stop tested
- [ ] Blockchain integrity verified

---

## 🎉 Success!

Your VIT-ChainVote system is now **LIVE** and accessible worldwide!

**Share these URLs:**
- **Voters**: `https://vit-chainvote.onrender.com`
- **Admins**: `https://vit-chainvote.onrender.com` (login with Shadow email)

---

## 📞 Need Help?

If you encounter issues:
1. Check Render logs (Dashboard → Service → Logs)
2. Check browser console (F12 → Console)
3. Verify all environment variables are set
4. Ensure API URL in config.js is correct
5. Try manual redeploy (Dashboard → Service → Manual Deploy)

**Happy Voting! 🗳️⛓️**
