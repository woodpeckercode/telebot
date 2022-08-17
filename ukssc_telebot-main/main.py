import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import emoji

PORT = int(os.environ.get('PORT', 8443))
TOKEN = os.environ["TOKEN"]

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
  update.message.reply_text(main_menu_message(),
  reply_markup=main_menu_keyboard(),
  parse_mode=ParseMode.HTML)

def main_menu(update,context):
  query = update.callback_query
  query.answer()
  query.edit_message_text(
                        text=main_menu_message2(),
                        reply_markup=main_menu_keyboard(),
                        parse_mode=ParseMode.HTML)
  
def events_menu(update,context):
  query = update.callback_query
  query.answer()
  query.edit_message_text(
                        text=events_menu_message(),
                        reply_markup=events_menu_keyboard())

def faq_menu(update,context):
  query = update.callback_query
  query.answer()
  query.edit_message_text(
                        text=faq_menu_message(),
                        reply_markup=faq_menu_keyboard())

# and so on for every callback_data option
def first_submenu(bot, update):
  pass

def second_submenu(bot, update):
  pass
def error(update, context):
    print(f'Update {update} caused error {context.error}')

##############################  Keyboards ##############################
def main_menu_keyboard():
  keyboard = [
        [
            InlineKeyboardButton("Upcoming Events", callback_data='events'),
            InlineKeyboardButton("FAQ", callback_data='faq'),
        ],
        [InlineKeyboardButton("Meet our Exco", url='https://www.theukssc.co.uk/current-committee')],
        [InlineKeyboardButton("Follow us on Instagram!", url="https://www.instagram.com/theukssc/")],
    ]
  return InlineKeyboardMarkup(keyboard)

def events_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Submenu 1-1', callback_data='m1_1')],
              [InlineKeyboardButton('Submenu 1-2', callback_data='m1_2')],
              [InlineKeyboardButton('Main menu', callback_data='main')]]
  return InlineKeyboardMarkup(keyboard)

def faq_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Submenu 2-1', callback_data='m2_1')],
              [InlineKeyboardButton('Submenu 2-2', callback_data='m2_2')],
              [InlineKeyboardButton('Main menu', callback_data='main')]]
  return InlineKeyboardMarkup(keyboard)

########################################################################

##############################  Message ##############################
def main_menu_message():
  image = 'https://static.wixstatic.com/media/55a087_e59723a339b84c03ac6557472d2142fc~mv2.png/v1/fit/w_2500,h_1330,al_c/55a087_e59723a339b84c03ac6557472d2142fc~mv2.png'
  return emoji.emojize('Hi :waving_hand: Welcome to UKSSC\'s Telegram Bot! :smiling_face_with_open_hands::smiling_face_with_hearts:\n\nPlease choose :backhand_index_pointing_down: any one of the options below to find out more. \n<a href="' + image + '">&#8205;</a>')
def main_menu_message2():
  return emoji.emojize('Hi :waving_hand: Welcome to UKSSC\'s Telegram Bot! :smiling_face_with_open_hands::smiling_face_with_hearts:\n\nPlease choose :backhand_index_pointing_down: any one of the options below to find out more.')

def events_menu_message():
  return 'Below is a list of upcoming events. Click to find out more:'

def faq_menu_message():
  return 'Frequently Asked Questions:'


########################################################################

def main() -> None:
    """Run the bot."""
    updater = Updater(TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    updater.dispatcher.add_handler(CallbackQueryHandler(events_menu, pattern='events'))
    updater.dispatcher.add_handler(CallbackQueryHandler(faq_menu, pattern='faq'))
    updater.dispatcher.add_handler(CallbackQueryHandler(first_submenu,
                                                    pattern='m1_1'))
    updater.dispatcher.add_handler(CallbackQueryHandler(second_submenu,
                                                    pattern='m2_1'))
    updater.dispatcher.add_error_handler(error)
    updater.start_webhook(listen="0.0.0.0", port=PORT,url_path=TOKEN, webhook_url = 'https://uksscbot.herokuapp.com/' + TOKEN) 
    updater.idle()


if __name__ == '__main__':
    main()
