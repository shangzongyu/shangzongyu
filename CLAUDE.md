
This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a GitHub profile repository (`shangzongyu/shangzongyu`) — the special repo whose `README.md` is displayed on the GitHub profile page. It contains:

- `README.md` — the profile page rendered by GitHub
- `code.gif` — animation used in the README
- `scripts/update_readme_from_hugo.py` — script that syncs latest blog posts into the README

## Blog Post Sync Script

The script `scripts/update_readme_from_hugo.py` reads Hugo markdown posts from `blog_repo/content/posts/` (a sibling checkout cloned at runtime by CI), parses YAML front matter, sorts posts by date, and rewrites the `<!-- BLOG-POST-LIST:START -->` / `<!-- BLOG-POST-LIST:END -->` block in `README.md`.

Run it manually (requires `blog_repo/` to exist):
```bash
python scripts/update_readme_from_hugo.py
```

Key constants in the script:
- `POSTS_DIR = Path("blog_repo/content/posts")` — source of Hugo posts
- `BLOG_BASE_URL = "https://shangzongyu.github.io"` — base URL for post links
- `POST_LIMIT = 5` — number of latest posts shown
