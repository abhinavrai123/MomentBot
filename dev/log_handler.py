from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CommandHandler
from src.config.constants import ENERGY_LEVELS, LogType
from src.logic.flows.moment_flow import MOMENT_FLOW
from src.logic.flows.journal_flow import JOURNAL_FLOW
from src.logic.utils.moment_utils import (
    build_reply_keyboard, clean_text_input, get_current_timestamp
)
from src.data.service import store_log_entry, store_journal_entry
from sqlalchemy.orm import Session

from datetime import datetime

# Flow identifiers
MOMENT = "moment"
JOURNAL = "journal"

# Step to state integer mapping
STEP_TO_STATE = {
    "select_log_type": 0,
    "ask_energy_score": 1,
    "select_cognitive_state": 2,
    "ask_comment": 3,
    "ask_trigger": 4,
    "store_journal_entry": 5,
}
STATE_TO_STEP = {v: k for k, v in STEP_TO_STATE.items()}

def get_flow(context):
    return MOMENT_FLOW if context.user_data.get("flow_type") == MOMENT else JOURNAL_FLOW

# --- ENTRY POINTS ---

async def start_log_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Default flow from free-text input
    context.user_data.clear()
    context.user_data["flow_type"] = MOMENT
    context.user_data["comment"] = clean_text_input(update.message.text.strip())
    context.user_data["step"] = "select_log_type"
    return await proceed_to_next_step(update, context)

async def start_journal_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # /j <text> → JOURNAL_FLOW
    context.user_data.clear()
    context.user_data["flow_type"] = JOURNAL
    context.user_data["log_type"] = "journal"
    context.user_data["comment"] = clean_text_input(update.message.text.replace("/j", "", 1).strip())
    context.user_data["step"] = "ask_energy_score"
    return await proceed_to_next_step(update, context)

# --- STEP HANDLER ---

async def handle_user_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    step = context.user_data["step"]
    user_input = update.message.text.strip()
    flow = get_flow(context)
    step_config = next(s for s in flow if s["step"] == step)

    if step == "select_log_type":
        if not LogType.has_value(user_input) or user_input == "cognitive_state":
            await update.message.reply_text("Please select a valid option.")
            return STEP_TO_STATE[step]
        context.user_data["log_type"] = user_input

    elif step == "ask_energy_score":
        if user_input not in ENERGY_LEVELS:
            await update.message.reply_text("Please choose a valid energy level.")
            return STEP_TO_STATE[step]
        context.user_data["energy_score"] = ENERGY_LEVELS[user_input]

    elif step == "select_cognitive_state":
        if user_input not in ["act", "obs", "crt", "mtn"]:
            await update.message.reply_text("Please choose a valid cognitive state.")
            return STEP_TO_STATE[step]
        context.user_data["cognitive_state"] = user_input

    elif step == "ask_comment":
        context.user_data["comment"] = clean_text_input(user_input)

    elif step == "ask_trigger":
        context.user_data["evnttrigger"] = clean_text_input(user_input)
        context.user_data["timestamp"] = get_current_timestamp()

    elif step == "store_journal_entry":
        return await store_and_finalize(update, context)

    next_step = step_config.get("next")
    context.user_data["step"] = next_step
    return await proceed_to_next_step(update, context)

# --- STEP EXECUTOR ---

async def proceed_to_next_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    step = context.user_data["step"]
    flow = get_flow(context)
    step_config = next(s for s in flow if s["step"] == step)

    if step_config.get("input_type") == "choice":
        reply_markup = build_reply_keyboard(step_config["options"])
        await update.message.reply_text(step_config["prompt"], reply_markup=reply_markup)
    elif step_config.get("input_type") in ["text", "text_optional"]:
        await update.message.reply_text(step_config["prompt"])
    elif step_config.get("input_type") == "none":
        await update.message.reply_text(step_config["prompt"])
        return ConversationHandler.END
    elif step_config.get("action") in ["store_to_db", "store_journal_to_db"]:
        return await store_and_finalize(update, context)

    return STEP_TO_STATE.get(step, ConversationHandler.END)

# --- DB WRITER ---

async def store_and_finalize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ts = context.user_data.get("timestamp") or get_current_timestamp()
    if isinstance(ts, str):
        timestamp = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    else:
        timestamp = ts

    if context.user_data["flow_type"] == MOMENT:
        await store_log_entry(
            user_id=update.effective_user.id,
            log_type=context.user_data["log_type"],
            energy_score=context.user_data.get("energy_score"),
            cognitive_state=context.user_data.get("cognitive_state"),
            comment=context.user_data.get("comment"),
            evnttrigger=context.user_data.get("evnttrigger"),
            timestamp=timestamp
        )
        # if context.user_data["log_type"] == "mood":
        #     await track_mood_swing(update, context)
        context.user_data["step"] = "end_flow"
        return await proceed_to_next_step(update, context)

    elif context.user_data["flow_type"] == JOURNAL:
        await store_journal_entry(
            user_id=update.effective_user.id,
            log_type="journal",
            energy_score=context.user_data["energy_score"],
            comment=context.user_data["comment"],
            timestamp=timestamp
        )
        context.user_data["step"] = "end_flow"
        return await proceed_to_next_step(update, context)

    return ConversationHandler.END

# --- CANCEL ---

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Logging canceled.")
    return ConversationHandler.END


# --- REGISTER ---

log_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.TEXT & (~filters.COMMAND), start_log_flow),
        CommandHandler("j", start_journal_flow),
    ],
    states={
        STEP_TO_STATE["select_log_type"]: [MessageHandler(filters.TEXT, handle_user_input)],
        STEP_TO_STATE["ask_energy_score"]: [MessageHandler(filters.TEXT, handle_user_input)],
        STEP_TO_STATE["select_cognitive_state"]: [MessageHandler(filters.TEXT, handle_user_input)],
        STEP_TO_STATE["ask_comment"]: [MessageHandler(filters.TEXT, handle_user_input)],
        STEP_TO_STATE["ask_trigger"]: [MessageHandler(filters.TEXT, handle_user_input)],
        STEP_TO_STATE["store_journal_entry"]: [MessageHandler(filters.TEXT, handle_user_input)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

def setup_handlers(app):
    app.add_handler(log_handler)
