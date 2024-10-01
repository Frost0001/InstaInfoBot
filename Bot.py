import os
import requests
import telebot
import webbrowser

# فتح رابط قناة تلغرام عند تشغيل البوت
webbrowser.open('https://t.me/kwulu')

# التحقق من تثبيت حزمة cfonts، وتثبيتها في حال عدم وجودها
try:
    from cfonts import render
except ImportError:
    os.system('pip install python-cfonts')
    from cfonts import render

# عرض اسم المطور بتنسيق جمالي
developer_name = "Frost"
output = render(f'{developer_name}', colors=['red', 'yellow'], align='center')
print(output)

# توكن البوت (استبدله بالتوكن الخاص بك)
bot_token = "ضع_توكن_البوت_هنا"

# تهيئة البوت باستخدام التوكن
bot = telebot.TeleBot(bot_token)


# معالجة أمر /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text="قناة البوت 🔰", url="https://t.me/kwulu"))
    
    welcome_message = "أهلاً بك! قم بإرسال اسم المستخدم الخاص بالضحية على إنستغرام! 🥷⚡"
    bot.send_message(message.chat.id, welcome_message, parse_mode='Markdown', reply_markup=markup)


# معالجة أي نص مرسل
@bot.message_handler(func=lambda message: True)
def get_instagram_info(message):
    username = message.text.strip()

    # إعداد الرؤوس (headers) لطلب HTTP من إنستغرام
    headers = {
        'accept': '*/*',
        'accept-language': 'ar',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'x-ig-app-id': '936619743392459',
    }

    try:
        # إرسال الطلب لجلب معلومات المستخدم من إنستغرام
        url = f'https://i.instagram.com/api/v1/users/web_profile_info/?username={username}'
        response = requests.get(url, headers=headers).json()
        user_data = response["data"]["user"]

        # استخراج المعلومات من البيانات المسترجعة
        full_name = user_data["full_name"]
        biography = user_data["biography"]
        followers = user_data["edge_followed_by"]["count"]
        following = user_data["edge_follow"]["count"]
        user_id = user_data["id"]
        posts = user_data["edge_owner_to_timeline_media"]["count"]
        profile_pic_url = user_data["profile_pic_url_hd"]

        # استخراج تاريخ الإنشاء باستخدام خدمة خارجية
        creation_date = requests.get(f"https://o7aa.pythonanywhere.com/?id={user_id}").json()["date"]

        # رسالة النتائج
        result_message = f"""
        ⌯ تم سحب معلومات الضحية بنجاح ✅ ⌯
        . ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ .
        [💙] الإسم ➥ {full_name}
        [👻] اسم المستخدم ➥ {username}
        [👥] المتابعون ➥ {followers}
        [🗣] المتابعين ➥ {following}
        [🆔] المعرف ➥ {user_id}
        [👻] البايو ➥ {biography}
        [💞] المنشورات ➥ {posts}
        [⏱] التاريخ ➥ {creation_date}
        . ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ .
        ⚖️ Telegram: @Frost_0001\n⚖️ CH: @kwulu
        """
        
        # إرسال الصورة الشخصية مع الرسالة
        bot.send_photo(message.chat.id, profile_pic_url, caption=result_message, parse_mode='Markdown')

    except Exception as e:
        bot.send_message(message.chat.id, "حدث خطأ أثناء محاولة جلب المعلومات. تأكد من صحة اسم المستخدم.")
        print(f"Error: {e}")


# بدء البوت
if __name__ == '__main__':
    print("البوت يعمل الآن...")
    bot.polling()
