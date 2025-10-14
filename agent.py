import argparse
import logging
import datetime
from typing import TypedDict
from os import getenv

from langchain_openai import ChatOpenAI
from langgraph.graph import START, END, MessagesState, StateGraph
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage

from prompts import SYSTEM_PROMPT, SUMMARY_PROMPT, WHY_IT_MATTERS_PROMPT, OUTOFTHEBOX_PROMPT, LINERS_PROMPT
from examples import EXAMPLE_SUMMARY, EXAMPLE_WHY_IT_MATTERS, EXAMPLE_OUTOFTHE_BOX, EXAMPLE_LINERS
from utils import fetch_papers_list, parse_summary, add_paper_links

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"',
    filename='logs/app.log', encoding='utf-8', level="DEBUG"
)

# Parse command line arguments
parser = argparse.ArgumentParser(description="LLM parameters")
parser.add_argument("--model", type=str, default="google/gemma-3-4b-it:free")
parser.add_argument("--temperature", type=float, default=0.7)
args = parser.parse_args()

# Load model interface
model = ChatOpenAI(
    api_key=getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    model=args.model,
    temperature=args.temperature,
)

# Define the chat prompt template
prompt_template = ChatPromptTemplate.from_messages(
    [
        #SystemMessage(content=SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="messages", n_messages=1),
    ]
)

# Graph state
class State(TypedDict):
    summary: str
    why_it_matters: str
    out_of_the_box: str
    liners: str
    combined_output: str

# Nodes
def summarize_node(state: State) -> dict:
    prompt = SUMMARY_PROMPT.format(
        example=EXAMPLE_SUMMARY,
        papers=papers_prompt
    )

    logger.info(f"Prompt to model: {prompt}")

    messages = [HumanMessage(content=prompt)]
    prompt = prompt_template.invoke({"messages": messages})
    response = model.invoke(prompt)
    logger.info(f"Model response: {response}")
    return {"summary": response.content.strip()}

def why_it_matters_node(state: State) -> dict:
    prompt = WHY_IT_MATTERS_PROMPT.format(
        example=EXAMPLE_WHY_IT_MATTERS,
        papers=papers_prompt
    )

    logger.info(f"Prompt to model: {prompt}")

    messages = [HumanMessage(content=prompt)]
    prompt = prompt_template.invoke({"messages": messages})
    response = model.invoke(prompt)
    logger.info(f"Model response: {response}")
    return {"why_it_matters": response.content.strip()}

def outofthebox_node(state: State) -> dict:
    prompt = OUTOFTHEBOX_PROMPT.format(
        example=EXAMPLE_OUTOFTHE_BOX,
        papers=papers_prompt
    )

    logger.info(f"Prompt to model: {prompt}")

    messages = [HumanMessage(content=prompt)]
    prompt = prompt_template.invoke({"messages": messages})
    response = model.invoke(prompt)
    logger.info(f"Model response: {response}")
    return {"out_of_the_box": response.content.strip()}

def liners_node(state: State) -> dict:
    prompt = LINERS_PROMPT.format(
        example=EXAMPLE_LINERS,
        papers=papers_prompt
    )

    logger.info(f"Prompt to model: {prompt}")

    messages = [HumanMessage(content=prompt)]
    prompt = prompt_template.invoke({"messages": messages})
    response = model.invoke(prompt)
    logger.info(f"Model response: {response}")
    return {"liners": response.content.strip()}

def aggregator_node(state: State) -> dict:
    combined = f"### 🤖 AI Newsletter ({datetime.date.today()}):\n{state['summary']}\n\n---\n\n"
    combined += f"### 🔹 AI Engineering - Why it Matters:\n{state['why_it_matters']}\n\n---\n\n"
    combined += f"### 🔸 AI Engineering - Out-of-the-Box Ideas:\n{state['out_of_the_box']}\n\n---\n\n"
    combined += f"### 📜 Paper Summaries:\n{state['liners']}\n"
    return {"combined_output": combined.strip()}

# Define the agent graph
workflow = StateGraph(state_schema=State)
workflow.add_node("summarize_node", summarize_node)
workflow.add_node("why_it_matters_node", why_it_matters_node)
workflow.add_node("outofthebox_node", outofthebox_node)
workflow.add_node("liners_node", liners_node)
workflow.add_node("aggregator_node", aggregator_node)

workflow.add_edge(START, "summarize_node")
workflow.add_edge(START, "why_it_matters_node")
workflow.add_edge(START, "outofthebox_node")
workflow.add_edge(START, "liners_node")
workflow.add_edge("summarize_node", "aggregator_node")
workflow.add_edge("why_it_matters_node", "aggregator_node")
workflow.add_edge("outofthebox_node", "aggregator_node")
workflow.add_edge("liners_node", "aggregator_node")
workflow.add_edge("aggregator_node", END)
agent = workflow.compile()

# Get new papers from arXiv
papers = fetch_papers_list()
logger.info(f"Fetched {len(papers)} new papers from arXiv.")
papers_prompt = ""
for id, paper in enumerate(papers):
    id += 1
    papers_prompt += f"- Paper ID: {id}\n"
    papers_prompt += f"- Title: {paper.title}\n"
    papers_prompt += f"- Abstract: {paper.summary}\n"
    papers_prompt += f"{'-'*100}\n"

# Run the agent
state = agent.invoke({})

# Parse and enhance the summary
output = add_paper_links(state["combined_output"], papers)

# Save summary to local file
filename = f"./AI-Summaries/AI-Summary ({datetime.date.today().strftime('%Y%m%d')}).md"
with open(filename, "w", encoding="utf-8") as f:
    f.write(output)