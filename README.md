# Aiogram 3.24.0 bot template (Python 3.12)

Minimal, ready-to-run template with folders for handlers, keyboards, filters,
data, and utils. Includes DB, i18n, middlewares, and a simple admin panel.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
cp .env.example .env
python -m bot.main
```

## Folders

- `bot/handlers` - message and command handlers (routers)
- `bot/keyboards` - reply/inline keyboards
- `bot/filters` - custom filters
- `bot/data` - constants and static data
- `bot/utils` - utilities (commands, helpers)
- `bot/middlewares` - middlewares (optional)
- `bot/db` - database layer (SQLite with aiosqlite)
- `bot/i18n` - simple translations and locale helpers

## Notes on aiogram v3

- Uses `Router` and `Dispatcher` with `include_routers(...)`
- Default bot properties (like `parse_mode`) are set via `DefaultBotProperties`
- Filters are imported from `aiogram.filters` (e.g. `CommandStart`, `Command`)

## Environment

- `BOT_TOKEN` - bot token
- `ADMIN_IDS` - comma-separated admin IDs
- `DB_PATH` - SQLite path (default: `storage/bot.db`)
- `DEFAULT_LOCALE` - default locale (default: `uz`)
- `FLOOD_LIMIT` - seconds between messages per user (0 disables)
