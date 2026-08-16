from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET


README_PATH = Path("README.md")
README_START = "<!-- BLOG-POST-LIST:START -->"
README_END = "<!-- BLOG-POST-LIST:END -->"
RSS_URL = "https://shangzongyu.github.io/index.xml"
POST_LIMIT = 5


@dataclass
class Post:
    title: str
    date: datetime
    url: str


def _local(tag: str) -> str:
    """Strip an XML namespace: '{http://...}title' -> 'title'."""
    return tag.rsplit("}", 1)[-1]


def _child_text(element: ET.Element, name: str) -> str:
    for child in element:
        if _local(child.tag) == name and child.text:
            return child.text.strip()
    return ""


def _child_attr(element: ET.Element, name: str, attr: str) -> str:
    for child in element:
        if _local(child.tag) == name and child.get(attr):
            return child.get(attr).strip()
    return ""


def _escape_link_text(text: str) -> str:
    """Make a title safe to use as Markdown link text."""
    return (
        text.replace("\\", "\\\\")
        .replace("[", "\\[")
        .replace("]", "\\]")
        .replace("\n", " ")
        .strip()
    )


def parse_date(raw: str) -> datetime:
    raw = raw.strip()
    if not raw:
        raise ValueError("empty date")

    # RSS <pubDate> uses RFC 822/2822.
    try:
        parsed = parsedate_to_datetime(raw)
        if parsed:
            return parsed
    except (TypeError, ValueError):
        pass

    # Atom <updated>/<published> use ISO 8601.
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        pass

    raise ValueError(f"Unsupported date format: {raw}")


def fetch_feed(url: str) -> str:
    request = Request(url, headers={"User-Agent": "github-profile-blog-sync/1.0"})
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_feed(xml_text: str) -> list[Post]:
    root = ET.fromstring(xml_text)
    posts: list[Post] = []

    for element in root.iter():
        tag = _local(element.tag)
        if tag == "item":  # RSS 2.0
            title = _child_text(element, "title")
            url = _child_text(element, "link")
            date_raw = _child_text(element, "pubDate")
        elif tag == "entry":  # Atom
            title = _child_text(element, "title")
            url = _child_attr(element, "link", "href")
            date_raw = _child_text(element, "updated") or _child_text(element, "published")
        else:
            continue

        if not title or not url:
            continue

        try:
            date = parse_date(date_raw)
        except ValueError:
            continue

        posts.append(Post(title=title, date=date, url=url))

    posts.sort(key=lambda post: post.date.timestamp(), reverse=True)
    return posts[:POST_LIMIT]


def render_posts(posts: list[Post]) -> str:
    if not posts:
        lines = ["- No posts found."]
    else:
        lines = [
            f"- [{_escape_link_text(post.title)}]({post.url}) · {post.date.strftime('%Y-%m-%d')}"
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
    xml_text = fetch_feed(RSS_URL)
    posts = parse_feed(xml_text)
    block = render_posts(posts)
    update_readme(block)


if __name__ == "__main__":
    main()
