#!/usr/bin/env python3
from typing import TYPE_CHECKING, Callable, NoReturn
import sys
from .prompts import (
    RAW_TEMPLATE,
    RAW_TRIPLE_QUOTES_TEMPLATE,
    REPLY_OK_IF_YOU_READ_TEMPLATE,
    REPLY_OK_IF_YOU_READ_TEMPLATE_SPLITTED_FIRST,
    REPLY_OK_IF_YOU_READ_TEMPLATE_SPLITTED_CONTINUED,
)

if TYPE_CHECKING:
    from datetime import datetime
    from langchain.docstore.document import Document


def convert_str_slice_notation_to_slice(str_slice: str) -> slice:
    # '1:3' -> slice(1, 3)
    # '1:' -> slice(1, None)
    # ':3' -> slice(None, 3)
    # ':' -> slice(None, None)
    # '3' -> slice(3)
    # '1:8:2' -> slice(1, 8, 2)
    # start

    def int_or_none(s: str) -> int | None:
        try:
            return int(s)
        except ValueError:
            return None

    return slice(*list(map(int_or_none, str_slice.split(":"))))
    # if str_slice.startswith(':'):
    #     start = None
    # else:
    #     start = int(str_slice.split(':')[0])
    # # stop
    # if str_slice.endswith(':'):
    #     stop = None
    # else:
    #     try:
    #         stop = int(str_slice.split(':')[1])
    #     except IndexError:
    #         stop = None
    # # step
    # if len(str_slice.split(':')) == 3:
    #     step = int(str_slice.split(':')[-1])
    # else:
    #     step = None
    # return slice(start, stop, step)


def get_token_count(s: str, model_name: str = "gpt-3.5-turbo") -> int:
    from tiktoken import encoding_for_model

    enc = encoding_for_model(model_name)
    tokenized_text = enc.encode(s)
    # calculate the number of tokens in the encoded text
    return len(tokenized_text)


def get_word_count(s: str) -> int:
    return len(s.split())


def format_date(dt: "datetime") -> str:
    return dt.strftime("%Y-%m-%d")


def pymupdf_doc_page_info(document: "Document") -> str:
    metadata = document.metadata
    total_pages_in_metadata = "total_pages" in metadata
    if "page_number" in metadata and total_pages_in_metadata:
        return f", Page {metadata['page_number']}/{metadata['total_pages']}"
    elif "page" in metadata and total_pages_in_metadata:
        return f", Page {metadata['page'] + 1}/{metadata['total_pages']}"
    else:
        return ""


def html_source_info(document: "Document") -> str:
    metadata = document.metadata
    if "source" in metadata:
        return f", Title: {metadata['title']}, Source: {metadata['source']}"
    else:
        return ""


def general_document_source_info(document: "Document") -> str:
    metadata = document.metadata
    if "source" in metadata:
        return f", Source: {metadata['source']}"
    else:
        return ""


def save_str_to_tempfile(s: str, suffix: str = ".txt") -> str:
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=suffix, delete=False) as f:
        f.write(s)
        return f.name


def open_file(path: str):
    # if on macOS, open with default app
    if sys.platform == "darwin":
        import subprocess

        subprocess.call(("open", path))
    # if on Linux, open with default app
    elif sys.platform.startswith("linux"):
        import subprocess

        subprocess.call(("xdg-open", path))
    # if on Windows, open with default app
    elif sys.platform == "win32":
        import os

        os.startfile(path)
    else:
        raise NotImplementedError(f"Unsupported platform: {sys.platform}")


