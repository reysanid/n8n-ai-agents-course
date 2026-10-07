# FAQ Semantic Search Agent

An intelligent FAQ system built with `n8n` that answers user questions using semantic search rather than exact keyword matching.

## What it does

1. A CSV file with 10 question–answer pairs is converted into vector embeddings and stored in an in-memory `vector store`.
2. When a user submits a question through a form, that question is embedded the same way and used to search the vector store for the closest match **by meaning**, not by exact wording.
3. The matching record's answer is pulled from its metadata and shown back to the user.

## Tech stack

- `n8n` running locally via `Docker`
- `Ollama` (`nomic-embed-text`, running natively on Windows) for embeddings — used instead of OpenAI's API because of Iran sanctions and no access to an international card
- In-memory `Simple Vector Store` node for storage and retrieval

## Architecture

**Ingestion branch:** Read CSV → Extract from File → Embeddings (Ollama) → Simple Vector Store (Insert)

**Retrieval branch:** Form submission → Embeddings (Ollama) → Simple Vector Store (Get Many) → Edit Fields (display answer)

## Challenges along the way

This was my first time working with `n8n` nodes and building a real AI Agent, and it took far longer and was far more challenging than I expected. I hit several serious, back-to-back bugs — each one on its own could have broken the whole output — and at one point set the exercise aside to work on the course's final project first. Returning to it afterward with a few more concepts understood is what let me finish it.

1. **Broken canvas connections** — some nodes couldn't be wired together; the issue traced back to incorrect settings on the nodes themselves, not the canvas.
2. **Mismatched Memory Keys** — the node that inserted data into the vector store and the node used for retrieval were pointing at two different Memory Keys, so they were effectively writing to and reading from two separate stores. Retrieval always came back empty, with no error shown.
3. **A typo in an Expression** — `{{ json.answer$ }}` instead of `{{ $json.answer }}` in the metadata field, which silently made every stored answer `undefined`. This one took a long time to trace.
4. **Wrong path in the final node** — even after the above fixes, the `Edit Fields` node was reading from the wrong place in the JSON structure. The correct path turned out to be `$json.document.metadata.answer`, not what I had guessed.
5. **In-memory store is temporary** — because the vector store is in-memory, every time the `n8n` container restarted (which happened several times during this exercise), all stored data was wiped and the ingestion branch had to be re-run. This was confusing at first because I assumed the problem was elsewhere.

## What I learned

Working with `n8n`, especially with AI Agents and vector stores, requires attention at three levels at once: the visual connections on the canvas, each node's internal settings (like Memory Key), and the exact syntax of every expression — because one small mistake (a misplaced character, a missing connection line) can break the entire chain without necessarily throwing a visible error.
