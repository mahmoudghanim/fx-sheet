# 🌐 Deploy FX Sheet Dashboard to Web Server

## Option 1: Shared Hosting (cPanel, Plesk, etc.)

### Requirements:
- ✅ Python 3.7+ support
- ✅ SSH access or File Manager
- ✅ Ability to run Python scripts

### Steps:

#### 1. Upload Files
Upload these files to your web server (public_html or www directory):
```
- index.html
- stocks-data.json
- server.py
- fetch_yahoo_data.py
```

#### 2. Configure Server
Most shared hosting uses Apache/Nginx. You have two options:

**Option A: Using .htaccess (Apache)**
Create `.htaccess` file:
```apache
RewriteEngine On
RewriteRule ^$ http://localhost:8001/ [P,L]
```

**Option B: Using Passenger (cPanel Python App)**
1. Go to "Setup Python App" in cPanel
2. Create new app:
   - Python version: 3.7+
   - Application root: /home/user/fx-sheet
   - Application URL: yourdomain.com/fx-sheet
   - Startup file: server.py
3. Install requirements (if any)

#### 3. Update Data on Server
SSH into your server and run:
```bash
cd /path/to/fx-sheet
python fetch_yahoo_data.py
```

#### 4. Automate Data Updates
Set up a cron job to update data daily:
```bash
# Edit crontab
crontab -e

# Add this line (updates at 6 AM daily)
0 6 * * * /usr/bin/python3 /path/to/fx-sheet/fetch_yahoo_data.py >> /path/to/fx-sheet/update.log 2>&1
```

---

## Option 2: PythonAnywhere (Free/Paid)

### Steps:
1. Sign up at https://www.pythonanywhere.com
2. Upload files via Files tab
3. Go to Web tab → Add a new web app
4. Choose "Manual configuration" → Python 3.10
5. Edit WSGI configuration file:

```python
import sys
path = '/home/yourusername/fx-sheet'
if path not in sys.path:
    sys.path.append(path)

# Simple static file serving
from django.conf import settings
from django.core.wsgi import get_wsgi_application

# Or use Flask/bottle for serving
```

**Easier method**: Use Flask
Create `flask_app.py`:
```python
from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    app.run()
```

---

## Option 3: VPS (DigitalOcean, AWS, Linode)

### Full Control Deployment:

#### 1. Install Dependencies
```bash
sudo apt update
sudo apt install python3 python3-pip nginx
```

#### 2. Upload Files
```bash
scp -r "FX Sheet" user@your-server:/var/www/fx-sheet
```

#### 3. Set Up Gunicorn (Production Server)
```bash
cd /var/www/fx-sheet
pip3 install gunicorn
```

Create `wsgi.py`:
```python
from server import Handler
import socketserver

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

def app(environ, start_response):
    # Simple WSGI app
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [open('index.html', 'rb').read()]
```

Run with Gunicorn:
```bash
gunicorn --bind 0.0.0.0:8000 wsgi:app
```

#### 4. Configure Nginx
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /var/www/fx-sheet;
    }
}
```

#### 5. Set Up Systemd Service
Create `/etc/systemd/system/fx-sheet.service`:
```ini
[Unit]
Description=FX Sheet Dashboard
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/fx-sheet
ExecStart=/usr/bin/gunicorn --bind 0.0.0.0:8000 wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Start the service:
```bash
sudo systemctl start fx-sheet
sudo systemctl enable fx-sheet
```

---

## Option 4: GitHub Pages (Static Only - No Server Needed)

**Best for**: Simple hosting without Python

### Steps:
1. Create a GitHub repository
2. Upload only these files:
   - `index.html`
   - `stocks-data.json`
3. Go to Settings → Pages
4. Select branch: main, folder: /root
5. Your site will be at: `https://username.github.io/fx-sheet/`

**Limitation**: You'll need to manually update `stocks-data.json` and push to GitHub

---

## Option 5: Docker (Any Server)

### Create Dockerfile:
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . /app

EXPOSE 8001

CMD ["python", "server.py"]
```

### Build and Run:
```bash
docker build -t fx-sheet .
docker run -d -p 8001:8001 --name fx-sheet-dashboard fx-sheet
```

### Docker Compose:
Create `docker-compose.yml`:
```yaml
version: '3'
services:
  fx-sheet:
    build: .
    ports:
      - "8001:8001"
    volumes:
      - ./stocks-data.json:/app/stocks-data.json
    restart: unless-stopped
```

Run:
```bash
docker-compose up -d
```

---

## Important: Static vs Dynamic Hosting

### If Your Server Doesn't Support Python:
You can still host it as a **static site**:

1. Upload only:
   - `index.html`
   - `stocks-data.json`

2. The dashboard will work perfectly!
3. Update data locally and re-upload `stocks-data.json`

**Works on**:
- ✅ GitHub Pages
- ✅ Netlify
- ✅ Vercel
- ✅ Any static hosting
- ✅ Shared hosting (HTML only)

---

## Security Considerations

1. **Don't expose server.py** if using static hosting
2. **Update data regularly** (set up automation)
3. **Use HTTPS** for production (Let's Encrypt is free)
4. **Rate limiting** if publicly accessible
5. **Backup stocks-data.json** regularly

---

## Recommended Solutions by Use Case:

| Use Case | Best Option | Cost |
|----------|-------------|------|
| Personal use | GitHub Pages | Free |
| Small team | PythonAnywhere | Free-$5/mo |
| Business | VPS + Nginx | $5-20/mo |
| Enterprise | Docker + Cloud | $20+/mo |
| Quick test | Static hosting | Free |

---

## Quick Deploy to Static Hosting (Easiest)

**Netlify (Drag & Drop)**:
1. Go to https://app.netlify.com/drop
2. Drag your folder containing `index.html` and `stocks-data.json`
3. Done! You get a live URL instantly

**Vercel**:
1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel`
3. Follow prompts

---

Need help with a specific hosting platform? Let me know which one!
