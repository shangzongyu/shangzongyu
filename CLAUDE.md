
This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a GitHub profile repository (`shangzongyu/shangzongyu`) — the special repo whose `README.md` is displayed on the GitHub profile page. It contains:

- `README.md` — the profile page rendered by GitHub
- `code.gif` — animation used in the README
- `scripts/update_readme_from_hugo.py` — script that syncs latest blog posts into the README

## Blog Post Sync Script

The script `scripts/update_readme_from_hugo.py` fetches the Hugo blog's RSS feed (`https://shangzongyu.github.io/index.xml`), parses the latest posts (title, permalink, date), and rewrites the `<!-- BLOG-POST-LIST:START -->` / `<!-- BLOG-POST-LIST:END -->` block in `README.md`. Using the RSS feed means the links always match the live site's real permalinks and drafts are excluded automatically.

Run it manually (no local blog checkout required):
```bash
python scripts/update_readme_from_hugo.py
```

Key constants in the script:
- `RSS_URL = "https://shangzongyu.github.io/index.xml"` — source feed
- `README_START` / `README_END` — the markers delimiting the auto-generated block
- `POST_LIMIT = 5` — number of latest posts shown

The workflow `.github/workflows/update-readme-from-blog.yml` runs this on a schedule (every 6 hours) and commits any change.
