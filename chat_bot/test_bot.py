# import logging
#
#
# from sqlalchemy import insert
# from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
# from telegram import __version__ as TG_VER
# from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
# from telegram.ext import ConversationHandler
#
# from database import async_session_maker
# from models import Client
# from config import TOKEN
#
# try:
#     from telegram import __version_info__
# except ImportError:
#     __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]
#
# if __version_info__ < (20, 0, 0, "alpha", 1):
#     raise RuntimeError(
#         f"This example is not compatible with your current PTB version {TG_VER}. To view the "
#         f"{TG_VER} version of this example, "
#         f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
#     )
#
# # Enable logging
# logging.basicConfig(
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
# )
# logger = logging.getLogger(__name__)
#
# NAME, OCCUPATION, USEFUL, PHOTO, LINKS, CONTACT_INFO, \
# MAIL_TO_ACCESS, INVESTMENT_CAPITAL, AVERAGE_MONTHLY_INCOME, GOAL = range(10)
#
#
#
#
#
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Начало анкеты. Запрашиваем имя"""
#     await update.message.reply_text("Добрый день!\nКак Вас зовут(Фамилия Имя)?", )
#     return NAME
#
#
# async def name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Получает имя и запрашивает информацию о занятиях"""
#     user = update.message.from_user
#     context.user_data['name'] = update.message.text
#     logger.info("id пользователя через update  %s",  update.update_id)
#     logger.info("id пользователя через user  %s",  user.id)
#     await update.message.reply_text(
#         f"Рад познакомиться, {update.message.text}!\nРасскажите, чем Вы занимаетесь?",
#     )
#     return OCCUPATION
#
#
# async def occupation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Получает инфо о роде деятельности и спрашивает,
#     чем может быть полезен клиент для своих коллег"""
#     user = update.message.from_user
#     context.user_data['occupation'] = update.message.text
#     logger.info("id пользователя через update  %s",  update.update_id)
#     logger.info("id пользователя через user  %s",  user.id)
#     await update.message.reply_text(
#         "Отлично!\nРасскажите, чем Вы можете быть полезны Вашим коллегам?"
#     )
#
#     return USEFUL
#
#
# async def useful(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Получает инфо о полезности клиента и запрашивает ссылку на фото"""
#     user = update.message.from_user
#     context.user_data['useful'] = update.message.text
#     logger.info("id пользователя через update  %s",  update.update_id)
#     logger.info("id пользователя через user  %s",  user.id)
#     await update.message.reply_text(
#         "Это может быть интересно! \nПришлите ссылку на Ваше фото"
#     )
#
#     logger.info("тестовый лог на получение всех данных %s: %s: %s.  Длина словаря %s", context.user_data['name'],
#                 context.user_data['occupation'], context.user_data['useful'], len(context.user_data))
#
#     try:
#         await add_client_data_to_db(context.user_data, user.id)
#     except:
#         await update.message.reply_text(
#             "К сожалению, произошла ошибка при добавлении Вашей информации. Попробуйте заполнить нашу Google анкету."
#             "https://docs.google.com/forms/d/e/1FAIpQLScfPJBjRKqiHDusUKG-lY4Cff4neloJoDa1y5onhvf-Ad_q2g/viewform\n"
#             "Будем признательны, если вы сообщите, что с ботом возникла проблема.\n"
#             "Приносим извинения за доставленные неудобства!"
#         )
#     finally:
#         context.user_data.clear()
#     logger.info("Длина словаря %s",  len(context.user_data))
#
#     return ConversationHandler.END
#
# async def add_client_data_to_db(user_data: dict, user_id: int):
#     async with async_session_maker() as session:
#         stmt = insert(Client).values(*[data for data in user_data.values()].append(user_id))
#         await session.execute(stmt)
#         await session.commit()
#
#
# async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Отмена или завершение анкеты"""
#     user = update.message.from_user
#     logger.info("User %s canceled the conversation.", user.first_name)
#     await update.message.reply_text(
#         "Всего хорошего! Надеюсь, мы скоро увидимся!", reply_markup=ReplyKeyboardRemove()
#     )
#
#     await add_client_data_to_db(context.user_data, user.id)
#
#     context.user_data.clear()
#
#     return ConversationHandler.END
#
#
#
#
# def main() -> None:
#     """Run the bot."""
#     # Create the Application and pass it your bot's token.
#     application = Application.builder().token(TOKEN).build()
#
#     # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
#     conv_handler = ConversationHandler(
#         entry_points=[CommandHandler("start", start)],
#         states={
#             NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
#             OCCUPATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, occupation)],
#             USEFUL: [MessageHandler(filters.TEXT & ~filters.COMMAND, useful)],
#
#         },
#         fallbacks=[CommandHandler("cancel", cancel)],
#     )
#
#     application.add_handler(conv_handler)
#
#     # Run the bot until the user presses Ctrl-C
#     application.run_polling()
#
#
# if __name__ == "__main__":
#     main()



