import logging
from telegram import Update, Poll, PollAnswer
from telegram.ext import Application, CommandHandler, PollHandler, CallbackContext
import random

# Set up logging to help with debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define your quiz questions and options
questions = [
    {
        "question": "What is the main function of the heart?",
        "options": ["Pump blood", "Digest food", "Filter waste", "Protect the body"],
        "answer": "Pump blood"
    },
    {
        "question": "Which of these is not part of the human circulatory system?",
        "options": ["Heart", "Blood", "Lungs", "Stomach"],
        "answer": "Stomach"
    },
    {
        "question": "What is the powerhouse of the cell?",
        "options": ["Nucleus", "Mitochondria", "Ribosome", "Chloroplast"],
        "answer": "Mitochondria"
    },
    # Add more questions as needed
]

# Dictionary to keep track of active polls
active_polls = {}

# Function to start the quiz
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Welcome to the Biology Quiz! Type /quiz to start.")

# Function to send a poll question
async def quiz(update: Update, context: CallbackContext) -> None:
    question = random.choice(questions)
    message = await context.bot.send_poll(
        chat_id=update.effective_chat.id,
        question=question["question"],
        options=question["options"],
        type=Poll.QUIZ,
        correct_option_id=question["options"].index(question["answer"]),
        open_period=30,  # 30 seconds timer
        is_anonymous=False  # Show who answered for better interaction
    )
    # Track the poll with the question data
    active_polls[message.poll.id] = {
        "chat_id": update.effective_chat.id,
        "message_id": message.message_id,
        "question": question["question"],
        "correct_answer": question["answer"]
    }

# Function to handle when a poll ends
async def handle_poll_answer(update: Update, context: CallbackContext) -> None:
    poll_id = update.poll.id
    if poll_id in active_polls:
        question_data = active_polls.pop(poll_id)
        correct_answer = question_data["correct_answer"]
        # Notify the users of the correct answer
        await context.bot.send_message(
            chat_id=question_data["chat_id"],
            text=f"The poll has ended. The correct answer was: {correct_answer}."
        )

# Main function to set up the bot
def main():
    # Replace 'YOUR_API_TOKEN' with your Telegram bot's token
    application = Application.builder().token("8195872687:AAFYDSg4RBCnFZiUBbwUlPkx3uzehue8f6Q").build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("quiz", quiz))
    application.add_handler(PollHandler(handle_poll_answer))

    # Run the bot
    logger.info("Starting the bot...")
    application.run_polling(timeout=10)
if __name__ == '__main__':
    main()