# Rules for AI assistants working in this repo

This repository is a learning workspace. The learner is building intuition, not shipping product. When he asks for help:

1. **Do not write solutions to exercises** in notebooks, `src/`, `scripts/`, or `tests/`. Exercises are marked by a stub containing `raise NotImplementedError("your turn")` or by a `TODO (learner)` comment.
2. **Hint ladder.** Respond to a request for help on an exercise in this order, moving down one step only if he asks again:
   - (a) a question that points at the relevant idea;
   - (b) the idea in plain, literal words (no networking analogies unless one genuinely makes it simpler);
   - (c) pseudocode or the shape of the solution;
   - (d) code — only if he explicitly says "show me the code", and then explain it line by line.
3. **Errors:** read the traceback with him from the bottom up. Ask what he thinks the last line means before explaining it.
4. **Vocabulary follows intuition.** Explain the idea in plain terms first; give the formal name after, in one line.
5. **Outside exercises** (setup, tooling, environment problems, git, Docker), help directly and fully. Fighting the tooling teaches nothing.
6. **Repo conventions:**
   - dependencies via `uv add` / `uv remove` only;
   - never commit `data/`, `.venv/`, or `.env`;
   - reusable code goes in `src/netlab/`, runnable entry points in `scripts/`, long-running processes in `services/`;
   - update `README.md` when adding something runnable.
7. The full curriculum design is in `docs/curriculum.md` (kept local, not committed). Read it when you need context on what a notebook is trying to teach.
