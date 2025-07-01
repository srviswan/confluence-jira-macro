# Quick Start for Space Admins 🚀

**You don't need Confluence Admin access! Here are your best options:**

## 🥇 Best Option: HTML Macro (5 minutes)

### What you need:
- Space Admin access ✅
- JIRA API token 🔑
- HTML Macro enabled (most instances have this)

### Quick Steps:
1. **Test first**: Open `demo.html` → Enter your JIRA details → Click "Load Issues"
2. **Copy working config** from demo
3. **Edit your page** → Add HTML Macro (+ → Other macros → Formatting → HTML)
4. **Paste content** from `jira-macro.html`
5. **Update config** section with your details
6. **Save and done!** 🎉

---

## 🥈 Alternative: Source Editor (Direct HTML)

### If HTML Macro isn't available:
1. Edit page → Switch to **Source Editor** (< > button)
2. Paste entire `jira-macro.html` content
3. Update configuration variables
4. Switch back to visual editor → Save

---

## 🥉 External Hosting + Iframe

### If you can host files:
1. Upload `jira-macro.html` to GitHub Pages/web server
2. Use **Iframe Macro** in Confluence
3. Point to your hosted URL

---

## ⚡ 2-Minute Setup

```javascript
// Just change these 4 lines in jira-macro.html:
const config = {
    baseUrl: 'https://YOUR-COMPANY.atlassian.net',
    username: 'YOUR-EMAIL@company.com', 
    apiToken: 'YOUR-API-TOKEN',
    jql: 'project = "YOUR-PROJECT" AND status != "Done"'
};
```

## 🔑 Get API Token (1 minute)
1. Go to JIRA → Profile → Security → API tokens
2. Create token → Copy it
3. Test in `demo.html` first!

## ❌ What you CAN'T do (requires admin):
- Create User Macros
- Install marketplace apps
- Modify global settings

## ✅ What you CAN do (as space admin):
- Add HTML macros ← **This is your best bet**
- Edit page source
- Embed iframes
- Create multiple pages with different JQL queries

**🎯 Recommendation: Start with HTML Macro method - it's the easiest and most reliable for space admins!**
