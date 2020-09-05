from pyrogram import Client, Filters, Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from databases.user_database import gerkules_user_db


@Client.on_callback_query(Filters.regex("Set plan") | Filters.regex("Change plan"))
def choose_plan(client: Client, message: Message):
    print(f"***REMOVED***message.from_user.username***REMOVED*** has chosen 'Set plan'.")
    client.send_message(message.from_user.username, "Choose your difficulty level:",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton("Bulk (2500 Cal/day)", callback_data="2500")],
                                [InlineKeyboardButton("Average (2000 Cal/day)", callback_data="2000")],
                                [InlineKeyboardButton("Slim (1500 Cal/day)", callback_data="1500")],
                                [InlineKeyboardButton("Student (1000 Cal/day)", callback_data="1000")],
                                [InlineKeyboardButton("Insane (500 Cal/day)", callback_data="500")],
                                [InlineKeyboardButton("Help", callback_data="Help")]
                            ]
                        )
                        )
    message.continue_propagation()


@Client.on_callback_query(Filters.regex("500") | Filters.regex("1000") | Filters.regex("1500") | Filters.regex("2000") |
                          Filters.regex("2500"))
def begin_plan(client: Client, callback_query: CallbackQuery):
    print(f"***REMOVED***callback_query.from_user.username***REMOVED*** is setting their plan.")
    client.send_message(callback_query.from_user.username,
                        f"Very well. You'll be limited to ***REMOVED***callback_query.data***REMOVED*** calories per day from now on. "
                        f"You can always change your planned intake as you wish.",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton("Input meal", callback_data="Input meal"),
                                    InlineKeyboardButton("Change plan", callback_data="Change plan"),
                                    InlineKeyboardButton("Help", callback_data="Help")
                                ]
                            ]
                        )
                        )
    gerkules_user_db.cursor.execute(f"UPDATE users SET quota=? WHERE username=?",
                                    (float(callback_query.data), callback_query.from_user.username))
    gerkules_user_db.conn.commit()
    callback_query.continue_propagation()

