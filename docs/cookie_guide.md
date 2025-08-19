# Cookie Export Guide 🍪

This guide explains how to properly export your Kick.com login cookies for use with the chat bot.

## 🔒 Security Warning

**⚠️ IMPORTANT**: Cookie files contain your login session data. Treat them like passwords:
- Never share cookie files with anyone
- Store them securely on your computer
- Delete them when no longer needed
- Use dedicated accounts for botting (not your main account)

## 📱 Method 1: Browser Extension (Recommended)

### For Google Chrome

1. **Install Cookie Editor Extension**
   - Go to [Chrome Web Store](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)
   - Click "Add to Chrome"
   - Pin the extension to your toolbar

2. **Login to Kick.com**
   - Go to [kick.com](https://kick.com)
   - Log in with your account
   - Navigate to any live stream to ensure you're fully logged in

3. **Export Cookies**
   - Click the Cookie Editor extension icon
   - You should see all Kick.com cookies listed
   - Click the "Export" button at the bottom
   - Select "Export as JSON"
   - Save the file as `account1.json` in your `cookies/` folder

### For Mozilla Firefox

1. **Install Cookie Editor Add-on**
   - Go to [Firefox Add-ons](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/)
   - Click "Add to Firefox"

2. **Follow the same export process** as Chrome above

## 🛠️ Method 2: Developer Tools (Manual)

### Google Chrome Developer Tools

1. **Open Developer Tools**
   - Go to Kick.com and log in
   - Press `F12` or right-click → "Inspect"
   - Go to the "Application" tab

2. **Navigate to Cookies**
   - In the left sidebar, expand "Storage"
   - Click on "Cookies"
   - Click on "https://kick.com"

3. **Copy Cookie Data**
   - You'll see all cookies in a table
   - For each important cookie, note down:
     - Name
     - Value
     - Domain
     - Path
     - Secure flag
     - HttpOnly flag
     - SameSite setting

4. **Format as JSON**
   Create a JSON file with this structure:
   ```json
   [
     {
       "name": "session_id",
       "value": "your_actual_session_value",
       "domain": ".kick.com",
       "path": "/",
       "secure": true,
       "httpOnly": true,
       "sameSite": "Lax"
     },
     {
       "name": "remember_token", 
       "value": "your_remember_token_value",
       "domain": ".kick.com",
       "path": "/",
       "secure": true,
       "httpOnly": true,
       "sameSite": "Lax"
     }
   ]
   ```

### Firefox Developer Tools

1. **Open Developer Tools**
   - Press `F12` or right-click → "Inspect Element"
   - Go to the "Storage" tab

2. **Navigate to Cookies**
   - In the left sidebar, click "Cookies"
   - Click on "https://kick.com"

3. **Export Process** is the same as Chrome above

## 🔍 Important Cookies to Include

Make sure your exported cookies include these essential ones:

### Required Cookies
- `session_id` - Your login session
- `remember_token` - Keeps you logged in
- `XSRF-TOKEN` - Security token
- `laravel_session` - Laravel framework session

### Optional but Helpful
- `chat_settings` - Chat preferences
- `user_preferences` - User settings
- `timezone` - User timezone
- Any cookies starting with `kick_`

## 📁 File Organization

### Naming Convention
Use descriptive names for your cookie files:
```
cookies/
├── main_account.json
├── bot_account_1.json
├── bot_account_2.json
├── backup_account.json
└── test_account.json
```

### File Structure
Each JSON file should contain an array of cookie objects:
```json
[
  {
    "name": "cookie_name",
    "value": "cookie_value",
    "domain": ".kick.com",
    "path": "/",
    "secure": true,
    "httpOnly": false,
    "sameSite": "Lax"
  }
]
```

## ✅ Validation

### Test Your Cookies

1. **Run Single Session Test**:
   ```bash
   python chatbot.py
   ```
   - Set sessions to 1
   - Start the bot
   - Check if it logs in successfully

2. **Check Status Log**:
   - Look for "Login successful!" message
   - If you see "Login failed", your cookies may be invalid

3. **Manual Verification**:
   - Open a new incognito window
   - Go to kick.com
   - Use the Cookie Editor to import your exported cookies
   - Refresh the page - you should be logged in

### Common Cookie Issues

**Cookies Expired**
- Kick.com sessions expire after a certain time
- Re-export fresh cookies from an active session
- Some accounts may require periodic re-authentication

**Missing Required Cookies**
- Ensure you exported ALL cookies from kick.com
- Don't filter or remove any cookies manually
- Include both secure and non-secure cookies

**Wrong Domain Format**
- Cookies should have domain `.kick.com` (with leading dot)
- Path should typically be `/`
- Secure flag should match the original cookie

## 🔄 Cookie Refresh Process

### When to Refresh Cookies

- **Bot login fails**: Usually means cookies expired
- **Chat messages not sending**: Session may be invalid
- **Regular maintenance**: Refresh every 1-2 weeks
- **After password changes**: Always refresh after changing password

### Automated Refresh (Advanced)

For advanced users, you can create a script to auto-refresh cookies:

```python
# refresh_cookies.py
import json
import os
from selenium import webdriver

def refresh_account_cookies(username, password):
    """Login and export fresh cookies."""
    driver = webdriver.Chrome()
    try:
        driver.get("https://kick.com/login")
        # Login process here...
        # Export cookies...
        pass
    finally:
        driver.quit()
```

## 🛡️ Security Best Practices

### Protecting Your Cookies

1. **File Permissions**:
   ```bash
   # Linux/macOS - restrict access
   chmod 600 cookies/*.json
   ```

2. **Encryption** (Optional):
   - Encrypt cookie files when not in use
   - Use tools like GPG or 7-Zip with password protection

3. **Regular Cleanup**:
   - Delete old/unused cookie files
   - Clear browser data periodically
   - Rotate accounts regularly

### Account Security

1. **Use Dedicated Accounts**:
   - Create separate accounts just for botting
   - Don't use your main viewing account
   - Use different emails and passwords

2. **Enable 2FA** (if available):
   - Add two-factor authentication to accounts
   - Keep backup codes secure

3. **Monitor Account Status**:
   - Regularly check for warnings or restrictions
   - Watch for unusual login notifications
   - Be prepared to lose bot accounts

## 🔧 Troubleshooting Cookies

### Login Failed Issues

**Problem**: "Login verification failed"
**Solutions**:
1. Re-export cookies from a fresh login
2. Make sure you're logged in when exporting
3. Check that all cookies were exported
4. Verify JSON format is correct

**Problem**: "Chat interface not found"
**Solutions**:
1. Check if the stream is live
2. Verify account has chat permissions
3. Make sure account isn't banned/restricted
4. Try navigating to a different stream

**Problem**: "Operation failed" immediately
**Solutions**:
1. Check cookie file format
2. Verify file paths are correct
3. Ensure Chrome is properly installed
4. Try running with a single session first

### Cookie Format Issues

**Invalid JSON Error**:
```bash
# Validate your JSON files
python -m json.tool cookies/account1.json
```

**Missing Fields**:
Ensure each cookie has these fields:
- `name` (required)
- `value` (required)
- `domain` (required)
- `path` (required)
- `secure`, `httpOnly`, `sameSite` (optional but recommended)

## 📞 Getting Help

If you're still having issues with cookies:

1. **Check the main troubleshooting guide**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. **Verify your setup**: Follow this guide step by step
3. **Test with a single account**: Start simple before scaling up
4. **Create a GitHub issue**: Include error messages and your configuration

## 🎯 Quick Checklist

Before running the bot, verify:

- [ ] Python 3.8+ installed
- [ ] Chrome browser installed
- [ ] Virtual environment activated
- [ ] Requirements installed (`pip install -r requirements.txt`)
- [ ] Cookie files in `cookies/` folder
- [ ] Cookie files are valid JSON format
- [ ] Cookies exported from logged-in session
- [ ] `chats.txt` contains your messages
- [ ] Account(s) are in good standing on Kick.com

## 📈 Next Steps

Once your cookies are working:

1. **Test Single Session**: Verify one account works perfectly
2. **Scale Gradually**: Add more accounts one by one
3. **Monitor Performance**: Watch for any issues or bans
4. **Optimize Messages**: Refine your chat messages for better engagement
5. **Set Schedules**: Plan when to run the bot for maximum effectiveness

Happy botting! 🤖