# Render Environment Variables

Set these values in Render Dashboard → Service → Environment.

```env
TELEGRAM_BOT_TOKEN=PASTE_NEW_BOT_TOKEN_HERE
TELEGRAM_ADMIN_IDS=PASTE_YOUR_TELEGRAM_USER_ID_HERE
DATABASE_URL=PASTE_RENDER_INTERNAL_DATABASE_URL_HERE
FRONTEND_URL=PASTE_FRONTEND_URL_HERE
BACKEND_URL=PASTE_BACKEND_URL_HERE
```

Do not commit real secrets to GitHub. Keep the bot token, database URL/password, and other credentials only in Render Environment Variables or a local `.env` file that is ignored by Git.
