import asyncio
import json
import os
import random
import sys
from datetime import datetime
from aiohttp import web
from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MenuButtonWebApp,
    WebAppInfo,
)

# Принудительный UTF-8 для Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

def load_config():
    if not os.path.exists(CONFIG_PATH):
        return {
            "bot_token": "8826741072:AAGZtwbqagOi7AEj9Fb_ObloLaP-hpn9H_8",
            "admin_id": None,
            "webapp_url": "https://qavalerq.github.io/apex_detail/index.html"
        }
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

config = load_config()
BOT_TOKEN = config.get("bot_token", "").strip()
ADMIN_ID = config.get("admin_id")
WEBAPP_URL = config.get("webapp_url", "").strip()

dp = Dispatcher()

def get_main_keyboard(url: str):
    if url.startswith("https://"):
        configurator_btn = InlineKeyboardButton(
            text="🏎 Студийный конфигуратор 360°",
            web_app=WebAppInfo(url=url)
        )
    else:
        configurator_btn = InlineKeyboardButton(
            text="🏎 Студийный конфигуратор 360° (Браузер)",
            url=url if url else "http://localhost:8086/index.html"
        )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [configurator_btn],
            [
                InlineKeyboardButton(text="🛡 Пакеты и гарантия", callback_data="info_packages"),
                InlineKeyboardButton(text="📍 Локация и боксы", callback_data="info_location")
            ],
            [
                InlineKeyboardButton(text="📞 Связаться со студией", callback_data="info_contact")
            ]
        ]
    )

@dp.message(CommandStart())
async def cmd_start(message: types.Message, bot: Bot):
    user_name = message.from_user.first_name or "Гость"
    print(f"[BOT] Получена команда /start от @{message.from_user.username} (ID: {message.from_user.id})")

    # Устанавливаем постоянную кнопку WebApp в левом нижнем углу Телеграма
    if WEBAPP_URL.startswith("https://"):
        try:
            await bot.set_chat_menu_button(
                chat_id=message.chat.id,
                menu_button=MenuButtonWebApp(
                    text="Конфигуратор 🏎",
                    web_app=WebAppInfo(url=WEBAPP_URL)
                )
            )
        except Exception as e:
            print(f"[!] Не удалось установить MenuButton: {e}")

    welcome_text = (
        f"💎 <b>Добро пожаловать в студию ApexDetail, {user_name}!</b>\n\n"
        f"Премиальный центр автодетейлинга и защитных покрытий в Новороссийске.\n\n"
        f"<b>Наши ключевые направления:</b>\n"
        f"• <b>Керамика 9H Pro:</b> глубокая полировка в зеркало + 2 слоя нанокерамики\n"
        f"• <b>PPF Бронь:</b> премиальный полиуретан 200 мкм от гравия и пескоструя\n"
        f"• <b>Detailing SPA:</b> деликатная химчистка кожи LeTech + озонирование\n\n"
        f"Запустите интерактивный <b>360° Конфигуратор</b> ниже, чтобы выбрать класс вашего авто, "
        f"собрать персональный пакет защиты и рассчитать смету в реальном времени:"
    )

    await message.answer(
        text=welcome_text,
        reply_markup=get_main_keyboard(WEBAPP_URL),
        parse_mode=ParseMode.HTML
    )

@dp.callback_query(F.data == "info_packages")
async def cb_packages(callback: types.CallbackQuery):
    text = (
        "🛡 <b>СТУДИЙНЫЕ СТАНДАРТЫ И ГАРАНТИЯ APEXDETAIL:</b>\n\n"
        "1. <b>Керамика 9H Pro + Полировка</b>\n"
        "• Удаление до 95% паутины, царапин и голограмм.\n"
        "• Экстремальный гидрофоб (угол капли 115°).\n"
        "• Гарантия сохранения блеска: <b>от 24 месяцев</b>.\n\n"
        "2. <b>Антигравийная пленка PPF (200 мкм)</b>\n"
        "• Топовый полиуретан с эффектом самозатягивания Top-Coat.\n"
        "• Зоны риска: капот, бампер, фары, зеркала, стойки.\n"
        "• Защита от гравия на трассе до 180 км/ч.\n\n"
        "3. <b>Интерьерный SPA-комплекс</b>\n"
        "• Деликатная паровая очистка без размокания поролона.\n"
        "• Кондиционирование премиальной косметикой LeTech.\n"
        "• Антибактериальная озонация салона и климатической системы."
    )
    await callback.message.answer(text=text, parse_mode=ParseMode.HTML)
    await callback.answer()