def deliver_prompts(
    what: str,
    documents: list["Document"],
    should_be_only_one_doc: bool = False,
    needs_splitting: bool = False,
    copy: bool = True,
    edit: bool = False,
    chunk_size: int = 2000,
    extra_chunk_info_fn: Callable[["Document"], str] = lambda doc: "",
    dry_run: bool = False,
    parts: list[int] | None = None,
    raw_triple_quotes: bool = False,
    raw: bool = False,
    out: str | None = None,
):
    from langchain.prompts import PromptTemplate
    from langchain.text_splitter import TokenTextSplitter
    import pyperclip

    if dry_run:
        print(
            "Dry running. Prompts will be described but not delivered.", file=sys.stderr
        )
    if needs_splitting:
        splitter = TokenTextSplitter(encoding_name="cl100k_base", chunk_size=chunk_size)
        documents = splitter.split_documents(documents)
        if parts:
            len_splitted = len(documents)
            valid_parts = [p for p in parts if 1 <= p <= len_splitted]
            print(
                f"Selecting {len(valid_parts)} parts out of {len_splitted}.",
                file=sys.stderr,
            )
            print(f"Using parts: {valid_parts}", file=sys.stderr)
            documents = [documents[i - 1] for i in valid_parts]
    if out:
        all_parts = []
        for doc in documents:
            content = doc.page_content
            # For file output, the default is to just use the content, without prompt framing.
            # We still respect --raw (`raw_triple_quotes`) if specified.
            if raw_triple_quotes:
                # Corresponds to RAW_TRIPLE_QUOTES_TEMPLATE
                formatted_part = f'"""\n{content}\n"""'
            else:
                # This covers the default case for file output and --raw-no-quotes (`raw`)
                formatted_part = content
            all_parts.append(formatted_part)
        # Join all parts with '---' on its own line
        final_output = "\n---\n".join(all_parts)
        with open(out, "w") as f:
            f.write(final_output)
        print(f"Successfully wrote {len(all_parts)} part(s) to {out}.", file=sys.stderr)
        return  # Exit after writing to file
    # --- Refactored Interactive/Clipboard/stdout Logic ---
    num_docs = len(documents)
    for i, doc in enumerate(documents):
        if raw:
            template = RAW_TEMPLATE
        elif raw_triple_quotes:
            template = RAW_TRIPLE_QUOTES_TEMPLATE
        elif num_docs == 1:
            template = REPLY_OK_IF_YOU_READ_TEMPLATE
        elif i == 0:
            template = REPLY_OK_IF_YOU_READ_TEMPLATE_SPLITTED_FIRST
        else:
            template = REPLY_OK_IF_YOU_READ_TEMPLATE_SPLITTED_CONTINUED
        prompt_template = PromptTemplate.from_template(template)
        if i > 0 and num_docs > 1 and (not raw) and (not raw_triple_quotes):
            prompt_template = prompt_template.partial(x=str(i + 1))
        content = doc.page_content
        if raw or raw_triple_quotes:
            formatted_prompt = prompt_template.format(content=content)
        else:
            formatted_prompt = prompt_template.format(what=what, content=content)
        print(
            f"--- Prompt {i + 1}/{num_docs} --- Word Count: {get_word_count(formatted_prompt)}, Char count: {len(formatted_prompt)}{extra_chunk_info_fn(doc)}",
            file=sys.stderr,
        )
        if dry_run:
            continue
        if edit:
            prompt_path = save_str_to_tempfile(formatted_prompt, suffix=".txt")
            open_file(prompt_path)
            print(
                f"Prompt for part {i + 1} opened for editing at: {prompt_path}",
                file=sys.stderr,
            )
            if i < num_docs - 1:
                input("Press Enter to process the next part...")
        elif copy:
            pyperclip.copy(formatted_prompt)
            print(f"Prompt {i + 1}/{num_docs} copied to clipboard.", file=sys.stderr)
            if i < num_docs - 1:
                try:
                    input("Press Enter to copy the next part, or Ctrl+C to exit...")
                except (KeyboardInterrupt, EOFError):
                    print("\nExiting.", file=sys.stderr)
                    return
        else:
            print(formatted_prompt)
            if i < num_docs - 1:
                print("\n---\n")


def assert_never(a: NoReturn) -> NoReturn:
    raise RuntimeError("Should not get here")


def save_stdin_to_tempfile() -> str:
    # create a temp file and save stdin to it, and return the tempfile path
    import tempfile
    import shutil
    import sys

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        with open(temp_file.name, "w") as f:
            shutil.copyfileobj(sys.stdin, f)
        temp_file_path = temp_file.name
    return temp_file_path


def save_clipboard_to_tempfile() -> str:
    # create a temp file and save stdin to it, and return the tempfile path
    import tempfile
    import pyperclip

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        with open(temp_file.name, "w") as f:
            f.write(pyperclip.paste())
        temp_file_path = temp_file.name
    return temp_file_path


def get_percentage_non_ascii(s: str) -> float:
    return sum((1 for c in s if ord(c) >= 128)) / len(s)


def get_default_chunk_size(model: str | None = None) -> int:
    from langchain_utils.config import MODEL_TO_CONTEXT_LENGTH_MAPPING, DEFAULT_MODEL

    if model not in MODEL_TO_CONTEXT_LENGTH_MAPPING:
        model = DEFAULT_MODEL
    return MODEL_TO_CONTEXT_LENGTH_MAPPING[model] // 2


def extract_github_info(url: str) -> dict[str, str] | None:
    import re

    # Define a regular expression to match GitHub URLs
    pattern = (
        "^https?://github\\.com/([^/]+)/([^/]+)(?:/(?:tree|blob)/([^/]+)(?:/(.+))?)?$"
    )
    # Use the regular expression to extract the URL components
    match = re.match(pattern, url)
    if match:
        repo_owner = match.group(1)
        repo_name = match.group(2)
        revision = (
            match.group(3) or "master"
        )  # Use "main" as the default revision if not provided
        file_path = (
            match.group(4) or "README.md"
        )  # Use "README.md" as the default file path if not provided
        return {
            "repo_owner": repo_owner,
            "repo_name": repo_name,
            "revision": revision,
            "file_path": file_path,
        }
    return None


def get_github_file_raw_url(
    repo_owner: str,
    repo_name: str,
    revision: str = "master",
    file_path: str = "README.md",
):
    # Construct the raw URL for the README.md file
    raw_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/{revision}/{file_path}"
    return raw_url


def substack_html_to_md(html: str) -> str:
    # cSpell:disable
    from bs4 import BeautifulSoup
    from markdownify import markdownify as md

    # cSpell:enable
    # Parse the HTML content
    soup = BeautifulSoup(html, "html.parser")
    # Extract the title and the target div content
    title = soup.find("title").text if soup.find("title") else ""  # type: ignore
    target_div = soup.select_one("div.available-content > div")
    # Remove all sub-divs from the target div
    if target_div:
        for sub_div in target_div.find_all("div", recursive=True):
            sub_div.decompose()
    # Convert the title and the cleaned div content to Markdown
    markdown_content = (
        f"# {title}\n\n" + md(str(target_div), heading_style="ATX")
        if target_div
        else "# " + title
    )
    return markdown_content


def url_to_html(url: str) -> str:
    from urllib.request import urlopen
    from urllib.request import Request
    from langchain_utils.config import USER_AGENT_WINDOWS_CHROME

    # Create a request with the specified user agent
    req = Request(url, headers={"User-Agent": USER_AGENT_WINDOWS_CHROME})
    # Open the URL and read the HTML content
    with urlopen(req) as response:
        html_content = response.read().decode("utf-8")
    return html_content
