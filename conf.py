BOT_TOKEN = "YOUR_BOT_TOKEN_FROM_BOTFATHER"
ADMIN_ID = 
BASE_USERS_DIR = "users"
MASTER_DB_FILE = "master.db"

LANGUAGES = ["ru", "en", "uk"]
DEFAULT_LANG = "ru"

TRANSLATIONS = {
    "ru": {
        "msg_text": "📝 Текст",
        "msg_voice": "🗣 Голосовое",
        "msg_video_note": "🔵 Кружок",
        "msg_photo": "🖼 Фото",
        "msg_video": "🎬 Видео",
        "msg_audio": "🎵 Аудио",
        "msg_sticker": "🎭 Стикер",
        "msg_animation": "👾 Гифка",
        "msg_other": "❓ Другое",
        
        "btn_export_deleted": "📥 Скачать удаленные",
        "btn_export_full": "📚 Скачать всю историю",
        "btn_emergency": "🚨 Экстренное удаление",
        "btn_lang": "🌍 Язык / Language / Мова",
        "btn_cancel": "🔙 Отмена",
        "btn_confirm_delete": "💣 ДА, УДАЛИТЬ ВСЁ",
        "btn_admin_broadcast": "📢 Рассылка",
        "btn_close": "❌ Закрыть",

        "connect_success": "✅ <b>Бот подключен!</b>\nВведите /start для настройки.",
        
        "access_denied": "🔒 <b>Доступ закрыт</b>\n\nМеню настроек доступно только владельцу подключения.\nПерейдите в <b>Настройки ➝ Telegram для бизнеса ➝ Чат-боты</b> и добавьте этого бота.",

        "stats_header": "📊 <b>Статистика архива</b>",
        "stats_count": "Сообщений в базе удаленных:",
        "settings_header": "⚙️ <b>Настройки уведомлений</b>\nНажмите, чтобы включить/выключить уведомления:",
        
        "emergency_warning": "🚨 <b>ВНИМАНИЕ! ЭКСТРЕННОЕ УДАЛЕНИЕ</b>\n\nВы собираетесь удалить:\n• Архив удаленных\n• Историю переписки\n• Активные сообщения\n\n<b>Это необратимо!</b>",
        "emergency_done": "✅ <b>Успешно очищено.</b>\nВсе данные удалены.",
        "emergency_cancel": "Отменено.",

        "admin_panel": "👨‍💻 <b>Админ-панель</b>",
        "users_count": "Пользователей:",
        "broadcast_prompt": "📢 <b>Рассылка</b>\nОтправьте сообщение для рассылки всем пользователям.\nНапишите 'отмена' для выхода.",
        "broadcast_cancel": "Рассылка отменена.",
        "broadcast_done": "✅ <b>Рассылка завершена!</b>",
        "broadcast_stats": "Доставлено: {success}\nОшибок: {blocked}",

        "export_no_data": "Нет данных.",
        "export_empty": "Архив пуст.",
        "export_deleted_title": "АРХИВ УДАЛЕННЫХ СООБЩЕНИЙ",
        "export_full_title": "ПОЛНАЯ ИСТОРИЯ ПЕРЕПИСКИ",
        "export_caption_del": "📂 Ваш архив удаленных сообщений",
        "export_caption_full": "📚 Полная история переписки",
        
        "report_deleted": "🛑 <b>Сообщение удалено</b>",
        "report_from": "👤 <b>От:</b>",
        "report_chat": "📍 <b>Чат:</b>",
        "report_caption": "📝 <b>Подпись:</b>",
        "report_text": "📃 <b>Текст:</b>",
        "report_circle": "<i>(Кружок ниже)</i>",
        "report_sticker": "<i>(Стикер ниже)</i>",
        
        "err_voice": "⚠️ <b>Ограничение голосовых.</b>\n🔄 <i>Отправляю файлом...</i>",
        "err_video_note": "⚠️ <b>Ограничение видеосообщений.</b>\n🔄 <i>Отправляю файлом...</i>",
        "err_file_restored": "(Файл)",
        "err_generic": "⚠️ Ошибка восстановления:",
        
        "txt_date": "⏰ Дата:",
        "txt_chat": "📍 Чат:",
        "txt_from": "👤 От:",
        "txt_type": "📎 Тип:",
        "txt_content": "💬 Содержание:",
        "txt_caption": "🏷 Подпись:",
        "txt_incoming": "📥 ВХОДЯЩЕЕ",
        "txt_outgoing": "📤 ИСХОДЯЩЕЕ",
        "txt_media_file": "[Медиа-файл]",
        
        "lang_select": "🌍 <b>Выберите язык / Select Language / Оберіть мову</b>"
    },
    "en": {
        "msg_text": "📝 Text",
        "msg_voice": "🗣 Voice",
        "msg_video_note": "🔵 Video Note",
        "msg_photo": "🖼 Photo",
        "msg_video": "🎬 Video",
        "msg_audio": "🎵 Audio",
        "msg_sticker": "🎭 Sticker",
        "msg_animation": "👾 Gif",
        "msg_other": "❓ Other",
        
        "btn_export_deleted": "📥 Download Deleted",
        "btn_export_full": "📚 Download History",
        "btn_emergency": "🚨 Emergency Delete",
        "btn_lang": "🌍 Language",
        "btn_cancel": "🔙 Cancel",
        "btn_confirm_delete": "💣 YES, DELETE ALL",
        "btn_admin_broadcast": "📢 Broadcast",
        "btn_close": "❌ Close",

        "connect_success": "✅ <b>Bot connected!</b>\nType /start to configure.",
        
        "access_denied": "🔒 <b>Access Denied</b>\n\nThe settings menu is available only to the connection owner.\nGo to <b>Settings ➝ Telegram Business ➝ Chat Bots</b> and add this bot.",

        "stats_header": "📊 <b>Archive Statistics</b>",
        "stats_count": "Messages in deleted archive:",
        "settings_header": "⚙️ <b>Notification Settings</b>\nTap to toggle notifications:",
        
        "emergency_warning": "🚨 <b>WARNING! EMERGENCY DELETE</b>\n\nYou are about to wipe:\n• Deleted archive\n• Chat history\n• Active messages\n\n<b>Irreversible!</b>",
        "emergency_done": "✅ <b>Wiped successfully.</b>\nAll data deleted.",
        "emergency_cancel": "Cancelled.",

        "admin_panel": "👨‍💻 <b>Admin Panel</b>",
        "users_count": "Users:",
        "broadcast_prompt": "📢 <b>Broadcast</b>\nSend a message to broadcast to all users.\nType 'cancel' to exit.",
        "broadcast_cancel": "Broadcast cancelled.",
        "broadcast_done": "✅ <b>Broadcast finished!</b>",
        "broadcast_stats": "Delivered: {success}\nFailed: {blocked}",

        "export_no_data": "No data found.",
        "export_empty": "Archive is empty.",
        "export_deleted_title": "DELETED MESSAGES ARCHIVE",
        "export_full_title": "FULL CHAT HISTORY",
        "export_caption_del": "📂 Your deleted messages archive",
        "export_caption_full": "📚 Full chat history",
        
        "report_deleted": "🛑 <b>Message Deleted</b>",
        "report_from": "👤 <b>From:</b>",
        "report_chat": "📍 <b>Chat:</b>",
        "report_caption": "📝 <b>Caption:</b>",
        "report_text": "📃 <b>Text:</b>",
        "report_circle": "<i>(Video note below)</i>",
        "report_sticker": "<i>(Sticker below)</i>",
        
        "err_voice": "⚠️ <b>Voice restricted.</b>\n🔄 <i>Sending as file...</i>",
        "err_video_note": "⚠️ <b>Video note restricted.</b>\n🔄 <i>Sending as file...</i>",
        "err_file_restored": "(File)",
        "err_generic": "⚠️ Restore error:",
        
        "txt_date": "⏰ Date:",
        "txt_chat": "📍 Chat:",
        "txt_from": "👤 From:",
        "txt_type": "📎 Type:",
        "txt_content": "💬 Content:",
        "txt_caption": "🏷 Caption:",
        "txt_incoming": "📥 INCOMING",
        "txt_outgoing": "📤 OUTGOING",
        "txt_media_file": "[Media File]",
        
        "lang_select": "🌍 <b>Select Language</b>"
    },
    "uk": {
        "msg_text": "📝 Текст",
        "msg_voice": "🗣 Голосове",
        "msg_video_note": "🔵 Кружечок",
        "msg_photo": "🖼 Фото",
        "msg_video": "🎬 Відео",
        "msg_audio": "🎵 Аудіо",
        "msg_sticker": "🎭 Стікер",
        "msg_animation": "👾 Гіфка",
        "msg_other": "❓ Інше",
        
        "btn_export_deleted": "📥 Скачати видалені",
        "btn_export_full": "📚 Скачати всю історію",
        "btn_emergency": "🚨 Екстрене видалення",
        "btn_lang": "🌍 Мова",
        "btn_cancel": "🔙 Скасувати",
        "btn_confirm_delete": "💣 ТАК, ВИДАЛИТИ ВСЕ",
        "btn_admin_broadcast": "📢 Розсилка",
        "btn_close": "❌ Закрити",

        "connect_success": "✅ <b>Бот підключений!</b>\nВведіть /start для налаштування.",

        "access_denied": "🔒 <b>Доступ заборонено</b>\n\nМеню налаштувань доступне тільки власнику підключення.\nПерейдіть в <b>Налаштування ➝ Telegram для бізнесу ➝ Чат-боти</b> та додайте цього бота.",

        "stats_header": "📊 <b>Статистика архіву</b>",
        "stats_count": "Повідомлень у базі видалених:",
        "settings_header": "⚙️ <b>Налаштування сповіщень</b>\nНатисніть, щоб увімкнути/вимкнути сповіщення:",
        
        "emergency_warning": "🚨 <b>УВАГА! ЕКСТРЕНЕ ВИДАЛЕННЯ</b>\n\nВи збираєтесь видалити:\n• Архів видалених\n• Історію листування\n• Активні повідомлення\n\n<b>Це незворотно!</b>",
        "emergency_done": "✅ <b>Успішно очищено.</b>\nВсі дані видалено.",
        "emergency_cancel": "Скасовано.",

        "admin_panel": "👨‍💻 <b>Адмін-панель</b>",
        "users_count": "Користувачів:",
        "broadcast_prompt": "📢 <b>Розсилка</b>\nНадішліть повідомлення для розсилки всім користувачам.\nНапишіть 'відміна' для виходу.",
        "broadcast_cancel": "Розсилку скасовано.",
        "broadcast_done": "✅ <b>Розсилка завершена!</b>",
        "broadcast_stats": "Доставлено: {success}\nПомилок: {blocked}",

        "export_no_data": "Немає даних.",
        "export_empty": "Архів порожній.",
        "export_deleted_title": "АРХІВ ВИДАЛЕНИХ ПОВІДОМЛЕНЬ",
        "export_full_title": "ПОВНА ІСТОРІЯ ЛИСТУВАННЯ",
        "export_caption_del": "📂 Ваш архів видалених повідомлень",
        "export_caption_full": "📚 Повна історія листування",
        
        "report_deleted": "🛑 <b>Повідомлення видалено</b>",
        "report_from": "👤 <b>Від:</b>",
        "report_chat": "📍 <b>Чат:</b>",
        "report_caption": "📝 <b>Підпис:</b>",
        "report_text": "📃 <b>Текст:</b>",
        "report_circle": "<i>(Кружечок нижче)</i>",
        "report_sticker": "<i>(Стікер нижче)</i>",
        
        "err_voice": "⚠️ <b>Обмеження голосових.</b>\n🔄 <i>Надсилаю файлом...</i>",
        "err_video_note": "⚠️ <b>Обмеження відеоповідомлень.</b>\n🔄 <i>Надсилаю файлом...</i>",
        "err_file_restored": "(Файл)",
        "err_generic": "⚠️ Помилка відновлення:",
        
        "txt_date": "⏰ Дата:",
        "txt_chat": "📍 Чат:",
        "txt_from": "👤 Від:",
        "txt_type": "📎 Тип:",
        "txt_content": "💬 Зміст:",
        "txt_caption": "🏷 Підпис:",
        "txt_incoming": "📥 ВХІДНЕ",
        "txt_outgoing": "📤 ВИХІДНЕ",
        "txt_media_file": "[Медіа-файл]",
        
        "lang_select": "🌍 <b>Оберіть мову / Select Language</b>"
    }
}