# Aiogram v3 darslik (v2 dan keyingi eng muhim o'zgarishlar)

Quyidagi yozuvlar 3 yil oldingi aiogram v2 tajribangizni tezda yangilash uchun yozildi. Maqsad: ushbu faylni o'qib, darhol yangi (v3) bot yozishni boshlay olish.

---

## 1) Aiogram v3 haqida umumiy
- Aiogram v3 — katta breaking changes bilan chiqqan versiya.
- V2 dagi ko'p importlar va dispatcher ishlash usuli o'zgargan.
- V3 da Router konsepti markaziy rol o'ynaydi.

---

## 2) Dispatcher va Router modeli
### V2 (eski)
```python
from aiogram import Bot, Dispatcher, executor

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Hi')

if __name__ == '__main__':
    executor.start_polling(dp)
```

### V3 (yangi)
```python
import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer('Hi')

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
```

**Muhim farq:**
- `Dispatcher` endi `bot` ni konstruktorga olmaydi.
- Handlerlar `Router` ga biriktiriladi, keyin router `Dispatcher` ga ulanadi.

---

## 3) Filtrlar va F (MagicFilter o'rniga)
V3 da filtrlar yangilangan va `F` sintaksis keng qo'llaniladi.

### V3 filtrlar
```python
from aiogram import F
from aiogram.filters import Command

@router.message(Command('help'))
async def help_handler(message: Message):
    await message.answer('Help')

@router.message(F.text & ~F.text.startswith('/'))
async def echo(message: Message):
    await message.answer(message.text)
```

**Muhim farq:**
- `BaseFilter` endi `from aiogram.filters import BaseFilter` dan import qilinadi.
- `MagicFilter` v2 dagi kabi emas; v3 da `F` ishlatiladi.

---

## 4) CallbackQuery va inline tugmalar
### Inline keyboard v3
```python
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='OK', callback_data='ok')]
])

@router.message(Command('inline'))
async def inline_handler(message: Message):
    await message.answer('Tanlang:', reply_markup=kb)

@router.callback_query(F.data == 'ok')
async def ok_handler(callback: CallbackQuery):
    await callback.answer('OK bosildi')
```

**Muhim farq:**
- Handlerlar endi `router.callback_query(...)` orqali yoziladi.
- `CallbackQuery` ni qaytarish (answer) v3 da ham kerak.

---

## 5) Reply keyboard (KeyboardButton)
V2 dagidek, lekin endi ko'pincha reply keyboard va inline keyboard alohida ishlatiladi.

```python
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Sozlamalar')]],
    resize_keyboard=True,
)

@router.message(CommandStart())
async def start(message: Message):
    await message.answer('Salom', reply_markup=kb)
```

**Muhim farq:**
- Reply keyboard matni o'zgarishi uchun yangi xabar yuborish kerak (oldingi reply markup avtomatik yangilanmaydi).

---

## 6) Middleware va `data` injektsiyasi
V3 da middleware `data` kontekstiga qiymat qo'shadi, handler esa parametr sifatida oladi.

### Middleware misol
```python
from aiogram import BaseMiddleware

class MyMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        data['foo'] = 'bar'
        return await handler(event, data)
```

### Handlerda ishlatish
```python
@router.message(Command('x'))
async def x_handler(message: Message, foo: str):
    await message.answer(foo)  # 'bar'
```

**Muhim farq:**
- V2 dagi kabi global `dp['key']` ishlashi o'zgargan; v3 da data injection ancha kuchli.

---

## 7) FSM (State machine) o'zgarishlari
V3 da FSM modul yo'llari o'zgargan.

### V3 FSM misol
```python
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

class Form(StatesGroup):
    name = State()

@router.message(Command('reg'))
async def reg_start(message: Message, state: FSMContext):
    await message.answer('Ismingiz?')
    await state.set_state(Form.name)

@router.message(Form.name)
async def reg_name(message: Message, state: FSMContext):
    await message.answer(f"Salom, {message.text}!")
    await state.clear()
```

**Muhim farq:**
- `FSMContext` va `StatesGroup` import yo'llari o'zgargan.
- `state.finish()` o'rniga `state.clear()` ishlatiladi.

---

## 8) Bot sozlash (DefaultBotProperties)
V3 da parse_mode default qilib bot yaratishda beriladi.

```python
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
```

**Muhim farq:**
- `parse_mode` ni har xabar yuborishda berish shart emas.

---

## 9) Update types va start_polling
V3 da `allowed_updates` ni qo'lda berish shart emas, dispatcher o'zi aniqlashi mumkin.

```python
await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
```

---

## 10) Xatolar (Exceptions) moduli
Aiogram v3 da exceptions alohida modulda.

```python
from aiogram.exceptions import TelegramBadRequest

try:
    await bot.send_message(chat_id, text)
except TelegramBadRequest:
    pass
```

---

## 11) Migratsiya bo'yicha tez-tez uchraydigan muammolar
1) `ImportError: cannot import name BaseFilter from aiogram`
   - Tuzatish: `from aiogram.filters import BaseFilter`

2) Handlerlar ishlamayapti
   - Router yaratib, `dp.include_router(router)` qilinmagan bo'lishi mumkin.

3) Reply keyboard til o'zgarmayapti
   - Reply keyboard yangilash uchun yangi xabar yuboring.

4) FSM state tozalanmayapti
   - `state.finish()` o'rniga `state.clear()` ishlating.

---

## 12) Minimal ishga tayyor skeleton (v3)
```python
import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer('Bot ishga tushdi!')

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
```

---

## Xulosa
Aiogram v3 da eng katta o'zgarishlar: Router arxitekturasi, filtrlar (`F`), FSM import yo'llari, middleware data injektsiyasi va Bot yaratish uslubi. Shu fayldagi misollar bilan endi v3 da tezda bot yozib ketishingiz mumkin.
## 13) InlineKeyboardBuilder va ReplyKeyboardBuilder (zamonaviy uslub)
Aiogram v3 da klaviaturalarni qo'l bilan list yozish o'rniga builder orqali tuzish qulayroq va o'qilishi osonroq.

### InlineKeyboardBuilder
```python
from aiogram.utils.keyboard import InlineKeyboardBuilder

builder = InlineKeyboardBuilder()
builder.button(text='✅ Tasdiqlash', callback_data='ok')
builder.button(text='❌ Bekor qilish', callback_data='cancel')
# 2 ta tugma bir qatorda
builder.adjust(2)

kb = builder.as_markup()
```

**Izoh:**
- `button(...)` tugma qo'shadi.
- `adjust(2)` — har qatorda 2 tadan tugma joylaydi.

### ReplyKeyboardBuilder
```python
from aiogram.utils.keyboard import ReplyKeyboardBuilder

builder = ReplyKeyboardBuilder()
builder.button(text='Sozlamalar')
builder.button(text='Profil')
# Har qatorda 1 tadan
builder.adjust(1)

kb = builder.as_markup(resize_keyboard=True)
```

**Izoh:**
- `as_markup(resize_keyboard=True)` — reply keyboardni tayyorlaydi.
- Reply keyboard matnini yangilash uchun yangi xabar yuboriladi.

---
