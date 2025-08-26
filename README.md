# AutoWiper 🧹

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Pyrogram](https://img.shields.io/badge/Pyrogram-v2.0-red)](https://docs.pyrogram.org/)
[![Made with Python](https://img.shields.io/badge/Made%20with-Python-37766B.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Deploy on Koyeb](https://img.shields.io/badge/Deploy-Koyeb-00C7B7)](https://www.koyeb.com/)

> **A lightweight Telegram auto-cleaner bot** that automatically deletes messages in groups and channels after a set time. Keep your chats **clutter-free, spam-free, and organized** — automatically.

🔹 **Made by**: [PIROXTG](https://github.com/PIROXTG)  
🔹 **Session Generator**: [@SessionStringZBot](https://t.me/SessionStringZBot) (trusted & secure)  
🔹 **Support & Help**: [@piroxhelorobot](https://t.me/piroxhelorobot)

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

## ✨ Key Features

✅ **Auto-delete messages** in multiple Telegram groups or channels  
✅ **Per-chat timer control** — set different durations for each chat  
✅ **Lightweight & fast** — built with [Pyrogram](https://docs.pyrogram.org/) (MTProto API)  
✅ **Userbot + Bot mode** — uses a user session for full message control  
✅ **Scheduled cleanup** — uses APScheduler for reliable timing  
✅ **Remote management** — control via Telegram commands  
✅ **Cloud ready** — deploy on Koyeb, Heroku, or any Linux server  
✅ **Production-grade** — graceful shutdown & comprehensive logging

---

## 📋 Commands Reference

### Bot Commands (Private Chat)
| Command | Description |
|---------|-------------|
| `/start` | Check if the bot is online |
| `/ping` | Measure bot response latency |
| `/status` | View uptime, active jobs, and monitored chats |

### Userbot Commands (In Monitored Chats)
| Command | Description |
|---------|-------------|
| `/delete` | Force immediate cleanup of old messages |
| `/update` | Pull latest code from GitHub and restart |
| `/restart` | Restart the bot service |
| `/chats` | List all monitored chats and their delete timers |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git installed on your system
- Telegram **bot token** from [@BotFather](https://t.me/BotFather)
- Telegram **user session string** from [@SessionStringZBot](https://t.me/SessionStringZBot)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/PIROXTG/AutoWiper.git
   cd AutoWiper
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the bot (Local Development Only)**
   
   ⚠️ **For local testing only** - Edit `config.py`:
   ```python
   # Telegram API Credentials
   API_ID = 12345678
   API_HASH = "your_api_hash_here"
   BOT_TOKEN = "your_bot_token_here"
   SESSION = "your_user_session_string_here"
   
   # Chat Configuration
   CHAT_IDS = [-1001234567890, -1009876543210]  # Chat IDs to monitor
   
   # Delete Timer Configuration (in seconds)
   ID_DUR = {
       -1001234567890: 3600,     # Delete after 1 hour
       -1009876543210: 7200,     # Delete after 2 hours
       # Use 0 to disable auto-delete for specific chats
   }
   ```
   
   **⚠️ NEVER commit this file with real credentials!**

4. **Run the bot**
   ```bash
   python main.py
   ```

---

## ☁️ Cloud Deployment

### Deploy on Koyeb (Recommended ✅)

Koyeb offers free hosting perfect for AutoWiper using Docker:

⭐ **IMPORTANT**: Always **star** the original repository first!

1. **Import as Private Repository**:
   - Go to GitHub → **Import repository**
   - Clone URL: `https://github.com/PIROXTG/AutoWiper.git`
   - Make it **PRIVATE** (crucial for security)
   - **DO NOT FORK** - Others can see your environment variables if you fork publicly

2. **Deploy on Koyeb**:
   - Sign up at [Koyeb](https://www.koyeb.com/)
   - Click **"Create App"** → **"Deploy from Git"**
   - Select your **private** imported repository
   - Choose **Docker** deployment method
   - Set **Service Type**: `Worker`
   - Add **Environment Variables** (see configuration below)
   - Click **Deploy** 🚀

⚠️ **Security Warning**: Never store credentials in public repositories. If you accidentally push sensitive data, immediately rotate all tokens and session strings.

### Alternative Deployment Options

- **Heroku**: Use the included `Procfile`
- **Railway**: Connect your GitHub repo
- **VPS/Server**: Run with `systemd` or `screen`

---

## ⚙️ Configuration Guide

### Environment Variables (Production)
For cloud deployment, set these environment variables instead of editing `config.py`:

```bash
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
SESSION=your_session_string
CHAT_IDS=[-1001234567890,-1009876543210]
```

### Timer Configuration Examples
```python
ID_DUR = {
    -1001234567890: 300,      # 5 minutes
    -1009876543210: 1800,     # 30 minutes
    -1007654321098: 3600,     # 1 hour
    -1005432109876: 86400,    # 24 hours
    -1003210987654: 0,        # Disabled (no auto-delete)
}
```

---

## 🔐 Security & Best Practices

### Security Guidelines
- **⚠️ CRITICAL**: Never fork this repository publicly - use GitHub's **Import** feature instead
- Always make your repository **PRIVATE** when importing
- **Never commit** `config.py` with real credentials to any repository
- Use **environment variables only** for production deployments
- If credentials are accidentally exposed, immediately:
  1. Revoke the bot token via @BotFather
  2. Generate a new session string
  3. Delete and recreate the compromised repository
- **DISCLAIMER**: The repository owner is not responsible for compromised accounts due to improper handling of credentials

### Important Notes
- The bot requires **delete message permissions** in target chats
- **Pinned messages** are preserved and won't be deleted
- Only messages older than the specified duration are removed
- The bot uses a user account session for broader permissions

---

## 🛠️ Troubleshooting

### Common Issues

**Bot not deleting messages?**
- Ensure the user account has admin/delete permissions
- Check if chat IDs are correct (negative numbers for groups/channels)
- Verify the session string is valid

**Connection errors?**
- Check your internet connection
- Verify API credentials are correct
- Ensure Telegram isn't blocked in your region

**Bot stops working?**
- Check logs for error messages
- Restart the bot with `/restart` command
- Update to latest version with `/update`

---

## 🤝 Support & Contributing

### Get Help
- 🐛 **Bug Reports**: [Open an issue](https://github.com/PIROXTG/AutoWiper/issues)
- 💬 **Support Chat**: [@piroxhelorobot](https://t.me/piroxhelorobot)
- 📖 **Documentation**: Check this README and inline comments

### Contributing
Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Areas for improvement:
- Performance optimizations
- Additional command features
- Better error handling
- Migration to Hydrogram (Pyrogram successor)

---

## 📚 Technical Details

### Built With
- **[Pyrogram v2.0](https://docs.pyrogram.org/)** - MTProto API framework
- **[APScheduler](https://apscheduler.readthedocs.io/)** - Task scheduling
- **Python 3.8+** - Core language

### Architecture
- **Hybrid approach**: Bot + Userbot for maximum compatibility
- **Asynchronous operations** for better performance
- **Graceful error handling** with comprehensive logging
- **Memory efficient** message tracking and cleanup

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **[Pyrogram](https://docs.pyrogram.org/)** - Excellent MTProto API framework
- **[@SessionStringZBot](https://t.me/SessionStringZBot)** - Trusted session string generator
- **[Koyeb](https://www.koyeb.com/)** - Reliable free cloud hosting
- **Community** - Thanks to all users and contributors!

---

<div align="center">

**🚀 AutoWiper - Keeping your Telegram chats clean, one message at a time.**

[⭐ Star this repo](https://github.com/PIROXTG/AutoWiper) • [🍴 Fork it](https://github.com/PIROXTG/AutoWiper/fork) • [📢 Join Support](https://t.me/piroxbots)

</div>