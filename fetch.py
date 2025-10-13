import arxiv
import datetime
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"',
    filename='logs/fetch.log', encoding='utf-8', level="DEBUG"
)

def fetch_papers_list():
    logger.info('Fetching new papers from arXiv (returned as list).')

    client = arxiv.Client()

    today = datetime.date.today()
    one_week_ago = today - datetime.timedelta(days=7)
    week_range = f"{one_week_ago.strftime('%Y%m%d')}0000 TO {today.strftime('%Y%m%d')}2359"
    query = f"cat:cs.CL AND submittedDate:[{week_range}]"
    max_results = 100

    search = arxiv.Search(
        query = query,
        max_results = max_results,
        sort_by = arxiv.SortCriterion.SubmittedDate
    )
    results = client.results(search)

    logger.debug("query=%s; max_results=%d", query, max_results)

    # Careful: this is slow for large results sets (in this case we are limited to 100)
    results = list(results)
    return results