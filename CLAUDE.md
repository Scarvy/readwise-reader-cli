# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install in development mode
uv sync

# Run the CLI
uv run rw-cli --help

# Run tests
uv run pytest

# Lint
uv run ruff check .
uv run ruff format .
```

The `READER_API_TOKEN` environment variable must be set to make API calls. Set it in a `.env` file or export it in the shell.

## Architecture

The CLI is built with **Click** and structured as a single package under `src/readwise_reader_cli/`.

**Request flow for `list`:**
1. `commands.py` — parses CLI options, manages a JSON file cache at `~/.local/share/reader/library.json` (1-minute expiry). Cache key is `{location}_{category}_{update_after}`.
2. `api.py` — wraps the Reader API v3. `list_documents()` calls `_fetch_results()`, which paginates via `pageCursor` until exhausted. Rate limit retries are handled automatically.
3. `models.py` — Pydantic models: `ListParameters` (serializes to API query params via `updatedAfter`/`pageCursor` aliases), `DocumentInfo` (represents a document).
4. `layout.py` — renders output using **rich** as either a table (default) or list layout. Highlights/notes have a separate column layout.

**`lib` command** uses `data.py` which fetches the *entire* library (no filters) and caches it for 1 day at `~/.local/share/reader/full_library.json`.

**`upload` command** uses `reading_list/extractors.py` to parse HTML or CSV reading list exports, then `utils.batch_add_documents()` to add them with a rich progress bar.

## Key design notes

- `--update-after` defaults to `None` (no filter). When omitted, the API returns all documents for the given location. Use `--date-range [today|week|month]` for relative filtering.
- The cache appends a `{"time": "..."}` sentinel as the last element of each cached list — code that iterates results must slice it off with `[:-1]`.
- `VALID_CATEGORY_OPTIONS` in `constants.py` is the source of truth for allowed categories; `constants.py` and `models.py`'s `CategoryEnum` must stay in sync.
