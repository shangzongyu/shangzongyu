
This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a GitHub profile repository (`shangzongyu/shangzongyu`) — the special repo whose `README.md` is displayed on the GitHub profile page. It contains:

- `README.md` — the profile page rendered by GitHub
- `code.gif` — animation used in the README
- `.github/workflows/update-readme-from-blog.yml` — GitHub Action that syncs latest blog posts into the README

## Blog Post Sync

The workflow `.github/workflows/update-readme-from-blog.yml` uses the [`gautamkrishnar/blog-post-workflow`](https://github.com/gautamkrishnar/blog-post-workflow) action to fetch the Hugo blog's RSS feed (`https://shangzongyu.github.io/index.xml`) and rewrite the `<!-- BLOG-POST-LIST:START -->` / `<!-- BLOG-POST-LIST:END -->` block in `README.md`.

Using the RSS feed means the links always match the live site's real permalinks and drafts are excluded automatically.

Key settings in the workflow:
- `feed_list` — `https://shangzongyu.github.io/index.xml`
- `max_post_count` — `5` (number of latest posts shown)
- schedule — every 6 hours (`0 */6 * * *`), plus `workflow_dispatch` for manual runs

> Note: GitHub requires the repository's Actions "Workflow permissions" to be set to **Read and write permissions** so the action can commit the README update.
