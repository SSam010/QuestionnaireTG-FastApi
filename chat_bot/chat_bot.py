import os
import sys


sys.path.append(os.path.join(sys.path[0], '/usr/src/questionnaire/website'))

import asyncio
import logging

import telegram
from sqlalchemy import insert
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram import __version__ as TG_VER
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.ext import ConversationHandler

from clients.models import Client
from config import TOKEN, OWNER_ID
from database import async_session_maker

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

# Enable logging
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

logging.basicConfig(
    format=log_format, level=logging.INFO
)
logger = logging.getLogger(__name__)

# Creating object for writing to a file
handler = logging.FileHandler('log_file.log', encoding='utf-8')

formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)

# Add an object to write to a file in the logger
logger.addHandler(handler)

# Steps of the quiz
NAME, INVESTMENT_TIME, INVESTMENT_TOOLS, INVESTMENT_AMOUNT, MEETING, CONTACT_NUMBER = range(6)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начало анкеты. Запрашиваем имя"""
    await update.message.reply_text(
        "Добрый день!\nЗаполняя анкету вы даете согласие на обработку ваших персональных данных. "
        "Ваши персональные данные не будут использоваться для рекламных целей."
        " Они нужны только для внутреннего пользования.",
    )
    await asyncio.sleep(1)
    await update.message.reply_text(
        "Как вас зовут (фамилия и имя)?",
    )
    return NAME


async def name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Получает имя и запрашивает информацию о занятиях"""
    user = update.message.from_user
    context.user_data['name'] = update.message.text
    logger.info(f"User {user.name} send name: {update.message.text}")
    reply_keyboard = [
        ["Не инвестирую"],
        ["Менее 1 года"],
        ["1-3 года"],
        ["3-5 лет"],
        ["Более 5 лет"]
    ]

    await update.message.reply_text(
        f"Рад познакомиться, {update.message.text}!\nРасскажите, Как давно Вы инвестируете?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
            input_field_placeholder="Выберите вариант"
        ),
    )
    return INVESTMENT_TIME


async def investment_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Получает инфо о периоде инвестирования и запрашивает
    список используемых инвестиционных инструментов"""
    user = update.message.from_user
    context.user_data['investment_time'] = update.message.text
    logger.info(f"User {user.name} send investment time: {update.message.text}")
    await update.message.reply_text(
        "Прекрасно!\nА какие инвестиционные инструменты Вы используете?"
    )

    return INVESTMENT_TOOLS


async def investment_tools(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Получает инфо об инвестиционных инструментах и запрашивает размер инвестирования"""
    user = update.message.from_user
    context.user_data['investment_tools'] = update.message.text
    logger.info(f"User {user.name} send investment tools: {update.message.text}")
    reply_keyboard = [
        ["До 100 $"],
        ["От 100 до 1000 $"],
        ["Свыше 1000 $"],
    ]

    await update.message.reply_text(
        "Принято!\nСколько денег ежемесячно Вы отправляете на инвестиции?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
            input_field_placeholder="Выберите вариант"
        ),
    )

    return INVESTMENT_AMOUNT


