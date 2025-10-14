import datetime
import asyncio

from agent import run_agent
from utils import send_telegram_message

if __name__ == "__main__":
    output = run_agent()

    # Save summary to local file
    filename = f"./AI-Summaries/AI-Summary ({datetime.date.today().strftime('%Y%m%d')}).md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(output)

    # Send summary via Telegram
    asyncio.run(send_telegram_message(output))