import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage


class AuthStates(StatesGroup):
    waiting_for_password = State()


async def start_handler(message: types.Message):
    # Запрашиваем пароль при старте бота
    await message.answer("Введите пароль:")
    # Устанавливаем состояние ожидания ввода пароля
    await AuthStates.waiting_for_password.set()


async def process_password_input(message: types.Message, state: FSMContext):
    # Получаем введенный пользователем пароль
    password = message.text
    # Проверяем, соответствует ли введенный пароль ожидаемому
    if password != "my_secret_password":
        # Выводим сообщение об ошибке и снова запрашиваем пароль
        await message.answer("Неправильный пароль. Попробуйте еще раз:")
        return
    # Очищаем состояние FSM и сообщаем пользователю об успешной аутентификации
    await state.finish()
    await message.answer("Вы успешно аутентифицированы. Теперь вы можете использовать команды бота.")


async def command_handler(message: types.Message):
    # Проверяем, авторизован ли пользователь
    user_id = message.from_user.id
    if user_id not in authorized_users:
        await message.answer("Вы не авторизованы. Введите пароль для доступа к функциям бота.")
        await AuthStates.waiting_for_password.set()
        return

    # Выполняем основную логику команды
    await message.answer("Текст сообщения")


async def main():
    # Инициализируем бота и хранилище FSM
    bot = Bot(token="")
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    # Регистрируем обработчики
    dp.register_message_handler(start_handler, commands="start")
    dp.register_message_handler(command_handler, commands="command")

    dp.register_message_handler(
        process_password_input,
        state=AuthStates.waiting_for_password
    )

    # Запускаем бота
    await dp.start_polling()


if __name__ == '__main__':
    authorized_users = set()
    asyncio.run(main())