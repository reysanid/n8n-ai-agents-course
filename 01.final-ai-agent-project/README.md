# Daily Digest: Smart Daily Newsletter

An automated n8n workflow that fetches new articles from designboom (a design and architecture news source), summarizes each one in Persian using a local language model, and sends the summary to the user on Telegram.

## What it does

1. Every day at 10:00, the workflow checks the designboom RSS feed and runs if there is a new article.
2. The article title and text are passed to a local LLM with a defined prompt, which returns a 2-3 sentence summary in Persian.
3. The summary is sent to the user's Telegram chat.

## Workflow

RSS Feed Trigger → Basic LLM Chain (+ Ollama Chat Model) → Telegram (Send Message)

## Tech stack

- `n8n` running locally via `Docker`
- `Ollama` running natively on Windows, with the `[model name]` model
- RSS feed of designboom as the news source (free, no API key or registration)
- Telegram Bot for delivery

## Technical decisions

- **RSS instead of NewsAPI / GNews:** the official designboom RSS feed is free and needs no API key, registration, or payment.
- **Local Ollama instead of a cloud LLM (e.g. OpenAI):** sanctions made it impossible to buy or use the OpenAI API directly, so the model runs locally on my own machine.
- **Model choice:** I first installed `[first model]`, but it had problems when testing the nodes in n8n. I then switched to `[second model]`, which worked with the exercise requirements and supports Persian reasonably well.

## Challenges

- **Connecting Docker to Ollama:** n8n runs inside a Docker container while Ollama runs directly on the host, so `localhost` did not work. I solved this by using the special address `host.docker.internal`, which Docker provides for reaching the host machine.
- **Output language:** the source is in English but the summary should be in Persian. I rewrote the prompt in the `Basic LLM Chain` node so that the Persian-language instruction is repeated at the beginning and at the end, which clearly improved the results. I also added instructions to keep the summary short, as the first outputs were too long.

## Known limitations

- Some messages are still sent in English instead of Persian, and those English ones are not summarized. A small local model is less consistent at following the language instruction.
- Telegram is filtered in Iran, so a VPN connection is needed to send messages.

## Result

The system runs without any external API. The workflow is published and active.

## Screenshots

(to be added)
