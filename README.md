# AutoWiper 🧹 - Koyeb Edition

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Pyrogram](https://img.shields.io/badge/Pyrogram-v2.0-red)](https://docs.pyrogram.org/)
[![Made with Python](https://img.shields.io/badge/Made%20with-Python-37766B.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Deploy on Koyeb](https://img.shields.io/badge/Deploy-Koyeb-00C7B7)](https://www.koyeb.com/)
[![Web App](https://img.shields.io/badge/Web%20App-Enabled-brightgreen)](https://github.com/PIROXTG/AutoWiper/tree/koyeb)
[![Always On](https://img.shields.io/badge/Always%20On-Auto%20Ping-orange)](https://github.com/PIROXTG/AutoWiper/tree/koyeb)

> **🌐 Web-enabled Telegram auto-cleaner bot** with comprehensive monitoring dashboard. Automatically deletes messages in groups and channels after a set time. Features **web dashboard, system monitoring, and auto-keep-alive** for cloud hosting platforms like Koyeb!

🔹 **Made by**: [PIROXTG](https://github.com/PIROXTG)  
🔹 **Session Generator**: [@SessionStringZBot](https://t.me/SessionStringZBot) (trusted & secure)  
🔹 **Support & Help**: [@piroxhelorobot](https://t.me/piroxhelorobot)  
🔹 **Main Repository**: [AutoWiper](https://github.com/PIROXTG/AutoWiper)  
🔹 **Branch**: `koyeb` (web app enabled)

## 🚨 IMPORTANT SECURITY NOTICE

> **⚠️ WARNING**: This bot uses your personal Telegram account session. Improper handling can lead to account compromise.

**NEVER**:
- Fork this repository publicly with your credentials
- Commit `config.py` with real values to any repository
- Share your session string or bot token with anyone

**ALWAYS**:
- ⭐ Star the original repository first
- Use GitHub's **Import repository** feature (not fork)
- Make your imported repository **PRIVATE**
- Use environment variables for deployment
- Keep your credentials secure and private

**DISCLAIMER**: The author is not responsible for any account compromise due to improper credential handling. Use at your own risk.

## ✨ Key Features (Koyeb Edition)

✅ **Auto-delete messages** in multiple Telegram groups or channels  
✅ **Per-chat timer control** — set different durations for each chat  
✅ **🌐 Web dashboard** — real-time monitoring via web interface  
✅ **📊 System monitoring** — comprehensive CPU, RAM, disk, and network stats  
✅ **🔄 Auto-ping system** — keeps cloud deployments alive 24/7  
✅ **📱 Mobile-friendly UI** — responsive web dashboard  
✅ **🩺 Health check API** — JSON endpoints for monitoring  
✅ **⚡ Lightning fast** — built with [Pyrogram](https://docs.pyrogram.org/) + [aiohttp](https://docs.aiohttp.org/)  
✅ **🤖 Userbot + Bot mode** — uses user session for full message control  
✅ **⏰ Scheduled cleanup** — APScheduler with enhanced monitoring  
✅ **📞 Remote management** — control via Telegram commands  
✅ **☁️ Cloud optimized** — perfect for Koyeb, Railway, Heroku  
✅ **🛡️ Production-grade** — graceful shutdown & comprehensive logging

---

## 🌐 Web Dashboard Features

### 📊 Live Monitoring Dashboard
- **Real-time system stats**: CPU, RAM, disk usage with visual indicators
- **Bot health status**: Connection status, uptime, active jobs
- **Network monitoring**: Data transfer, packet statistics
- **Performance metrics**: Load averages, process information
- **Mobile responsive**: Works perfectly on phones and tablets

### 🔗 API Endpoints
| Endpoint | Description | Response Type |
|----------|-------------|---------------|
| `/` | Main dashboard with bot overview | HTML |
| `/health` | Health check API for monitoring | JSON |
| `/stats` | Detailed system statistics | JSON |

### 🔄 Auto-Keep-Alive System
- **Auto-ping**: Pings web server every 2 minutes
- **Prevents sleeping**: Keeps free hosting platforms active
- **24/7 operation**: No more bot downtime on free tiers
- **Smart monitoring**: Logs ping status and connection health

---

## 📋 Commands Reference

### Bot Commands (Private Chat)
| Command | Description |
|---------|-------------|
| `/start` | Welcome message with web dashboard URL |
| `/ping` | Measure bot response latency |
| `/status` | Comprehensive uptime, jobs, and system stats |
| `/sysinfo` | Detailed system information and metrics |

### Userbot Commands (Owner Only)
| Command | Description |
|---------|-------------|
| `/delete` | Force immediate cleanup of old messages |
| `/update` | Pull latest code from GitHub and restart |
| `/restart` | Restart the bot service |
| `/chats` | List all monitored chats and their delete timers |
| `/stats` | Enhanced statistics dashboard with queue info |
| `/webapp` | Web dashboard information and URLs |

---

## 🚀 Quick Deploy on Koyeb

### Prerequisites
- GitHub account
- Telegram **bot token** from [@BotFather](https://t.me/BotFather)
- Telegram **user session string** from [@SessionStringZBot](https://t.me/SessionStringZBot)
- Chat IDs of groups/channels to monitor

### 🌟 One-Click Deploy

⭐ **IMPORTANT**: Always **star** the [original repository](https://github.com/PIROXTG/AutoWiper) first!

1. **Import as Private Repository**:
   - Go to GitHub → **Import repository**
   - Clone URL: `https://github.com/PIROXTG/AutoWiper.git`
   - **Repository name**: `AutoWiper-Private` (or your choice)
   - Make it **PRIVATE** ⚠️ (crucial for security)
   - **DO NOT FORK** - Others can see your environment variables if you fork publicly

2. **Switch to Koyeb Branch**:
   ```bash
   git checkout koyeb
   git push origin koyeb
   ```

3. **Deploy on Koyeb**:
   - Sign up at [Koyeb](https://www.koyeb.com/) (free tier available)
   - Click **"Create App"** → **"Deploy from Git"**
   - Connect your GitHub account
   - Select your **private** imported repository
   - **Branch**: Select `koyeb` ⚠️ (important!)
   - **Build method**: `Dockerfile` (auto-detected)
   - **Service type**: `Web Service` (for web dashboard)
   - **Port**: `8080` (auto-detected from Dockerfile)

4. **Configure Environment Variables**:
   ```bash
   API_ID=12345678
   API_HASH=your_api_hash_here
   BOT_TOKEN=your_bot_token_here
   SESSION=your_session_string_here
   CHAT_IDS=[-1001234567890,-1009876543210]
   ```

5. **Deploy & Access**:
   - Click **Deploy** 🚀
   - Wait for deployment to complete (~2-3 minutes)
   - Access your web dashboard at the provided Koyeb URL
   - Bot will automatically start and send you a confirmation message

### 🎯 Post-Deployment
- **Web Dashboard**: Access via your Koyeb app URL
- **Health Monitoring**: Use `/health` endpoint for uptime services
- **System Stats**: Monitor via `/stats` API endpoint
- **Bot Status**: Check Telegram for startup confirmation message

---

## ⚙️ Configuration Guide

### Environment Variables
Set these in your Koyeb app settings:

#### 🔴 Required Variables
```bash
API_ID=12345678                                    # Telegram API ID
API_HASH=abcdef1234567890abcdef1234567890          # Telegram API Hash
BOT_TOKEN=1234567890:ABCDEF1234567890abcdef       # Bot token from @BotFather
SESSION=BQABCDEFGHIJKLMNOPQRSTUVWXYZabcdef...     # User session string
CHAT_IDS=[-1001234567890,-1009876543210]           # Chat IDs to monitor
```

#### 🟡 Optional Variables
```bash
PORT=8080                                          # Web server port (auto-detected)
ID_DUR={"-1001234567890":3600,"-1009876543210":7200}  # Custom delete timers
```

### Delete Timer Configuration
```python
ID_DUR = {
    -1001234567890: 300,      # 5 minutes
    -1009876543210: 1800,     # 30 minutes  
    -1007654321098: 3600,     # 1 hour
    -1005432109876: 86400,    # 24 hours
    -1003210987654: 0,        # Disabled (no auto-delete)
}
```

### Dependencies (Auto-installed)
```txt
pyrotgfork==2.1.35          # Telegram client
tgcrypto==1.2.5             # Encryption
APScheduler==3.10.4         # Task scheduling
aiohttp==3.9.1              # Web server
psutil==5.9.6               # System monitoring
```

---

## 🌐 Web Dashboard Guide

### 📱 Dashboard Overview
The web dashboard provides comprehensive monitoring:

```
🤖 AutoWiper Dashboard
├── 📊 Bot Status
│   ├── Uptime: 2:30:45
│   ├── Active Jobs: 15
│   ├── Monitored Chats: 3
│   └── Status: 🟢 Running
├── 🖥️ System Health  
│   ├── CPU: 15.2%
│   ├── RAM: 45.8% (1.2/2.8 GB)
│   ├── Disk: 32.1% (8.5 GB free)
│   └── Load: 0.80
├── 🤖 Bot Process
│   ├── Memory: 45.2 MB
│   ├── CPU: 2.1%
│   └── Threads: 12
└── 📡 Network
    ├── Sent: 125.8 MB
    └── Received: 89.3 MB
```

### 🔗 API Examples

#### Health Check Endpoint
```bash
GET https://your-app.koyeb.app/health

Response:
{
  "status": "healthy",
  "uptime": "2:30:45", 
  "active_jobs": 15,
  "monitored_chats": 3,
  "bot_running": true,
  "user_running": true,
  "timestamp": "2024-01-15T10:30:45"
}
```

#### Detailed Statistics
```bash
GET https://your-app.koyeb.app/stats

Response:
{
  "uptime": "2:30:45",
  "active_jobs": 15,
  "system": {
    "cpu_percent": 15.2,
    "memory_percent": 45.8,
    "memory_total_gb": 2.8,
    "disk_percent": 32.1,
    "load_avg": [0.8, 0.9, 0.7]
  },
  "bot_status": {
    "bot_connected": true,
    "user_connected": true,
    "scheduler_running": true
  },
  "process": {
    "memory_mb": 45.2,
    "cpu_percent": 2.1,
    "threads": 12
  }
}
```

### 📊 Monitoring Integration
Use with external services:
- **UptimeRobot**: Monitor `/health` endpoint
- **Pingdom**: Set up HTTP checks  
- **StatusCake**: Performance monitoring
- **New Relic**: APM integration
- **Custom Scripts**: Automated health checks

---

## 🔐 Security & Best Practices

### 🛡️ Security Guidelines
- **⚠️ CRITICAL**: Never fork publicly - use GitHub **Import repository** feature
- Always make your imported repository **PRIVATE**
- **Never commit** real credentials to any repository
- Use **environment variables only** for all deployments
- The web dashboard shows **no sensitive information** (safe to expose)
- **HTTPS only** - Koyeb provides SSL certificates automatically

### 🔒 Credential Security
If credentials are accidentally exposed:
1. **Immediately** revoke bot token via @BotFather
2. **Generate new** session string via @SessionStringZBot  
3. **Delete** compromised repository and recreate
4. **Update** environment variables in Koyeb
5. **Redeploy** with new credentials

### ⚡ Performance Notes
- **Memory Usage**: ~50-80MB (lightweight)
- **CPU Usage**: ~1-5% (very efficient)
- **Network**: Low bandwidth, periodic API calls
- **Web Server**: <1MB additional memory overhead
- **Auto-ping**: Minimal resource usage (every 2 minutes)

---

## 🛠️ Troubleshooting

### Common Issues

**❌ Web dashboard not loading?**
- Ensure you're using the `koyeb` branch
- Check if deployment shows "Web Service" type
- Verify port 8080 is configured
- Check Koyeb logs for startup errors

**❌ Bot not staying online?**
- Confirm you're using `koyeb` branch (has auto-ping)
- Check if web service is properly configured
- Verify health check endpoint responds: `/health`
- Monitor Koyeb logs for ping activity

**❌ Deployment fails?**
- Ensure `koyeb` branch is selected
- Check all environment variables are set
- Verify CHAT_IDS format: `[-1001234567890,-1009876543210]`
- Review build logs in Koyeb dashboard

**❌ Bot commands not working?**
- Verify session string is valid and active
- Check bot token with @BotFather
- Ensure user account has delete permissions in target chats
- Confirm chat IDs are negative numbers for groups

**❌ System stats not showing?**
- This is normal on some restricted cloud environments
- Basic stats will be shown as fallback
- Check if `psutil` has necessary permissions

### 🔍 Debugging Steps
1. **Check Koyeb Logs**: View real-time application logs
2. **Test Health Endpoint**: Visit `/health` to verify web server
3. **Verify Environment**: Ensure all required variables are set
4. **Test Bot Token**: Send `/start` to your bot
5. **Check Session**: Ensure session string is not expired

---

## 🤝 Support & Contributing

### 🆘 Get Help
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/PIROXTG/AutoWiper/issues)
- 💬 **Support Chat**: [@piroxhelorobot](https://t.me/piroxhelorobot)
- 📖 **Documentation**: Check README and inline code comments
- 🌐 **Web Issues**: Specify you're using `koyeb` branch

### 🤝 Contributing  
Contributions welcome! Areas for improvement:
- **🎨 UI/UX**: Better web dashboard design
- **📊 Analytics**: More detailed statistics
- **🔐 Security**: Authentication, rate limiting
- **🚀 Performance**: Caching, optimization
- **📱 Mobile**: Enhanced mobile experience
- **🔌 Integrations**: Webhook support, external APIs

**How to contribute**:
1. Fork the repository (for contributions only)
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📚 Technical Architecture

### 🏗️ System Design
```
AutoWiper (Koyeb Edition)
├── 🌐 Web Server (aiohttp)
│   ├── Dashboard (HTML/CSS/JS)
│   ├── Health API (/health)
│   ├── Stats API (/stats)
│   └── Auto-ping (every 2min)
├── 🤖 Telegram Bot (pyrogram)
│   ├── Command handling
│   ├── Message monitoring
│   └── Auto-deletion
├── 👤 Telegram User (pyrogram)
│   ├── Message deletion
│   ├── Chat history processing
│   └── Owner commands
├── ⏰ Scheduler (APScheduler)
│   ├── Timed deletions
│   ├── Regular cleanup (4min)
│   └── Heartbeat monitoring
└── 📊 System Monitor (psutil)
    ├── Resource monitoring
    ├── Performance metrics
    └── Process statistics
```

### 🔧 Technologies Used
- **[Pyrogram v2.0](https://docs.pyrogram.org/)** - Telegram MTProto API
- **[aiohttp v3.9](https://docs.aiohttp.org/)** - Async HTTP server  
- **[APScheduler v3.10](https://apscheduler.readthedocs.io/)** - Task scheduling
- **[psutil v5.9](https://psutil.readthedocs.io/)** - System monitoring
- **[Docker](https://www.docker.com/)** - Containerization
- **Python 3.8+** - Runtime environment

### ⚡ Performance Characteristics
- **Cold Start**: ~10-15 seconds
- **Memory**: 50-80MB average usage
- **CPU**: 1-5% under normal load
- **Network**: <1MB/hour typical usage  
- **Disk I/O**: Minimal (logs only)
- **Concurrent Connections**: 100+ supported

---

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

**Open Source Libraries**:
- Pyrogram: LGPL-3.0 License
- aiohttp: Apache-2.0 License  
- APScheduler: MIT License
- psutil: BSD-3-Clause License

---

## 🙏 Acknowledgments

- **[PIROXTG](https://github.com/PIROXTG)** - Original AutoWiper creator
- **[Pyrogram](https://docs.pyrogram.org/)** - Excellent Telegram framework
- **[aiohttp](https://docs.aiohttp.org/)** - Robust async web framework
- **[@SessionStringZBot](https://t.me/SessionStringZBot)** - Trusted session generator
- **[Koyeb](https://www.koyeb.com/)** - Excellent free cloud hosting
- **Community** - Users, testers, and contributors

---

## 🎯 Quick Links

### 🚀 Deploy Now
[![Deploy to Koyeb](https://img.shields.io/badge/Deploy%20to%20Koyeb-00C7B7?style=for-the-badge&logo=koyeb&logoColor=white)](https://www.koyeb.com/)

### 📚 Resources  
- **[Main Repository](https://github.com/PIROXTG/AutoWiper)** - Original AutoWiper
- **[Koyeb Documentation](https://www.koyeb.com/docs)** - Deployment guides
- **[Pyrogram Docs](https://docs.pyrogram.org/)** - Telegram API reference
- **[aiohttp Docs](https://docs.aiohttp.org/)** - Web server documentation

### 🔗 Community
- **[Support Bot](https://t.me/piroxhelorobot)** - Get help
- **[Support Group](https://t.me/piroxbots)** - Community chat
- **[Session Generator](https://t.me/SessionStringZBot)** - Get session strings

---

<div align="center">

**🌐 AutoWiper Koyeb Edition - Advanced Telegram Auto-Cleaner**

**🚀 With Web Dashboard • 📊 System Monitoring • 🔄 Auto-Keep-Alive**

[⭐ Star Original Repo](https://github.com/PIROXTG/AutoWiper) • [🌐 Koyeb Branch](https://github.com/PIROXTG/AutoWiper/tree/koyeb) • [📢 Join Community](https://t.me/piroxbots)

*Keeping your Telegram chats clean with style! 🧹✨*

</div>