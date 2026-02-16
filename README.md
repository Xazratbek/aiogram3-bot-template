# Aiogram 3.24.0 bot template (Python 3.12)

Minimal, ready-to-run template with folders for handlers, keyboards, filters,
data, and utils. Uses aiogram v3 routers and dispatcher.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
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

## Notes on aiogram v3

- Uses `Router` and `Dispatcher` with `include_routers(...)`
- Default bot properties (like `parse_mode`) are set via `DefaultBotProperties`
- Filters are imported from `aiogram.filters` (e.g. `CommandStart`, `Command`)
