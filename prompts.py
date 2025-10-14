SYSTEM_PROMPT = """You are a helpful assistant. You follow the user's instructions carefully to the last letter. You always answer in Markdown format."""

SUMMARY_PROMPT = """
The following are several title and abstracts from recent AI papers (each with a unique ID). Your task is to summarize them into a concise summary.

Here are some rules to follow:
- Summary is a single paragraph.
- Focus on the main contributions and findings of the papers.
- Highlight relationships between papers if applicable.
- Each mention of a paper MUST BE clearly linked to its unique ID within brackets.

Here is an example of a good summary:
{example}

Here are the papers to summarize:
{papers}

Please provide the summary below WITH NO PREAMBLE OR INTRODUCTION:
"""

WHY_IT_MATTERS_PROMPT = """
The following are several title and abstracts from recent AI papers (each with a unique ID). Your task is to explain why the advancements in these papers matter specifically to an AI Engineer in the industry setting.

Here are some rules to follow:
- Explanation is a single paragraph.
- Keep it concise, no more than 10 sentences FOR ALL PAPERS TOGETHER.
- Do not mention or reference any paper in particular, but rather focus on the collective impact of these advancements.
- Focus on practical implications and applications.

Here is an example of a good explanation:
{example}

Here are the papers to consider:
{papers}

Please provide the explanation below WITH NO PREAMBLE OR INTRODUCTION:
"""

OUTOFTHEBOX_PROMPT = """
The following are several title and abstracts from recent AI papers (each with a unique ID). Your task is to brainstorm a creative, out-of-the-box application idea that leverages the advancements in these papers.

Here are some rules to follow:
- Keep it concise, no more than 2-3 sentences.
- Think creatively about how these advancements could be applied in novel ways.
- Ensure the idea is feasible with current technology.
- Avoid generic ideas; be specific.
- Make sure to reference the papers by their unique IDs within brackets.

Here is an example of a good idea:
{example}

Here are the papers to consider:
{papers}

Please provide the idea below WITH NO PREAMBLE OR INTRODUCTION:
"""

LINERS_PROMPT = """
The following are several title and abstracts from recent AI papers (each with a unique ID). Your task is to generate a list of concise, one-liner descriptions for each paper in bullet points.

Here are some rules to follow:
- Each description should be a single sentence in a single bullet point.
- Focus on the main contribution or finding of the paper.
- Each description MUST BE clearly linked to its unique ID within brackets.

Here is an example of good one-liners:
{example}

Here are the papers to describe:
{papers}

Please provide the one-liners below WITH NO PREAMBLE OR INTRODUCTION:
"""