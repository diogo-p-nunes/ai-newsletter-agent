# ai-newsletter-agent
AI Newsletter Agent that sends summarized info on new paper releases on arXiv. Based on OpenRouter.

### Create conda environment and install dependencies

```bash
conda create -n "ainews" python=3.12
conda activate ainews
pip install -r requirements.txt
```

### Example usage

```bash
export OPENROUTER_API_KEY=<OPENROUTER_API_KEY>
export TELEGRAM_BOT_TOKEN=<TELEGRAM_BOT_TOKEN>
export TELEGRAM_USER_ID=<TELEGRAM_USER_ID>
python main.py
```