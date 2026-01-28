import asyncio
import logging
import sqlite3
import os
import datetime
import html
import io
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import BusinessMessagesDeleted, BusinessConnection, FSInputFile, BufferedInputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from conf import BOT_TOKEN, ADMIN_ID, BASE_USERS_DIR, MASTER_DB_FILE, TRANSLATIONS, DEFAULT_LANG

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

LANG_CACHE = {}

MSG_KEYS = [
    "text", "voice", "video_note", "photo", "video", 
    "audio", "sticker", "animation", "other"
]

class AdminStates(StatesGroup):
    waiting_for_broadcast = State()

def get_lang(user_id):
    if user_id in LANG_CACHE:
        return LANG_CACHE[user_id]
        
    try:
        db_path = get_user_db_path(user_id)
        if not os.path.exists(db_path):
            return DEFAULT_LANG
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.execute("SELECT value FROM settings WHERE key = 'language'")
            row = cursor.fetchone()
            if row:
                lang = str(row[0])
                if lang in TRANSLATIONS:
                    LANG_CACHE[user_id] = lang
                    return lang
    except Exception:
        pass
    
    LANG_CACHE[user_id] = DEFAULT_LANG
    return DEFAULT_LANG

def t(user_id, key):
    lang = get_lang(user_id)
    return TRANSLATIONS[lang].get(key, f"<{key}>")

def get_msg_type_name(user_id, msg_type_key):
    return t(user_id, f"msg_{msg_type_key}")


def ensure_dirs():
    if not os.path.exists(BASE_USERS_DIR):
        os.makedirs(BASE_USERS_DIR)

