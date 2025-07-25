# Command handlers
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CommandHandler, CallbackQueryHandler

from src.config.constants import ENERGY_LEVELS, LogType
from src.logic.flows.moment_flow import MOMENT_FLOW
from src.logic.utils.moment_utils import build_reply_keyboard, clean_text_input, get_current_timestamp
from src.data.service import store_log_entry  # Stub for DB logic
from datetime import datetime
#from src.logic.utils.swing_utils import track_mood_swing

# State keys
SELECT_LOG_TYPE, ASK_ENERGY, ASK_TRIGGER, STORE_ENTRY, END_FLOW = range(5)

# Entry point: free-text message
async def start_log_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    context.user_data["comment"] = clean_text_input(text)

    # Ask for log type
    prompt = MOMENT_FLOW[0]["prompt"]
    options = MOMENT_FLOW[0]["options"]
    reply_markup = build_reply_keyboard(options)
    await update.message.reply_text(prompt, reply_markup=reply_markup)
    return SELECT_LOG_TYPE

async def handle_log_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_type = update.message.text.strip()
    if not LogType.has_value(log_type) or log_type == "cognitive_state":
        await update.message.reply_text("Please select a valid option.")
        return SELECT_LOG_TYPE

    context.user_data["log_type"] = log_type

    # Ask energy
    prompt = MOMENT_FLOW[1]["prompt"]
    options = MOMENT_FLOW[1]["options"]
    reply_markup = build_reply_keyboard(options)
    await update.message.reply_text(prompt, reply_markup=reply_markup)
    return ASK_ENERGY

async def handle_energy_score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    energy = update.message.text.strip()
    if energy not in ENERGY_LEVELS:
        await update.message.reply_text("Please choose a valid energy level.")
        return ASK_ENERGY

    context.user_data["energy_score"] = ENERGY_LEVELS[energy]

    # Ask trigger
    prompt = MOMENT_FLOW[3]["prompt"]
    await update.message.reply_text(prompt)
    return ASK_TRIGGER

async def handle_trigger(update: Update, context: ContextTypes.DEFAULT_TYPE):
    trigger_text = clean_text_input(update.message.text)
    evnttrigger_text = clean_text_input(update.message.text)
    context.user_data["evnttrigger"] = evnttrigger_text
    context.user_data["timestamp"] = get_current_timestamp()

    raw_timestamp = context.user_data["timestamp"]
    if isinstance(raw_timestamp, str):
        timestamp = datetime.fromisoformat(raw_timestamp.replace("Z", "+00:00"))
    else:
        timestamp = raw_timestamp

    # Store entry
    await store_log_entry(
        user_id=update.effective_user.id,
        log_type=context.user_data["log_type"],
        energy_score=context.user_data["energy_score"],
        comment=context.user_data.get("comment"),
        evnttrigger=context.user_data["evnttrigger"],
        timestamp=timestamp
    )

    # If mood, run mood swing tracking
  #  if context.user_data["log_type"] == "mood":
     #   await track_mood_swing(update, context)

    await update.message.reply_text("Your moment has been recorded. ✅")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Logging canceled.")
    return ConversationHandler.END

log_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.TEXT & (~filters.COMMAND), start_log_flow)],
    states={
        SELECT_LOG_TYPE: [MessageHandler(filters.TEXT, handle_log_type)],
        ASK_ENERGY: [MessageHandler(filters.TEXT, handle_energy_score)],
        ASK_TRIGGER: [MessageHandler(filters.TEXT, handle_trigger)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

def setup_handlers(app):
    app.add_handler(log_handler)
