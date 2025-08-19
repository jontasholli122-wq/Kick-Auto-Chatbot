# Detailed Setup Guide

This guide will walk you through setting up the Kick.com Chat Bot step by step.

## 📋 Prerequisites

### System Requirements
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.8 or higher
- **Memory**: At least 4GB RAM (8GB+ recommended for multiple sessions)
- **Browser**: Google Chrome (latest version)
- **Internet**: Stable broadband connection

### Account Requirements
- Valid Kick.com account(s)
- Accounts should be in good standing (not banned/restricted)
- Recommended: Use dedicated accounts for botting

## 🔧 Installation Steps

### 1. Install Python

**Windows:**
1. Download Python from [python.org](https://python.org)
2. During installation, check "Add Python to PATH"
3. Verify: Open Command Prompt and run `python --version`

**macOS:**
```bash
# Using Homebrew (recommended)
brew install python

# Or download from python.org
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### 2. Install Google Chrome

Download and install Google Chrome from [google.com/chrome](https://google.com/chrome)

### 3. Clone or Download the Project

**Option A: Git Clone (Recommended)**
```bash
git clone https://github.com/yourusername/kickcom-chatbot.git
cd kickcom-chatbot
```

**Option B: Download ZIP**
1. Download the ZIP file from GitHub
2. Extract to your desired location
3. Open terminal/command prompt in the extracted folder

### 4. Set Up Python Environment

**Create Virtual Environment (Recommended):**
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

**Install Dependencies:**
```bash
pip install -r requirements.txt
```

## 🍪 Cookie Setup

### Method 1: Cookie Editor Extension (Easiest)

1. **Install Extension**
   - Chrome: [Cookie Editor](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)
   - Firefox: [Cookie Editor](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/)

2. **Export Cookies**
   - Go to Kick.com and log in
   - Click the Cookie Editor extension icon
   - Click "Export" → "Export as JSON"
   - Save as `cookies/account1.json`

3. **Repeat for Multiple Accounts**
   - Use different browsers/incognito windows
   - Save each as `cookies/account2.json`, etc.

### Method 2: Developer Tools (Advanced)

1. **Open Developer Tools**
   - Go to Kick.com and log in
   - Press F12 to open Developer Tools
   - Go to Application → Storage → Cookies → kick.com

2. **Export Cookies Manually**
   - Copy all cookie data
   - Format as JSON array (see example below)
   - Save in `cookies/` folder

**Example Cookie JSON Format:**
```json
[
  {
    "name": "session_id",
    "value": "your_session_value_here",
    "domain": ".kick.com",
    "path": "/",
    "secure": true,
    "httpOnly": true,
    "sameSite": "Lax"
  },
  {
    "name": "another_cookie",
    "value": "another_value",
    "domain": ".kick.com",
    "path": "/",
    "secure": false,
    "httpOnly": false,
    "sameSite": "None"
  }
]
```

## 📝 Message Configuration

### Default Messages
The bot comes with default messages, but you should customize them:

**Edit `chats.txt`:**
```
Hello everyone!
Great stream!
Loving the content!
This is awesome!
Keep it up!
Amazing gameplay!
LOL
Nice!
Poggers
Good stuff!
```

### Message Guidelines
- **Be Natural**: Use messages you would actually type
- **Vary Length**: Mix short and long messages
- **Stay Positive**: Avoid controversial or negative content
- **Use Emotes**: Include popular Twitch/Kick emotes
- **Be Relevant**: Match the streamer's content style

## 🚀 Running the Bot

### First Run
```bash
python chatbot.py
```

### GUI Configuration

1. **Set Sessions**: Start with 1-2 sessions for testing
2. **Configure Timing**:
   - Message Interval: 30-90 seconds (recommended)
   - Startup Delay: 10-15 seconds between sessions
3. **Choose Options**:
   - Enable "Sequential Mode" for stability
   - Enable "Headless Mode" to hide browsers
4. **Start**: Click "Start Bot Sessions"

### Monitoring

- **Status Log**: Shows all bot activities in real-time
- **Active Sessions**: Displays currently running sessions
- **Message Count**: Tracks messages sent per session

## 🛡️ Security & Safety

### Account Safety
- **Use Burner Accounts**: Don't use your main Kick.com account
- **Spread Sessions**: Don't run too many from the same IP
- **Monitor for Bans**: Watch for account restrictions
- **Backup Cookies**: Keep cookie files backed up

### Privacy
- **Keep Cookies Private**: Never share cookie files
- **Use VPN**: Consider using a VPN for multiple accounts
- **Clean Up**: Delete cookie files when done

### Rate Limiting
- **Reasonable Intervals**: Don't spam messages too quickly
- **Respect Chat Rules**: Follow streamer and platform guidelines
- **Monitor Response**: Watch for rate limiting or restrictions

## 🔍 Verification

### Test Your Setup

1. **Single Session Test**:
   - Set sessions to 1
   - Start the bot
   - Verify it logs in and sends a message

2. **Multi-Session Test**:
   - Gradually increase sessions (2, then 3, etc.)
   - Monitor for errors in the status log
   - Check that all sessions start successfully

3. **Long-Term Test**:
   - Run for 30+ minutes
   - Verify messages continue to send
   - Check for any crashes or errors

## 🆘 Common Issues

### Installation Problems
- **Python Not Found**: Make sure Python is in your PATH
- **Permission Denied**: Run as administrator (Windows) or use `sudo` (Linux/macOS)
- **Module Not Found**: Reinstall requirements with `pip install -r requirements.txt`

### Browser Issues
- **Chrome Not Found**: Install Google Chrome or update ChromeDriver path
- **Driver Conflicts**: Delete Chrome cache and restart
- **Multiple Instance Errors**: Use Sequential Mode

### Login Problems
- **Cookies Expired**: Re-export fresh cookies
- **Invalid Format**: Check JSON syntax in cookie files
- **Account Banned**: Check account status on Kick.com

### Performance Issues
- **High CPU Usage**: Enable Headless Mode
- **Memory Leaks**: Restart bot sessions periodically
- **Slow Performance**: Reduce concurrent sessions

For more detailed troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## 📞 Getting Help

If you encounter issues:

1. **Check the logs** in the GUI status window
2. **Review this setup guide** thoroughly
3. **Search existing issues** on GitHub
4. **Create a new issue** with:
   - Error messages
   - Your configuration
   - Steps to reproduce
   - System information

## 🎯 Next Steps

Once you have the bot running:

1. **Optimize Your Messages**: Add more natural, varied content
2. **Scale Gradually**: Slowly increase concurrent sessions
3. **Monitor Performance**: Watch system resources and bot behavior
4. **Customize Features**: Modify the script for your specific needs

Happy botting! 🚀