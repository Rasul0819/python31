from aiogram import Bot,Dispatcher,types,executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from keyboards import car_menu
from datas import start_db,show_cars,add_to_db

class SellCar(StatesGroup):
    name = State()
    Model = State()
    horsepower = State()
    numbercar = State()
    birth_date = State()
    new = State()
    photo_car = State()

api = '7355286497:AAGPqi_h5eGVb7ESpsKS_8zL6eUVa_P5fYM'
PROXY_URL = "http://proxy.server:3128/"
bot = Bot(api,proxy=PROXY_URL)
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)



async def on_startup(_):
    await start_db()

@dp.message_handler(commands=['start'])
async def send_hi(xabar:types.Message):
    await xabar.answer(text='Hello!',reply_markup=car_menu)

@dp.callback_query_handler()
async def send_reg(call:types.CallbackQuery):
    data = call.data
    if data=='sellcar':
        await bot.send_message(
            chat_id=call.from_user.id,
            text='Здравствуйте\nНапишите свое имя для продажи машины!'
        )
        await SellCar.name.set()
    elif data=='buycar':
        cars = await show_cars()
        for car in cars:
            await bot.send_photo(
                photo=car[6],
                chat_id=call.from_user.id,
                caption=f'''Отлично машина выставлена на продажу!,
name:{car[0]},
model:{car[1]},
horsepower:{car[2]},
nomer:{car[3]},
data:{car[4]},
new?:{car[5]}
'''

            )
@dp.message_handler(state=SellCar.name)
async def send_model(message:types.Message,state:FSMContext):
    async with state.proxy() as magliwmat:
        magliwmat['name_user']=message.text
    await message.answer('напишите модель машины!')
    await SellCar.Model.set()
@dp.message_handler(state=SellCar.Model)
async def send_model(message:types.Message,state:FSMContext):
    async with state.proxy() as magliwmat:
        magliwmat['model']=message.text
    await message.answer('напишите сколько лошадильных сил в машине!')
    await SellCar.horsepower.set()
@dp.message_handler(state=SellCar.horsepower)
async def send_horse(message:types.Message,state:FSMContext):
    async with state.proxy() as magliwmat:
        magliwmat['horse_power']=message.text
    await message.answer('Теперь оставьте номер машины!')
    await SellCar.numbercar.set()
@dp.message_handler(state=SellCar.numbercar)
async def send_phone(message:types.Message,state:FSMContext):
    async with state.proxy() as magliwmat:
        magliwmat['num_car']=message.text
    await message.answer('Теперь оставьте дату машины!')
    await SellCar.birth_date.set()
@dp.message_handler(state=SellCar.birth_date)
async def send_email(message:types.Message,state:FSMContext):
    async with state.proxy() as magliwmat:
        magliwmat['birth_car']=message.text
    await message.answer('Теперь ответьте нам новый или бу машина!')
    await SellCar.new.set()
@dp.message_handler(state=SellCar.new)
async def send_birth(message:types.Message,state:FSMContext):
    async with state.proxy() as magliwmat:
        magliwmat['new_car']=message.text
    await message.answer('Теперь отправьте нам фото машины для продажи!')
    await SellCar.photo_car.set()
@dp.message_handler(content_types='photo',state=SellCar.photo_car)
async def send_photo(photo:types.ContentType.PHOTO,state:FSMContext):
    async with state.proxy() as magliwmat:
        magliwmat['photoCar']=photo['photo'][0]['file_id']
    await bot.send_photo(caption=f'''Отлично машина выставлена на продажу!,
name:{magliwmat['name_user']},
model:{magliwmat['model']},
horsepower:{magliwmat['horse_power']},
nomer:{magliwmat['num_car']},
data:{magliwmat['birth_car']},
new?:{magliwmat['new_car']},''',
    photo=magliwmat['photoCar'],
    chat_id=photo.from_user.id)

    await add_to_db(
        seller=magliwmat['name_user'],
        model=magliwmat['model'],
        horsepower=magliwmat['horse_power'],
        date=magliwmat['birth_car'],
        car_number=magliwmat['num_car'],
        photo=magliwmat['photoCar'],
        is_new=magliwmat['new_car']
    )
    await state.finish()
if __name__=='__main__':
    executor.start_polling(dp,skip_updates=True,on_startup=on_startup)