def init_master_db():
    with sqlite3.connect(MASTER_DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS connections (
                connection_id TEXT PRIMARY KEY,
                user_chat_id INTEGER
            )
        """)
        conn.commit()

def get_user_db_path(user_id):
    user_dir = os.path.join(BASE_USERS_DIR, str(user_id))
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    return os.path.join(user_dir, "user_data.db")

def get_history_db_path(user_id):
    user_dir = os.path.join(BASE_USERS_DIR, str(user_id))
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    return os.path.join(user_dir, "full_history.db")

def init_user_db(user_id):
    db_path = get_user_db_path(user_id)
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS active_messages (
                key_id TEXT PRIMARY KEY,
                msg_type TEXT,
                content TEXT,
                caption TEXT,
                author_name TEXT,
                author_username TEXT,
                chat_title TEXT,
                date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS archive_deleted (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                msg_type TEXT,
                content TEXT,
                caption TEXT,
                author_name TEXT,
                author_username TEXT,
                chat_title TEXT,
                date_deleted TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value INTEGER
            )
        """)
        conn.commit()
    
    hist_path = get_history_db_path(user_id)
    with sqlite3.connect(hist_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS history_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                direction TEXT,
                date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                chat_title TEXT,
                sender_name TEXT,
                sender_username TEXT,
                msg_type TEXT,
                content TEXT,
                caption TEXT
            )
        """)
        conn.commit()

async def download_and_send_file(chat_id, file_id, filename, caption):
    try:
        file_info = await bot.get_file(file_id)
        file_io = io.BytesIO()
        await bot.download_file(file_info.file_path, destination=file_io)
        file_io.seek(0)
        input_file = BufferedInputFile(file_io.read(), filename=filename)
        await bot.send_document(chat_id=chat_id, document=input_file, caption=caption, parse_mode="HTML")
        return True
    except Exception as e:
        print(f"❌ Error downloading file: {e}")
        try:
            await bot.send_document(chat_id, document=file_id, caption=caption, parse_mode="HTML")
        except:
            pass
        return False


@dp.business_connection()
async def on_business_connection(event: BusinessConnection):
    with sqlite3.connect(MASTER_DB_FILE) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO connections (connection_id, user_chat_id) VALUES (?, ?)",
            (event.id, event.user_chat_id)
        )
        conn.commit()
    
    init_user_db(event.user_chat_id)

    if event.is_enabled:
        try:
            await bot.send_message(
                chat_id=event.user_chat_id,
                text=TRANSLATIONS[DEFAULT_LANG]["connect_success"],
                parse_mode="HTML"
            )
        except:
            pass

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id

    is_authorized = False
    try:
        with sqlite3.connect(MASTER_DB_FILE) as conn:
            cursor = conn.execute("SELECT 1 FROM connections WHERE user_chat_id = ?", (user_id,))
            if cursor.fetchone():
                is_authorized = True
    except Exception: pass 

    if not is_authorized:
        u_lang = message.from_user.language_code
        if u_lang not in TRANSLATIONS: u_lang = DEFAULT_LANG
        await message.answer(TRANSLATIONS[u_lang]["access_denied"], parse_mode="HTML")
        return

    init_user_db(user_id)
    db_path = get_user_db_path(user_id)

    lang_set = False
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute("SELECT value FROM settings WHERE key = 'language'")
        if cursor.fetchone(): lang_set = True

    if not lang_set:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="setlang_ru"),
                InlineKeyboardButton(text="🇺🇸 English", callback_data="setlang_en"),
                InlineKeyboardButton(text="🇺🇦 Українська", callback_data="setlang_uk")
            ]
        ])
        await message.answer(TRANSLATIONS[DEFAULT_LANG]["lang_select"], reply_markup=kb, parse_mode="HTML")
        return

    archive_count = 0
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute("SELECT COUNT(*) FROM archive_deleted")
        archive_count = cursor.fetchone()[0]

    keyboard = [
        [InlineKeyboardButton(text=t(user_id, "btn_settings"), callback_data="open_settings")],
        [InlineKeyboardButton(text=t(user_id, "btn_export_deleted"), callback_data="export_deleted")],
        [InlineKeyboardButton(text=t(user_id, "btn_export_full"), callback_data="export_full")],
        [
            InlineKeyboardButton(text=t(user_id, "btn_lang"), callback_data="change_lang"),
            InlineKeyboardButton(text=t(user_id, "btn_emergency"), callback_data="emergency_ask")
        ]
    ]

    text = (
        f"{t(user_id, 'stats_header')}\n"
        f"{t(user_id, 'stats_count')} <b>{archive_count}</b>\n\n"
        f"{t(user_id, 'connect_success')}" 
    )

    try:
        if isinstance(message, types.CallbackQuery):
             await message.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard), parse_mode="HTML")
        else:
             await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard), parse_mode="HTML")
    except:
        await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard), parse_mode="HTML")

@dp.callback_query(F.data == "back_to_main")
async def back_to_main_menu(callback: CallbackQuery):
    await cmd_start(callback)

@dp.callback_query(F.data == "change_lang")
async def ask_change_lang(callback: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="setlang_ru"),
            InlineKeyboardButton(text="🇺🇸 English", callback_data="setlang_en"),
            InlineKeyboardButton(text="🇺🇦 Українська", callback_data="setlang_uk")
        ],
        [InlineKeyboardButton(text=t(callback.from_user.id, "btn_cancel"), callback_data="cancel_lang")]
    ])
    await callback.message.edit_text(t(callback.from_user.id, "lang_select"), reply_markup=kb, parse_mode="HTML")

@dp.callback_query(F.data == "cancel_lang")
async def cancel_lang_change(callback: CallbackQuery):
    await callback.message.delete()
    await cmd_start(callback.message)

@dp.callback_query(F.data.startswith("setlang_"))
async def set_language(callback: CallbackQuery):
    user_id = callback.from_user.id
    new_lang = callback.data.split("_")[1]
    
    LANG_CACHE[user_id] = new_lang
    
    db_path = get_user_db_path(user_id)
    with sqlite3.connect(db_path) as conn:
        conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('language', ?)", (new_lang,))
        conn.commit()
    
    await callback.answer(f"Language set to {new_lang}")
    await callback.message.delete()
    await cmd_start(callback.message)


@dp.callback_query(F.data == "open_settings")
async def open_settings_menu(callback: CallbackQuery):
    await render_settings_menu(callback)

@dp.callback_query(F.data.startswith("toggle_"))
async def on_toggle_setting(callback: CallbackQuery):
    user_id = callback.from_user.id
    msg_type = callback.data.split("_", 1)[1]
    db_path = get_user_db_path(user_id)
    
    with sqlite3.connect(db_path) as conn:
        key_db = "notify_edit" if msg_type == "notify_edit" else msg_type
        cursor = conn.execute("SELECT value FROM settings WHERE key = ?", (key_db,))
        row = cursor.fetchone()
        current_value = row[0] if row is not None else 1
        new_value = 0 if current_value else 1
        conn.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key_db, new_value))
        conn.commit()
    
    await render_settings_menu(callback)


async def render_settings_menu(callback: CallbackQuery):
    user_id = callback.from_user.id
    db_path = get_user_db_path(user_id)

    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute("SELECT key, value FROM settings")
        rows = cursor.fetchall()
        db_settings = {row[0]: row[1] for row in rows}

    keyboard = []
    row = []

    for m_key in MSG_KEYS:
        if m_key == "other": continue
        val = db_settings.get(m_key)
        is_enabled = bool(val) if val is not None else True
        status_icon = "✅" if is_enabled else "❌"
        title = get_msg_type_name(user_id, m_key)
        
        row.append(InlineKeyboardButton(text=f"{status_icon} {title}", callback_data=f"toggle_{m_key}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row: keyboard.append(row)
    
    val_edit = db_settings.get("notify_edit")
    is_edit = bool(val_edit) if val_edit is not None else True
    icon_edit = "✅" if is_edit else "❌"
    keyboard.append([InlineKeyboardButton(
        text=f"{icon_edit} {t(user_id, 'btn_toggle_edit')}", 
        callback_data="toggle_notify_edit"
    )])

    keyboard.append([InlineKeyboardButton(text=t(user_id, "btn_back"), callback_data="back_to_main")])

    text = t(user_id, 'settings_header')
    
    try:
        await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard), parse_mode="HTML")
    except TelegramBadRequest: 
        await callback.answer()


@dp.callback_query(F.data == "emergency_ask")
async def ask_emergency_delete(callback: CallbackQuery):
    user_id = callback.from_user.id
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(user_id, "btn_confirm_delete"), callback_data="emergency_confirm")],
        [InlineKeyboardButton(text=t(user_id, "btn_cancel"), callback_data="emergency_cancel")]
    ])
    await callback.message.edit_text(
        t(user_id, "emergency_warning"),
        reply_markup=kb,
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "emergency_cancel")
async def cancel_emergency(callback: CallbackQuery):
    await callback.answer(t(callback.from_user.id, "emergency_cancel"))
    await callback.message.delete()
    await cmd_start(callback.message)

@dp.callback_query(F.data == "emergency_confirm")
async def perform_emergency_delete(callback: CallbackQuery):
    user_id = callback.from_user.id
    
    u_path = get_user_db_path(user_id)
    with sqlite3.connect(u_path) as conn:
        conn.execute("DELETE FROM active_messages")
        conn.execute("DELETE FROM archive_deleted")
        conn.commit()
        
    h_path = get_history_db_path(user_id)
    with sqlite3.connect(h_path) as conn:
        conn.execute("DELETE FROM history_log")
        conn.commit()

    await callback.answer("DONE", show_alert=True)
    await callback.message.edit_text(t(user_id, "emergency_done"), parse_mode="HTML")


@dp.message(Command("admin"))
async def cmd_admin(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    user_id = message.from_user.id
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(user_id, "btn_admin_broadcast"), callback_data="admin_broadcast")],
        [InlineKeyboardButton(text=t(user_id, "btn_close"), callback_data="admin_close")]
    ])
    
    user_count = 0
    try:
        with sqlite3.connect(MASTER_DB_FILE) as conn:
            cursor = conn.execute("SELECT COUNT(DISTINCT user_chat_id) FROM connections")
            user_count = cursor.fetchone()[0]
    except: pass

    await message.answer(
        f"{t(user_id, 'admin_panel')}\n\n{t(user_id, 'users_count')} <b>{user_count}</b>",
        reply_markup=kb,
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "admin_close")
async def admin_close(callback: CallbackQuery):
    await callback.message.delete()

@dp.callback_query(F.data == "admin_broadcast")
async def admin_start_broadcast(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    await callback.message.edit_text(t(user_id, "broadcast_prompt"), parse_mode="HTML")
    await state.set_state(AdminStates.waiting_for_broadcast)

@dp.message(AdminStates.waiting_for_broadcast)
async def process_broadcast(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    txt = message.text.lower() if message.text else ""
    if txt in ["отмена", "cancel", "відміна"]:
        await state.clear()
        await message.answer(t(user_id, "broadcast_cancel"))
        await cmd_admin(message)
        return

    users = []
    try:
        with sqlite3.connect(MASTER_DB_FILE) as conn:
            cursor = conn.execute("SELECT DISTINCT user_chat_id FROM connections")
            users = [row[0] for row in cursor.fetchall()]
    except Exception:
        await state.clear()
        return

    success = 0
    blocked = 0
    
    for uid in users:
        try:
            await message.copy_to(chat_id=uid)
            success += 1
            await asyncio.sleep(0.05)
        except Exception:
            blocked += 1
    
    stats_msg = t(user_id, "broadcast_stats").format(success=success, blocked=blocked)
    await message.answer(
        f"{t(user_id, 'broadcast_done')}\n{stats_msg}",
        parse_mode="HTML"
    )
    await state.clear()


@dp.callback_query(F.data == "export_deleted")
async def on_export_deleted_btn(callback: CallbackQuery):
    await callback.answer()
    await cmd_export(callback.message)

@dp.callback_query(F.data == "export_full")
async def on_export_full_btn(callback: CallbackQuery):
    await callback.answer()
    await cmd_export_all(callback.message)

@dp.message(Command("export"))
async def cmd_export(message: types.Message):
    user_id = message.chat.id
    db_path = get_user_db_path(user_id)
    if not os.path.exists(db_path):
        await bot.send_message(user_id, t(user_id, "export_no_data"))
        return
    
    report_path = f"deleted_{user_id}.txt"
    try:
        with sqlite3.connect(db_path) as conn:
            rows = conn.execute("SELECT date_deleted, author_name, msg_type, content, caption, chat_title FROM archive_deleted ORDER BY date_deleted DESC").fetchall()
        
        if not rows:
            await bot.send_message(user_id, t(user_id, "export_empty"))
            return

        with open(report_path, "w", encoding="utf-8") as f:
            f.write(t(user_id, "export_deleted_title") + "\n")
            f.write("=========================================\n\n")
            for r in rows:
                date, author, m_type, content, caption, chat = r
                
                readable_type = get_msg_type_name(user_id, m_type)
                readable_content = content if m_type == "text" else t(user_id, "txt_media_file")
                
                txt_date = t(user_id, "txt_date")
                txt_chat = t(user_id, "txt_chat")
                txt_from = t(user_id, "txt_from")
                txt_type = t(user_id, "txt_type")
                txt_cont = t(user_id, "txt_content")
                txt_capt = t(user_id, "txt_caption")
                
                f.write(f"{txt_date} {date}\n{txt_chat} {chat}\n{txt_from} {author}\n{txt_type} {readable_type}\n{txt_cont} {readable_content}\n")
                if caption: f.write(f"{txt_capt} {caption}\n")
                f.write("-" * 40 + "\n\n")
        
        await bot.send_document(user_id, document=FSInputFile(report_path), caption=t(user_id, "export_caption_del"))
        os.remove(report_path)
    except Exception as e:
        await bot.send_message(user_id, f"Error: {e}")

@dp.message(Command("export_all"))
async def cmd_export_all(message: types.Message):
    user_id = message.chat.id
    db_path = get_history_db_path(user_id)
    if not os.path.exists(db_path):
        await bot.send_message(user_id, t(user_id, "export_no_data"))
        return

    report_path = f"full_{user_id}.txt"
    try:

        rows = []
        with sqlite3.connect(db_path) as conn:
            cursor = conn.execute("SELECT date_time, direction, sender_name, msg_type, content, caption, chat_title FROM history_log ORDER BY date_time ASC")
            rows = cursor.fetchall()
        
        if not rows:
            await bot.send_message(user_id, t(user_id, "export_empty"))
            return


        with open(report_path, "w", encoding="utf-8") as f:
            f.write(t(user_id, "export_full_title") + "\n")
            f.write("="*40 + "\n\n")
            for r in rows:
                date, direction, author, m_type, content, caption, chat = r
                readable_type = get_msg_type_name(user_id, m_type)
                dir_arrow = t(user_id, "txt_incoming") if direction == "incoming" else t(user_id, "txt_outgoing")
                readable_content = content if m_type == "text" else t(user_id, "txt_media_file")

                txt_chat = t(user_id, "txt_chat")
                txt_from = t(user_id, "txt_from")
                txt_type = t(user_id, "txt_type")
                txt_cont = t(user_id, "txt_content")
                txt_capt = t(user_id, "txt_caption")

                f.write(f"[{date}] {dir_arrow}\n{txt_chat} {chat}\n{txt_from} {author}\n{txt_type} {readable_type}\n{txt_cont} {readable_content}\n")
                if caption: f.write(f"{txt_capt} {caption}\n")
                f.write("-" * 40 + "\n\n")


        document = FSInputFile(report_path)
        await bot.send_document(user_id, document=document, caption=t(user_id, "export_caption_full"))
        

        if os.path.exists(report_path):
            os.remove(report_path)

    except Exception as e:
        logging.error(f"Export error: {e}")
        await bot.send_message(user_id, f"Error: {e}")


@dp.business_message()
async def log_message(message: types.Message):
    owner_id = None
    with sqlite3.connect(MASTER_DB_FILE) as conn:
        cursor = conn.execute("SELECT user_chat_id FROM connections WHERE connection_id = ?", (message.business_connection_id,))
        row = cursor.fetchone()
        if row: owner_id = row[0]
    if not owner_id: return

    msg_type = "unknown"
    content = ""
    caption = message.caption or ""

    if message.text:
        msg_type = "text"
        content = message.text
    elif message.voice:
        msg_type = "voice"
        content = message.voice.file_id
    elif message.audio:
        msg_type = "audio"
        content = message.audio.file_id
    elif message.video_note:
        msg_type = "video_note"
        content = message.video_note.file_id
    elif message.photo:
        msg_type = "photo"
        content = message.photo[-1].file_id
    elif message.video:
        msg_type = "video"
        content = message.video.file_id
    elif message.sticker:
        msg_type = "sticker"
        content = message.sticker.file_id
    elif message.animation:
        msg_type = "animation"
        content = message.animation.file_id
    else:
        msg_type = "other"
        content = "[File]"

    key = f"{message.business_connection_id}:{message.message_id}"
    author_name = message.from_user.full_name
    author_username = f"@{message.from_user.username}" if message.from_user.username else "No Username"
    chat_title = message.chat.title or message.chat.full_name
    direction = "incoming"
    if message.from_user.id == owner_id: direction = "outgoing"

    init_user_db(owner_id)
    if msg_type != "other":
        try:
            with sqlite3.connect(get_user_db_path(owner_id)) as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO active_messages (key_id, msg_type, content, caption, author_name, author_username, chat_title) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (key, msg_type, content, caption, author_name, author_username, chat_title)
                )
                conn.commit()
        except Exception: pass

    try:
        with sqlite3.connect(get_history_db_path(owner_id)) as conn:
            conn.execute(
                "INSERT INTO history_log (direction, chat_title, sender_name, sender_username, msg_type, content, caption) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (direction, chat_title, author_name, author_username, msg_type, content, caption)
            )
            conn.commit()
    except Exception: pass

@dp.edited_business_message()
async def handle_edited(message: types.Message):
    owner_id = None
    with sqlite3.connect(MASTER_DB_FILE) as conn:
        cursor = conn.execute("SELECT user_chat_id FROM connections WHERE connection_id = ?", (message.business_connection_id,))
        row = cursor.fetchone()
        if row: owner_id = row[0]
    if not owner_id: return

    key = f"{message.business_connection_id}:{message.message_id}"
    user_db_path = get_user_db_path(owner_id)

    try:
        with sqlite3.connect(user_db_path) as conn:
            cursor = conn.execute("SELECT msg_type, content, caption, author_name, author_username, chat_title FROM active_messages WHERE key_id = ?", (key,))
            data = cursor.fetchone()

            if data:
                msg_type, old_content, old_caption, author_name, author_username, chat_title = data
                
                cursor_setting = conn.execute("SELECT value FROM settings WHERE key = ?", (msg_type,))
                row_setting = cursor_setting.fetchone()
                is_type_enabled = bool(row_setting[0]) if row_setting is not None else True

                cursor_edit = conn.execute("SELECT value FROM settings WHERE key = 'notify_edit'")
                row_edit = cursor_edit.fetchone()
                is_edit_enabled = bool(row_edit[0]) if row_edit is not None else True

                old_text = ""
                new_text = ""
                has_changes = False

                if msg_type == "text":
                    old_text = old_content
                    new_text = message.text or ""
                    if old_text != new_text:
                        has_changes = True
                
                elif msg_type in ["photo", "video", "document", "audio", "voice"]:
                    old_text = old_caption or ""
                    new_text = message.caption or ""
                    if old_text != new_text:
                        has_changes = True

                if has_changes and is_type_enabled and is_edit_enabled:
                    curr_time = datetime.datetime.now().strftime("%H:%M")
                    safe_author = html.escape(author_name)
                    safe_username = html.escape(author_username)
                    safe_chat = html.escape(chat_title)
                    
                    safe_old = html.escape(old_text)
                    safe_new = html.escape(new_text)

                    text_report = (
                        f"<blockquote><b>Сообщение изменено</b> | {curr_time}\n"
                        f"<b>От:</b> {safe_author} (<code>{safe_username}</code>)\n"
                        f"<b>Чат:</b> {safe_chat}\n"
                        f"<b>Было:</b> <tg-spoiler>{safe_old}</tg-spoiler></blockquote>\n\n"
                        f"<b>Стало:</b>\n{safe_new}"
                    )
                    
                    try:
                        await bot.send_message(owner_id, text_report, parse_mode="HTML")
                    except Exception:
                        pass

                if msg_type == "text":
                    conn.execute("UPDATE active_messages SET content = ? WHERE key_id = ?", (new_text, key))
                else:
                    conn.execute("UPDATE active_messages SET caption = ? WHERE key_id = ?", (new_text, key))
                
                conn.commit()

    except Exception as e:
        print(f"Edit Handle Error: {e}")

@dp.deleted_business_messages()
async def handle_deleted(event: BusinessMessagesDeleted):
    owner_id = None
    with sqlite3.connect(MASTER_DB_FILE) as conn:
        cursor = conn.execute("SELECT user_chat_id FROM connections WHERE connection_id = ?", (event.business_connection_id,))
        row = cursor.fetchone()
        if row: owner_id = row[0]
    if not owner_id: return

    user_db_path = get_user_db_path(owner_id)
    try:
        with sqlite3.connect(user_db_path) as conn:
            for msg_id in event.message_ids:
                key = f"{event.business_connection_id}:{msg_id}"
                cursor = conn.execute("SELECT msg_type, content, caption, author_name, author_username, chat_title FROM active_messages WHERE key_id = ?", (key,))
                data = cursor.fetchone()

                if data:
                    msg_type, content, caption, author_name, author_username, chat_title = data
                    cursor_setting = conn.execute("SELECT value FROM settings WHERE key = ?", (msg_type,))
                    row_setting = cursor_setting.fetchone()
                    is_enabled = bool(row_setting[0]) if row_setting is not None else True

                    if is_enabled:
                        curr_time = datetime.datetime.now().strftime("%H:%M")
                        safe_author = html.escape(author_name)
                        safe_username = html.escape(author_username)
                        safe_chat = html.escape(chat_title)
                        safe_caption = html.escape(caption) if caption else ""

                        header = (
                            f"<blockquote><b>Сообщение удалено</b> | {curr_time}\n"
                            f"<b>От:</b> {safe_author} (<code>{safe_username}</code>)\n"
                            f"<b>Чат:</b> {safe_chat}</blockquote>"
                        )

                        full_caption = f"{header}\n\n<b>Подпись:</b>\n{safe_caption}" if safe_caption else header

                        try:
                            if msg_type == "text":
                                await bot.send_message(owner_id, f"{header}\n\n<b>Текст:</b>\n{html.escape(content)}", parse_mode="HTML")
                            
                            elif msg_type == "voice":
                                try:
                                    await bot.send_voice(owner_id, voice=content, caption=header, parse_mode="HTML")
                                except:
                                    await bot.send_message(owner_id, f"{header}\n\n⚠️ Ошибка голосового, файл ниже:", parse_mode="HTML")
                                    await download_and_send_file(owner_id, content, "voice.ogg", header)
                            
                            elif msg_type == "audio":
                                await bot.send_audio(owner_id, audio=content, caption=header, parse_mode="HTML")
                            
                            elif msg_type == "video_note":
                                await bot.send_message(owner_id, f"{header}\n<i>(Видеосообщение ниже)</i>", parse_mode="HTML")
                                try:
                                    await bot.send_video_note(owner_id, video_note=content)
                                except:
                                    await bot.send_message(owner_id, "⚠️ Ошибка кружочка, файл:", parse_mode="HTML")
                                    await download_and_send_file(owner_id, content, "circle.mp4", "(Файл)")
                            
                            elif msg_type == "photo":
                                await bot.send_photo(owner_id, photo=content, caption=full_caption, parse_mode="HTML")
                            
                            elif msg_type == "video":
                                await bot.send_video(owner_id, video=content, caption=full_caption, parse_mode="HTML")
                            
                            elif msg_type == "sticker":
                                await bot.send_message(owner_id, f"{header}\n<i>(Стикер ниже)</i>", parse_mode="HTML")
                                await bot.send_sticker(owner_id, sticker=content)
                            
                            elif msg_type == "animation":
                                await bot.send_animation(owner_id, animation=content, caption=full_caption, parse_mode="HTML")
                        
                        except Exception as e:
                            try: await bot.send_message(owner_id, f"⚠️ Ошибка восстановления: {html.escape(str(e))}", parse_mode="HTML")
                            except: pass
                    
                    conn.execute("INSERT INTO archive_deleted (msg_type, content, caption, author_name, author_username, chat_title) VALUES (?, ?, ?, ?, ?, ?)", (msg_type, content, caption, author_name, author_username, chat_title))
                    conn.execute("DELETE FROM active_messages WHERE key_id = ?", (key,))
                    conn.commit()
    except sqlite3.Error as e: print(f"DB Error: {e}")

async def main():
    ensure_dirs()
    init_master_db()
    await bot.delete_webhook(drop_pending_updates=True)
    print("Bot started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")