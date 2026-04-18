# GitHub Token Setup Guide

## Quick Setup (5 minutes)

To enable the "Update Data" button in your dashboard, you need to create a GitHub Personal Access Token.

---

### **Step 1: Create Personal Access Token**

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Fill in the form:
   - **Note**: `FX Sheet Dashboard Token`
   - **Expiration**: Choose `No expiration` (or your preference)
4. Select scopes/permissions:
   - ✅ **repo** (Full control of private repositories)
   - This will automatically check all sub-items under `repo`
5. Click **"Generate token"** at the bottom
6. **IMPORTANT**: Copy the token immediately (starts with `ghp_...`)
   - You won't be able to see it again!

---

### **Step 2: Configure index.html**

1. Open `index.html` in a text editor
2. Find this section near line 883:

```javascript
const GITHUB_CONFIG = {
    owner: 'YOUR_GITHUB_USERNAME',  // ← Replace with your GitHub username
    repo: 'FX-Sheet',               // ← Replace with your repository name
    token: ''                        // ← Paste your token here
};
```

3. Replace the values:
   - `YOUR_GITHUB_USERNAME` → Your actual GitHub username (e.g., `'john-doe'`)
   - `repo` → Your repository name (likely `'FX-Sheet'`)
   - `token` → Paste the token you copied (e.g., `'ghp_abc123...'`)

**Example:**
```javascript
const GITHUB_CONFIG = {
    owner: 'john-doe',
    repo: 'FX-Sheet',
    token: 'ghp_1234567890abcdefghijklmnopqrstuvwxyz'
};
```

4. Save the file

---

### **Step 3: Test It!**

1. Open `index.html` in your browser (or visit your GitHub Pages URL)
2. Click the **"📊 Update Data"** button
3. You should see:
   - Button changes to "Updating..." with orange color
   - Status message shows progress
   - After 30-60 seconds, data refreshes automatically

---

## **How It Works**

```
You click "Update Data" button
        ↓
JavaScript calls GitHub API to trigger workflow
        ↓
GitHub Actions runs update_stocks.py
        ↓
Fetches fresh data from Yahoo Finance
        ↓
Commits updated stocks-data.json
        ↓
Dashboard reloads the new data
```

---

## **Security Notes**

⚠️ **Keep your token private!**
- Don't commit `index.html` with the token to a **public** repository
- If your repo is public, consider:
  - Using a local version with the token for personal use
  - Deploying to GitHub Pages from a **private** repository
  - Using environment variables (requires a backend)

✅ **Safe usage:**
- Private repository: ✅ Safe to include token
- Local file only: ✅ Safe
- Public repository: ❌ Don't commit the token

---

## **Troubleshooting**

### **Error: "Failed to trigger workflow: 401"**
- Your token is invalid or expired
- Generate a new token and update `index.html`

### **Error: "Failed to trigger workflow: 404"**
- Check your `owner` and `repo` values
- Make sure the repository name is correct (case-sensitive)

### **Error: "Failed to trigger workflow: 403"**
- Token doesn't have the right permissions
- Make sure you selected the `repo` scope when creating the token

### **Button shows "Setup Required" message**
- You haven't configured the token yet
- Follow Step 2 above

---

## **Alternative: Manual Update**

If you prefer not to use the token, you can always:
1. Go to your GitHub repository
2. Click **Actions** tab
3. Click **"Update FX Sheet Stock Data"** workflow
4. Click **"Run workflow"** → **"Run workflow"** button
5. Wait for it to complete (~1-2 minutes)
6. Refresh your dashboard

---

## **Need Help?**

Common issues:
- **Token not working?** → Regenerate with `repo` scope
- **Workflow not running?** → Check `.github/workflows/update-stocks.yml` exists
- **Data not updating?** → Check GitHub Actions logs for errors

---

**That's it! You now have on-demand stock data updates with one click! 🎉**