async def investment_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Получает инфо о размере инвестирования и указать инфо для встречи или контакта"""
    user = update.message.from_user
    context.user_data['investment_amount'] = update.message.text
    logger.info(f"User {user.name} send investment_amount: {update.message.text}")
    await update.message.reply_text(
        "Отлично!\nКогда вам удобно провести консультацию? "
        "Напишите дату и временной диапазон."
    )

    return MEETING


async def meeting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Получает  инфо для встречи и запрашивает мобильный номер для связи"""
    user = update.message.from_user
    context.user_data['meeting'] = update.message.text
    logger.info(f"User {user.name} send meeting info: {update.message.text}")
    await update.message.reply_text(
        "Спасибо!\nУкажите Ваш номер телефона для связи."
    )

    return CONTACT_NUMBER


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отмена или завершение анкеты"""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Всего хорошего! Надеюсь, мы скоро увидимся!", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


async def contact_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Получает контактную информацию и заканчивает диалог"""
    user = update.message.from_user
    context.user_data['contact_number'] = update.message.text
    logger.info(f"User {user.name} send contact_number: {update.message.text}")

    try:
        await add_client_data_to_db(context, user)
        await update.message.reply_text(
            "Отлично, на этом наше знакомство подошло к концу!\n"
            "В скором времени мы ознакомимся с предоставленными данными и свяжемся с Вами!\n"
            "Хорошего дня!")

        logger.info(f"Запись пользователя {user.name} id {user.id} добавлена в базу")

        await send_notification_to_admin(success=True, user=user, context=context)

    except Exception as some_error:
        await update.message.reply_text(
            "К сожалению, произошла ошибка при добавлении Вашей информации. Попробуйте заполнить нашу Google анкету.\n"
            "https://docs.google.com/forms/d/e/1FAIpQLSfpDZP5v4EiqPstY-Zlneo7I5Wy6sEpW9oDEf2oufDz88TUoA/viewform\n"
            "Будем признательны, если вы сообщите, что с ботом возникла проблема.\n"
            "Приносим извинения за доставленные неудобства!")

        logger.info(f"ОШИБКА! Запись пользователя {user.name} id {user.id} не была добавлена в базу\n"
                    f"ошибка: {some_error}")

        await send_notification_to_admin(success=False, user=user, context=context)

    finally:
        context.user_data.clear()

    return ConversationHandler.END


async def add_client_data_to_db(context: ContextTypes.DEFAULT_TYPE, user: telegram._user.User):
    async with async_session_maker() as session:
        stmt = insert(Client).values(
            tg_id=user.id,
            tg_link=user.name,
            name=context.user_data['name'],
            investment_time=context.user_data['investment_time'],
            investment_tools=context.user_data['investment_tools'],
            investment_amount=context.user_data['investment_amount'],
            meeting=context.user_data['meeting'],
            contact_number=context.user_data['contact_number'],

        )
        await session.execute(stmt)
        await session.commit()


async def send_notification_to_admin(success: bool, user: telegram._user.User,
                                     context: ContextTypes.DEFAULT_TYPE, OWNER_ID: int = OWNER_ID):
    """Отправка сообщения владельцу о том, что кто-то заполнил данные"""

    data_user_text = f"Данные пользователя:\n" \
                     f"Cсылка: {user.name}\n" \
                     f"Имя: {context.user_data['name']}\n" \
                     f"Период инвестирования: {context.user_data['investment_time']}\n" \
                     f"Инвест. инструменты: {context.user_data['investment_tools']}\n" \
                     f"Ежемес. инвестирование: {context.user_data['investment_amount']}\n" \
                     f"Когда связаться: {context.user_data['meeting']}\n" \
                     f"Моб. номер: {context.user_data['contact_number']}"

    if success:
        message = f"Пользователь {user.name} заполнил анкету. Данные сохранены в базу данных.\n{data_user_text}"
    else:
        message = f"Пользователь {user.name} заполнил анкету, но данные не были сохранены в базу данных.\n{data_user_text}"

    await context.bot.send_message(chat_id=OWNER_ID, text=message)


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
            INVESTMENT_TIME: [MessageHandler(filters.Regex("^(Не инвестирую|"
                                                           "Менее 1 года|"
                                                           "1-3 года|"
                                                           "3-5 лет|"
                                                           "Более 5 лет)$"),
                                             investment_time
                                             )
                              ],

            INVESTMENT_TOOLS: [MessageHandler(filters.TEXT & ~filters.COMMAND, investment_tools)],
            INVESTMENT_AMOUNT: [MessageHandler(filters.Regex("^(До 100 \$|"
                                                             "От 100 до 1000 \$|"
                                                             "Свыше 1000 \$|)$"),
                                               investment_amount
                                               )
                                ],

            MEETING: [MessageHandler(filters.TEXT & ~filters.COMMAND, meeting)],
            CONTACT_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, contact_number)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
