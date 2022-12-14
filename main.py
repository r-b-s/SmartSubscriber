
import os,aiogram, asyncio,psycopg2


DB = psycopg2.connect(os.getenv('DATABASE_URL'), sslmode='require')
BOT = aiogram.Bot(token=os.getenv('SmartSub'))
DP = aiogram.Dispatcher(BOT)
DB.autocommit= True


@DP.message_handler(aiogram.dispatcher.filters.RegexpCommandsFilter(regexp_commands=['sub\s(.+)']))   
async def sub(message: aiogram.types.Message, regexp_command):
    await BOT.send_message(message.from_user.id, regexp_command.group(1) ) 
    with DB.cursor() as cursor:
        cursor.execute("""INSERT INTO blogs(URI) VALUES (%s);""", ( regexp_command.group(1),) )
        


async def poll():
    pass


@DP.message_handler(commands=['help','start'])
async def help(message:  aiogram.types.Message):  
    with open('README.md','r', encoding="utf-8") as help:       
        await BOT.send_message(message.from_user.id,help.read() )   

@DP.message_handler(commands=['setup'])
async def setup(message:  aiogram.types.Message):
    with DB.cursor() as cursor:
        cursor.execute("""CREATE TABLE IF NOT EXISTS blogs (BlogId SERIAL PRIMARY KEY, URI VARCHAR(255) NOT NULL);""")
        cursor.execute("""SELECT * FROM blogs ;""")  
        results =  cursor.fetchall()  
        print (results)        
        await BOT.send_message(message.from_user.id,results)


def repeat(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(60*5, repeat, coro, loop)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.call_later(60*5, repeat, poll, loop)
    aiogram.executor.start_polling(DP,loop=loop)