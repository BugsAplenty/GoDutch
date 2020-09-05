#!/usr/bin/env python

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

HELP_BUTTON = InlineKeyboardButton(text='Help', callback_data='Help')
CANCEL_BUTTON = InlineKeyboardButton(text='Cancel', callback_data='Cancel')
SET_PLAN_BUTTON = InlineKeyboardButton(text='Set plan', callback_data='Set plan')
INPUT_MEAL_BUTTON = InlineKeyboardButton(text='Input meal', callback_data='Input meal')
CHANGE_PLAN_BUTTON = InlineKeyboardButton(text='Change plan', callback_data='Change plan')
ACCEPT_BUTTON = InlineKeyboardButton(text='Accept', callback_data='Accept')

START_SELECT = InlineKeyboardMarkup(
    [[
        SET_PLAN_BUTTON,
        HELP_BUTTON
    ]]
)
TIMEZONE_SELECT = InlineKeyboardMarkup(
    [[
        HELP_BUTTON
    ]]
)
SET_GOAL_SELECT = InlineKeyboardMarkup(
    [[
        HELP_BUTTON
    ]]
)
START_PLAN_SELECT = InlineKeyboardMarkup(
    [[
        INPUT_MEAL_BUTTON,
        CHANGE_PLAN_BUTTON,
        HELP_BUTTON
    ]]
)
INPUT_MEAL_SELECT = InlineKeyboardMarkup(
    [[
        CANCEL_BUTTON,
        HELP_BUTTON
    ]]
)
INPUT_CANCELLED_SELECT = InlineKeyboardMarkup(
    [[
        INPUT_MEAL_BUTTON,
        CHANGE_PLAN_BUTTON,
        HELP_BUTTON
    ]]
)
INPUT_ACCEPTED_SELECT = InlineKeyboardMarkup(
    [[
        INPUT_MEAL_BUTTON,
        CHANGE_PLAN_BUTTON,
        HELP_BUTTON
    ]]
)
INPUT_ACCEPTED_QUOTA_EXCEEDED_SELECT = InlineKeyboardMarkup(
    [[
        CHANGE_PLAN_BUTTON,
        HELP_BUTTON
    ]]
)
NEW_FOOD_CAL_CHECK = InlineKeyboardMarkup(
    [[
        CANCEL_BUTTON,
        HELP_BUTTON
    ]]
)
AMOUNT_CHECK_SELECT = InlineKeyboardMarkup(
    [[
        CANCEL_BUTTON,
        HELP_BUTTON
    ]]
)
SUMMARIZE_INPUT_SELECT = InlineKeyboardMarkup(
    [[
        ACCEPT_BUTTON,
        HELP_BUTTON
    ]]
)



