import arxiv
import datetime
import logging
import telegram
import os
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(
    format='format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"',
    filename='logs/app.log', encoding='utf-8', level="DEBUG"
)

def fetch_papers_list():
    logger.info('Fetching new papers from arXiv (returned as list).')

    client = arxiv.Client()

    today = datetime.date.today()
    one_week_ago = today - datetime.timedelta(days=7)
    week_range = f"{one_week_ago.strftime('%Y%m%d')}0000 TO {today.strftime('%Y%m%d')}2359"
    query = f"cat:cs.CL AND submittedDate:[{week_range}]"
    max_results = 10

    search = arxiv.Search(
        query = query,
        max_results = max_results,
        sort_by = arxiv.SortCriterion.SubmittedDate
    )
    results = client.results(search)

    logger.debug(f"query={query}; max_results={max_results}")

    # Careful: this is slow for large results sets (in this case it's fine)
    results = list(results)
    return results

def add_paper_links(output: str, papers: list) -> str:
    id2link = {str(id+1): paper.pdf_url for id, paper in enumerate(papers)}
    for id in id2link:
        target = f"[{id}]({id2link[id]})"
        output = output.replace(f"[id={id}]", target)

    logger.info(f"Output with paper links: {output}")
    return output

async def send_telegram_message(message):
    bot = telegram.Bot(os.getenv("TELEGRAM_BOT_TOKEN"))
    for part in message.split('---'):
        if len(part) > 4096:
            for i in range(0, len(part), 4096):
                await bot.send_message(text=part[i:i+4096], chat_id=os.getenv("TELEGRAM_USER_ID"))
        else:
            await bot.send_message(text=part, chat_id=os.getenv("TELEGRAM_USER_ID"))