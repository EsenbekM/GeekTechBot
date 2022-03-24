from aiogram import Bot, Dispatcher, types
from db import Database
from lists import *
from mp import *
from environs import Env

env = Env()
env.read_env()

TOKEN = env.str('TOKEN')


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db = Database('database.db')

ADMINS = []

ADMINS.append(683673337)


def check_bad_words(mess: str):
    for i in bad_words:
        if i in mess.lower():
            return True

def str_analyth(mess):
    if (
        '#standup' in mess and
        'что сделал' in mess and 
        'проблем' in mess and 
        'что буду делать' in mess and 
        len(mess) > 50
        ):

        return True


def get_info() -> str:
    '''
        function for get structure info
    '''
    ans = dict()
    users = db.get_users()
    all_amount = db.all_amount()

    message_text = ""
    if len(users) != 0:
        for row in users:
            if row[2] not in list(ans.keys()):
                ans[row[2]] = [(row[3], row[4], row[5])]
            elif row[2] in list(ans.keys()):
                ans[row[2]].append((row[3], row[4], row[5]))
        
        for k, v in ans.items():
            message_text += f"\nGroup: {k}\n"
            for i in v:
                message_text += f"\nNickname: @{i[0]}\nName: {i[1]}\nAmount of StandUp's: {i[2]}\n"
        return  message_text + f'\nAll amount: {all_amount}'
    return "StandUp list is empty!"

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(
        message.from_user.id, 
        f"/start - Начать\n/get_detail - Получить детальную информацию о стендапах\n/get_group - Общее количество стендапов в группе\n/clear - Очистить базу данных"
        )

@dp.message_handler(commands=['info'])
async def start(message: types.Message):
    await message.delete()
    if message.chat.type != 'private':
        await bot.send_message(
            message.chat.id,
            "ПИШИТЕ СТЕНДАПЫ СТРОГО ПО ШАБЛОНУ!\n\n#StandUp\nЧто сделал(a): (Напишите что вы сделали в ходе выполнения дз)\nПроблемы: (Опишите проблемы с которыми столкнулись в ходе выполнения дз)\nЧто буду делать: (Напишите что вы собираетесь делать, чтобы улучшить результат)\n"
            )
    

@dp.message_handler(commands=['clear'])
async def clear_db(message: types.Message):
    if message.chat.type == 'private':
        if message.from_user.id in ADMINS:
            await bot.send_message(
                message.from_user.id, 
                f"Вы уверены что хотите очистить данные?", 
                reply_markup=cl
                )

@dp.message_handler(commands=['clear_all'])
async def clear_all_db(message: types.Message):
    if message.chat.type == 'private':
        if message.from_user.id in ADMINS:
            await bot.send_message(message.from_user.id, f"Все данные удалены!")
            ADMINS.clear()
            db.clear_all()

@dp.callback_query_handler(text="yes")
async def funny_mod(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    db.clear_table()
    await bot.send_message(message.from_user.id, f"Данные успешно очищены!")

@dp.callback_query_handler(text="no")
async def funny_mod(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, f"Отмена")

@dp.message_handler(commands=['admin'])
async def create_admin(message: types.Message):
    '''
        hendler to add admin
    '''
    if message.chat.type == 'private' and message.from_user.id == 683673337:
        try:
            admin_id = int(message.text[7:])
            db.add_admin(
                user_id=admin_id,
                group='admin',
                nickname='admin',
                name='admin',
                count=0
                )
            for i in (db.get_admin()):
                ADMINS.append(i[1])
            await bot.send_message(message.from_user.id, "Admin added!")
            
        except ValueError:
            await bot.send_message(message.from_user.id, "ERROR!")

#nickname, name, count
@dp.message_handler(commands=['get_detail'])
async def get_info_to_admin(message: types.Message):
    '''
        hendler for get info for admins
    '''
    if message.chat.type == 'private':
        if message.from_user.id in ADMINS:
            message_text = get_info()
            if len(message_text) == 0:
                await bot.send_message(message.from_user.id, "StendUp list is empty!")
            else:
                await bot.send_message(message.from_user.id, message_text)
        else:
            await message.reply("Permission denied!")    

@dp.message_handler(commands=['get_group'])
async def get_info_to_admin(message: types.Message):
    '''
        hendler for get info for admins
    '''
    if message.chat.type == 'private':
        if message.from_user.id in ADMINS:
            message_text = ""
            dct = db.group_amount()
            for k,v in dct.items():
                message_text += f"\n{k} - {v}"
            if len(message_text) == 0:
                await bot.send_message(message.from_user.id, "StendUp list is empty!")
            else:
                await bot.send_message(message.from_user.id, message_text)
        else:
            await message.reply("Permission denied!")  

@dp.message_handler()
async def find_stendup(message: types.Message):
    '''
        hendler to find stendups in the chats
    '''
    if check_bad_words(message.text) and message.from_user.id == 683673337:
            await message.reply("Согласен)")
    elif check_bad_words(message.text):
            await message.reply("Ненормативная лексика запрещена!")
    elif (message.chat.type != 'private') and str_analyth(message.text.lower()):
        if db.user_exist(message.from_user.id):
            db.add_count(message.from_user.id)
        if not db.user_exist(message.from_user.id):
            db.add_user(
                user_id=message.from_user.id,
                group=message.chat.title,
                nickname=message.from_user.username,
                name=message.from_user.full_name,
                count=1
                )
            db.set_active(message.from_user.id, 1)
        await message.reply("Ваш StandUp засчитан!")

    elif (message.chat.type != 'private') and not str_analyth(message.text.lower()) and '#standup' in message.text.lower():
        await message.reply("Ваш StandUp не был засчитан!")
        await bot.send_message(
            message.chat.id,
            "ПИШИТЕ СТЕНДАПЫ СТРОГО ПО ШАБЛОНУ!\n\n#StandUp\nЧто сделал(a):\nПроблемы:\nЧто буду делать:\n"
            )