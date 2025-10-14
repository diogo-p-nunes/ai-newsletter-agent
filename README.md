# ai-newsletter-agent
AI Newsletter Agent that sends summarized info on new paper releases on arXiv. Based on OpenRouter

### Create conda environment and install dependencies

```bash
conda create -n "ainews" python=3.12
conda activate ainews
pip install -r requirements.txt
```

### Example usage

The following should take only a few seconds (~3s).

```bash
OPENROUTER_API_KEY=<OPENROUTER_API_KEY> time python agent.py --model google/gemma-3-4b-it:free
```