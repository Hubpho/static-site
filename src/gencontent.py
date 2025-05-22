import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node


def generate_pages_recursive(
    dir_path_content: str,
    template_path: str,
    dest_dir_path: str,
    base_path: str = "/",
) -> None:
    """Walk the /content tree and render every Markdown file to HTML."""
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)

        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, str(dest_path), base_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, base_path)


def generate_page(
    from_path: str,
    template_path: str,
    dest_path: str,
    base_path: str = "/",
) -> None:
    print(f" • {from_path} → {dest_path}")

    with open(from_path, "r") as f:
        markdown_content = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    html       = markdown_to_html_node(markdown_content).to_html()
    title      = extract_title(markdown_content)

    page_html = (
        template.replace("{{ Title }}", title)
                .replace("{{ Content }}", html)
                .replace('href="/', f'href="{base_path}')
                .replace('src="/',  f'src="{base_path}')
    )

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(page_html)


def extract_title(md: str) -> str:
    """Return the first H1 line (e.g. '# My Post' → 'My Post')."""
    for line in md.splitlines():
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")