@dp.callback_query(F.data == "info_location")
async def cb_location(callback: types.CallbackQuery):
    text = (
        "📍 <b>ЛОКАЦИЯ И ОСНАЩЕНИЕ СТУДИИ:</b>\n\n"
        "г. Новороссийск, ул. Мира, 12 (закрытая охраняемая территория)\n"
        "⏰ Режим работы: ежедневно с 09:00 до 21:00\n\n"
        "<b>Наши рабочие залы:</b>\n"
        "• <b>Бокс №1 (Чистый зал):</b> беспылевая зона, бестеневое спектральное LED-освещение CRI 98+, нанесение керамики и PPF.\n"
        "• <b>Бокс №2 (Мокрый зал):</b> профессиональная 3-фазная мойка, химчистка, турбосушка теплым воздухом.\n\n"
        "☕ Для клиентов: лаунж-зона с кофе, мониторы видеонаблюдения за боксом."
    )
    await callback.message.answer(text=text, parse_mode=ParseMode.HTML)
    await callback.answer()

@dp.callback_query(F.data == "info_contact")
async def cb_contact(callback: types.CallbackQuery):
    text = (
        "📞 <b>КОНТАКТЫ APEXDETAIL:</b>\n\n"
        "• Телефон / WhatsApp: <code>+7 (999) 777-12-34</code>\n"
        "• Telegram старшего мастера: @qavalerq\n"
        "• Instagram: @apexdetail_nvrsk\n\n"
        "Готовы ответить на любые вопросы и согласовать нестандартный проект!"
    )
    await callback.message.answer(text=text, parse_mode=ParseMode.HTML)
    await callback.answer()

# Обработка данных из Mini App (WebApp)
@dp.message(F.web_app_data)
async def handle_webapp_data(message: types.Message, bot: Bot):
    raw_data = message.web_app_data.data
    try:
        data = json.loads(raw_data)
    except Exception:
        data = {"raw": raw_data}

    order_num = f"APX-{random.randint(1000, 9999)}"
    now_str = datetime.now().strftime("%d.%m.%Y %H:%M")

    car_class = data.get("car_class", "Не указан")
    car_model = data.get("car_model", "Не указана")
    client = data.get("client", message.from_user.first_name)
    packages = data.get("packages", [])
    addons = data.get("addons", [])
    datetime_slot = data.get("datetime", "По согласованию")
    bay = data.get("bay", "Бокс №1")
    total = data.get("total", 0)

    packages_str = "\n".join([f"  • <b>{p}</b>" for p in packages]) if packages else "  • Базовый комплекс"
    addons_str = "\n".join([f"  + {a}" for a in addons]) if addons else "  — нет"

    ticket_text = (
        f"🏁 <b>ЭЛЕКТРОННЫЙ НАРЯД-ЗАКАЗ #{order_num}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 <b>Клиент:</b> {client} (@{message.from_user.username or 'id' + str(message.from_user.id)})\n"
        f"🚗 <b>Автомобиль:</b> {car_model} ({car_class})\n"
        f"📅 <b>Дата & время заезда:</b> {datetime_slot}\n"
        f"🏢 <b>Рабочий зал:</b> {bay}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🛡 <b>Выбранные комплексы:</b>\n{packages_str}\n\n"
        f"✨ <b>Дополнительные опции:</b>\n{addons_str}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 <b>Итоговая смета:</b> <b>{total:,.0f} ₽</b>\n\n"
        f"✅ <i>Бронь зафиксирована в системе ApexDetail. Мастер свяжется с вами за 1 час до заезда. Ждем вас!</i>"
    ).replace(",", " ")

    await message.answer(text=ticket_text, parse_mode=ParseMode.HTML)

    # Уведомление администратору (если задан)
    if ADMIN_ID:
        try:
            admin_msg = (
                f"🚨 <b>НОВАЯ БРОНЬ #{order_num} В APEXDETAIL!</b>\n\n"
                f"Клиент: {client} (@{message.from_user.username})\n"
                f"Авто: {car_model} ({car_class})\n"
                f"Заезд: {datetime_slot} ({bay})\n"
                f"Сумма: <b>{total:,.0f} ₽</b>"
            ).replace(",", " ")
            await bot.send_message(chat_id=ADMIN_ID, text=admin_msg, parse_mode=ParseMode.HTML)
        except Exception as e:
            print(f"[!] Не удалось отправить уведомление админу: {e}")

async def start_web_server():
    port = int(os.environ.get("PORT", 8080))
    app = web.Application()

    async def handle_ping(request):
        return web.Response(text="ApexDetail Bot is running!")

    app.router.add_get("/", handle_ping)
    app.router.add_get("/health", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f" Web Health-Check запущен на порту {port}")

async def main():
    if not BOT_TOKEN:
        print("[!] ОШИБКА: bot_token не указан в config.json!")
        return

    bot = Bot(token=BOT_TOKEN)
    me = await bot.get_me()
    print("=" * 50)
    print(f" ApexDetail Bot запущен: @{me.username} ({me.first_name})")
    print(f" WebApp URL: {WEBAPP_URL}")
    print(" Бот слушает команды и заказы через Telegram Mini App...")
    print("=" * 50)

    try:
        await start_web_server()
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\nApexDetail Bot остановлен.")
