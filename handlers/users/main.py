from aiogram.types import Message, ChatPermissions, input_file, ChatMemberAdministrator
from loader import dp, supergroup, bot
from aiogram import F
from aiogram.filters import and_f
from time import time



# Yangi foydalanuvchi qo'shilganda

@dp.message(F.new_chat_members)
async def new_member(message: Message):
    for user in message.new_chat_members:
        user_name = user.first_name  
        await message.answer(f"{user_name} Guruhga xush kelibsiz!")
    await message.delete()

# Foydalanuvchi chiqib ketsa

@dp.message(F.left_chat_member)
async def left_member(message:Message):
    user = message.left_chat_member.full_name
    await message.answer(f"{user} Xayr!")
    await message.delete()

# BAN BO'LISHI VA BAN DAN OCHISH

@dp.message(and_f(F.reply_to_message, F.text=="/ban"))
async def ban_user(message:Message):
    user_id =  message.reply_to_message.from_user.id
    await message.chat.ban_sender_chat(user_id)
    await message.answer(f"{message.reply_to_message.from_user.first_name} guruhdan chiqarib yuborilasiz.")

@dp.message(and_f(F.reply_to_message,F.text=="/unban"))
async def unban_user(message:Message):
    user_id =  message.reply_to_message.from_user.id
    await message.chat.unban_sender_chat(user_id)
    await message.answer(f"{message.reply_to_message.from_user.first_name} guruhga qaytishingiz mumkin.")


# Mute qilish (moslashuvchan vaqt bilan)

@dp.message(and_f(F.reply_to_message, F.text=="/mute"), supergroup)
async def mute_user(message:Message):
    user_id =  message.reply_to_message.from_user.id
    permission = ChatPermissions(can_send_messages=False)

    until_date = int(time()) + 60 
    
    await message.chat.restrict(user_id=user_id, permissions=permission, until_date=until_date)
    await message.answer(f"{message.reply_to_message.from_user.first_name} 1 minutga blocklandingiz")

# Guruh rasmini o'rnatish

@dp.message(and_f(F.reply_to_message.photo,F.text=="/setphoto"))
async def setphoto_group(message:Message):
    photo =  message.reply_to_message.photo[-1].file_id
    file = await bot.get_file(photo)
    file_path = file.file_path
    file = await bot.download_file(file_path)
    file = file.read()
    await message.chat.set_photo(photo=input_file.BufferedInputFile(file=file,filename="asd.jpg"))
    await message.answer("Gruh rasmi uzgardi")

    
# Guruh a’zolarini ro‘yxatlash

@dp.message(F.text == "/members")
async def list_members(message: Message):
    try:
        members = await message.chat.get_members()
        member_list = "\n".join([f"{m.user.mention_html()} - {'Admin' if m.is_chat_admin() else 'User'}" for m in members[:10]])
        await message.answer(f"Guruh a'zolari (top 10):\n{member_list}")
    except Exception as e:
        await message.answer(f"Xatolik: {str(e)}")


# Ovoz berish (poll) yaratish 
# masalan, /poll Bugun yig‘ilish bo‘lsinmi?
# @dp.message(F.text.regexp(r"/poll\s+(.+)"))
# async def create_poll(message: Message):
#     try:
#         question = message.text.split("/poll", 1)[1].strip()
#         await message.answer_poll(question=question, options=["Ha", "Yo‘q", "Bilmayman"], is_anonymous=False)
#     except Exception as e:
#         await message.answer(f"Xatolik: {str(e)}")


# 2 - usul 
@dp.message(F.text.startswith("/poll"))
async def create_poll(message: Message):
    args = message.text.split("\n")[1:]  # Savol va variantlar
    if len(args) < 3:
        return await message.answer("⛔ Iltimos, kamida 1 savol va 2 ta variant yozing.")

    question = args[0]
    options = args[1:]
    await bot.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=options,
        is_anonymous=False
    )

# /poll
# Guruhda qanday o'zgarishlar kerak?
# Variant 1
# Variant 2
# Variant 3


# Guruh statistikasi

@dp.message(F.text == "/stats")
async def group_stats(message: Message):
    try:
        member_count = await message.chat.get_member_count()
        await message.answer(f"Guruh statistikasi:\nA'zolar soni: {member_count}")
    except Exception as e:
        await message.answer(f"Xatolik: {str(e)}")


# Guruh sozlamalarini ko‘rsatish
# 1 - usul
@dp.message(F.text == "/info")
async def group_info(message: Message):
    chat = message.chat
    member = await bot.get_chat_member(chat.id, message.from_user.id)

    if isinstance(member, ChatMemberAdministrator):
        text = (
            f"📌 Guruh nomi: {chat.title}\n"
            f"🆔 Guruh ID: {chat.id}\n"
            f"👥 A'zolar soni: {await bot.get_chat_member_count(chat.id)}\n"
            f"👑 Admin: {member.user.full_name}"
        )
        await message.answer(text)
    else:
        await message.answer("⛔ Siz admin emassiz!")


# Xaqoratli so'zlar uchun filtr

# xaqoratli_sozlar = {"tentak", "jinni", "✅"}

# @dp.message(and_f(F.chat.func(lambda chat: chat.type == "supergroup"),F.text ))
# async def tozalash(message:Message):
#     text = message.text

#     for soz in xaqoratli_sozlar:
#         # salom og'ayni jinni bro
#         print(soz, text.lower().find(soz))  

#         if text.lower().find(soz) != -1:
#             user_id =  message.from_user.id
#             until_date = int(time()) + 60
#             permission = ChatPermissions(can_send_messages=False)
#             await message.chat.restrict(user_id=user_id,permissions=permission,until_date=until_date)
#             await message.answer(text=f"{message.from_user.mention_html()} o'zing {soz}")
#             await message.delete() 
#             break

# Anti-Spam tizimi (Tez-tez yozadiganlarni bloklash)

# from collections import defaultdict

# user_messages = defaultdict(list)

# @dp.message(F.text)
# async def anti_spam(message: Message):
#     user_id = message.from_user.id
#     now = time()

#     user_messages[user_id].append(now)
#     user_messages[user_id] = [msg_time for msg_time in user_messages[user_id] if now - msg_time < 5]

#     if len(user_messages[user_id]) >= 3:
#         permission = ChatPermissions(can_send_messages=False)
#         await message.chat.restrict(user_id=user_id, permissions=permission, until_date=int(now) + 60)
#         await message.answer(f"{message.from_user.first_name} spam uchun 1 daqiqaga bloklandi.")
