from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from urllib.parse import quote


README_PATH = Path("README.md")
POSTS_DIR = Path("blog_repo/content/posts")
README_START = "<!-- BLOG-POST-LIST:START -->"
README_END = "<!-- BLOG-POST-LIST:END -->"
BLOG_BASE_URL = "https://shangzongyu.github.io"
POST_LIMIT = 5


@dataclass
class Post:
    title: str
    date: datetime
    url: str


def parse_front_matter(content: str) -> dict[str, str]:
    if not content.startswith("---\n"):
        return {}

    parts = content.split("---\n", 2)
    if len(parts) < 3:
        return {}

    front_matter = parts[1]
    data: dict[str, str] = {}

    for line in front_matter.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("\"'")

    return data


def parse_date(raw: str) -> datetime:
    raw = raw.strip()
    formats = (
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
    )

    normalized = raw.replace("Z", "+0000")
    for fmt in formats:
        try:
            if fmt == "%Y-%m-%dT%H:%M:%SZ":
                return datetime.strptime(raw, fmt)
            return datetime.strptime(normalized, fmt)
        except ValueError:
            continue

    raise ValueError(f"Unsupported date format: {raw}")


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"[^a-z0-9\-\u4e00-\u9fff]", "", text)
    return quote(text)


def build_post_url(meta: dict[str, str], file_path: Path) -> str:
    slug = meta.get("slug") or meta.get("url") or file_path.stem

    if slug.startswith("http://") or slug.startswith("https://"):
        return slug

    if slug.startswith("/"):
        return f"{BLOG_BASE_URL}{slug}"

    if "/" in slug:
        return f"{BLOG_BASE_URL}/{slug.strip('/')}/"

    return f"{BLOG_BASE_URL}/posts/{slugify(slug)}/"


def collect_posts() -> list[Post]:
    posts: list[Post] = []

    for path in POSTS_DIR.rglob("*.md"):
        content = path.read_text(encoding="utf-8")
        meta = parse_front_matter(content)
        title = meta.get("title")
        date_raw = meta.get("date")

        if not title or not date_raw:
            continue

        try:
            date = parse_date(date_raw)
        except ValueError:
            continue

        posts.append(
            Post(
                title=title,
                date=date,
                url=build_post_url(meta, path),
            )
        )

    posts.sort(key=lambda item: item.date, reverse=True)
    return posts[:POST_LIMIT]


def render_posts(posts: list[Post]) -> str:
    if not posts:
        lines = ["- No posts found."]
    else:
        lines = [
            f"- [{post.title}]({post.url}) · {post.date.strftime('%Y-%m-%d')}"
            for post in posts
        ]

    return "\n".join(
        [
            README_START,
            *lines,
            README_END,
        ]
    )


def update_readme(block: str) -> None:
    content = README_PATH.read_text(encoding="utf-8")

    start_index = content.find(README_START)
    end_index = content.find(README_END)
    if start_index == -1 or end_index == -1:
        raise RuntimeError("README markers not found")

    end_index += len(README_END)
    updated = content[:start_index] + block + content[end_index:]
    README_PATH.write_text(updated, encoding="utf-8")


def main() -> None:
    posts = collect_posts()
    block = render_posts(posts)
    update_readme(block)


if __name__ == "__main__":
    main()
