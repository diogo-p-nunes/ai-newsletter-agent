import argparse
import logging
import datetime

from langchain_ollama.chat_models import ChatOllama
from langgraph.graph import START, END, MessagesState, StateGraph
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage

from prompts import SYSTEM_PROMPT_SUMMARY

from utils import fetch_papers_list, parse_summary, add_paper_links


logger = logging.getLogger(__name__)
logging.basicConfig(
    format='format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"',
    filename='logs/app.log', encoding='utf-8', level="DEBUG"
)

# Parse command line arguments
parser = argparse.ArgumentParser(description="LLM parameters")
parser.add_argument("--model", type=str, default="qwen3:8b")
parser.add_argument("--temperature", type=float, default=0.7)
args = parser.parse_args()

# Load model interface
model = ChatOllama(
    model=args.model,
    temperature=args.temperature,
)

# Define the chat prompt template
prompt_template = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="system_prompt"),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Node to summarize all results
def summarize_node(state: MessagesState) -> dict:
    # create prompt with all abstracts
    prompt = "Here are some recent AI papers:\n\n"
    for id, paper in enumerate(papers):
        prompt += f"- Paper ID: {id}\n"
        prompt += f"- Title: {paper.title}\n"
        prompt += f"- Abstract: {paper.summary}\n"
        prompt += f"{'-'*10}\n"
    prompt += "\nProvide the requested summary."
    logger.info(f"Prompt to model: {prompt}")

    # prompt the model
    messages = state["messages"] + [HumanMessage(content=prompt)]
    prompt = prompt_template.invoke({
        "system_prompt": [SystemMessage(content=SYSTEM_PROMPT_SUMMARY)],
        "messages": messages
    })
    response = model.invoke(prompt)
    logger.info(f"Model response: {response}")

    return {"messages": response}

# Define the agent graph
workflow = StateGraph(state_schema=MessagesState)
workflow.add_node("summarize_node", summarize_node)
workflow.add_edge(START, "summarize_node")
workflow.add_edge("summarize_node", END)
agent = workflow.compile()

# Run the agent
# get new papers from arXiv
papers = fetch_papers_list()
logger.info(f"Fetched {len(papers)} new papers from arXiv.")

initial_state = {"messages": []}
final_state = agent.invoke(initial_state)

# Parse and enhance the summary
summary = parse_summary(final_state["messages"][-1].content)
summary = add_paper_links(summary, papers)

# Save summary to local file
filename = f"/Users/diogo/Desktop/AI-Summaries/AI-Summary ({datetime.date.today().strftime('%Y%m%d')}).md"
with open(filename, "w", encoding="utf-8") as f:
    f.write(summary)