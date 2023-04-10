#!/usr/bin/env python3

from typing import TYPE_CHECKING, Callable, NoReturn
import sys
from .prompts import (
    REPLY_OK_IF_YOU_READ_TEMPLATE,
    REPLY_OK_IF_YOU_READ_TEMPLATE_SPLITTED_FIRST,
    REPLY_OK_IF_YOU_READ_TEMPLATE_SPLITTED_CONTINUED,
)


if TYPE_CHECKING:
    from datetime import datetime
    from langchain.docstore.document import Document


def get_token_count(s: str, model_name: str = 'gpt-3.5-turbo') -> int:
    from tiktoken import encoding_for_model

    enc = encoding_for_model(model_name)
    tokenized_text = enc.encode(s)

    # calculate the number of tokens in the encoded text
    return len(tokenized_text)


def get_word_count(s: str) -> int:
    return len(s.split())


def format_date(dt: 'datetime') -> str:
    return dt.strftime('%Y-%m-%d')


def pymupdf_doc_page_info(document: 'Document') -> str:
    metadata = document.metadata
    if 'page_number' in metadata:
        return f', Page {metadata["page_number"]}/{metadata["total_pages"]}'
    else:
        return ''


def url_source_info(document: 'Document') -> str:
    metadata = document.metadata
    if 'source' in metadata:
        return f', URL: {metadata["source"]}'
    else:
        return ''


def save_str_to_tempfile(s: str, suffix: str = '.txt') -> str:
    import tempfile

    with tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False) as f:
        f.write(s)
        return f.name


def open_file(path: str):
    # if on macOS, open with default app
    if sys.platform == 'darwin':
        import subprocess

        subprocess.call(('open', path))
    # if on Linux, open with default app
    elif sys.platform.startswith('linux'):
        import subprocess

        subprocess.call(('xdg-open', path))
    # if on Windows, open with default app
    elif sys.platform == 'win32':
        import os

        os.startfile(path)
    else:
        raise NotImplementedError(f'Unsupported platform: {sys.platform}')


def deliver_prompts(
    what: str,
    documents: list['Document'],
    should_be_only_one_doc: bool = False,
    needs_splitting: bool = False,
    copy: bool = True,
    edit: bool = False,
    chunk_size: int = 2000,
    extra_chunk_info_fn: Callable[['Document'], str] = lambda doc: '',
    dry_run: bool = False,
    parts: list[int] | None = None,
):
    from langchain.prompts import PromptTemplate

    def deliver_single_doc(document: 'Document'):
        prompt = PromptTemplate.from_template(REPLY_OK_IF_YOU_READ_TEMPLATE)
        content = document.page_content
        formatted_prompt = prompt.format(what=what, content=content)

        def edit_prompt(formatted_prompt: str = formatted_prompt):
            formatted_prompt_path = save_str_to_tempfile(
                formatted_prompt, suffix='.txt'
            )
            open_file(formatted_prompt_path)
            print(
                f'Please edit the prompt at {formatted_prompt_path} and copy it yourself.',
                file=sys.stderr,
            )
            return

        if edit and not dry_run:
            edit_prompt()
            return
        if copy:
            print(
                f'Word Count: {get_word_count(formatted_prompt)}, Char count: {len(formatted_prompt)}{extra_chunk_info_fn(document)}',
                file=sys.stderr,
            )
            if not dry_run:
                import pyperclip

                pyperclip.copy(formatted_prompt)
                print('Prompt copied to clipboard.', file=sys.stderr)
        else:
            print(formatted_prompt)

    def deliver_multiple_docs(documents: list['Document']):
        if edit:
            print(f'Please copy the prompts after each edits.', file=sys.stderr)
        for i, doc in enumerate(documents):
            num_chunks = len(documents)
            if i == 0:
                prompt = PromptTemplate.from_template(
                    REPLY_OK_IF_YOU_READ_TEMPLATE_SPLITTED_FIRST
                )
            else:
                prompt = PromptTemplate.from_template(
                    REPLY_OK_IF_YOU_READ_TEMPLATE_SPLITTED_CONTINUED
                ).partial(x=str(i + 1))
            content = doc.page_content
            formatted_prompt = prompt.format(what=what, content=content)
            if dry_run:
                print(
                    f'Press Enter to copy prompt {i+1}/{num_chunks}. Word Count: {get_word_count(formatted_prompt)}, Char count: {len(formatted_prompt)}{extra_chunk_info_fn(doc)}: '
                )
                continue
            if edit:
                input(
                    f'Press Enter to edit prompt {i+1}/{num_chunks}. Word Count: {get_word_count(formatted_prompt)}, Char count: {len(formatted_prompt)}{extra_chunk_info_fn(doc)}: '
                )
                formatted_prompt_path = save_str_to_tempfile(
                    formatted_prompt, suffix='.txt'
                )
                open_file(formatted_prompt_path)
                continue
            input(
                f'Press Enter to copy prompt {i+1}/{num_chunks}. Word Count: {get_word_count(formatted_prompt)}, Char count: {len(formatted_prompt)}{extra_chunk_info_fn(doc)}: '
            )
            import pyperclip

            pyperclip.copy(formatted_prompt)

    if dry_run:
        print(
            f'Dry running. Nothing will be copied to your clipboard, and you don'
            't need to press Enter to move forward.'
        )
    if needs_splitting:
        from langchain.text_splitter import TokenTextSplitter

        splitter = TokenTextSplitter(encoding_name='cl100k_base', chunk_size=chunk_size)
        splitted = splitter.split_documents(documents)
        if parts:
            len_splitted = len(splitted)
            parts = list({part for part in parts if 0 <= part - 1 < len_splitted})
            print(
                f'Selecting {len(parts)} parts out of {len_splitted}.', file=sys.stderr
            )
            print(f'Using parts: {parts}', file=sys.stderr)
            splitted = [splitted[i - 1] for i in parts]
        deliver_multiple_docs(splitted)

    elif should_be_only_one_doc:
        deliver_single_doc(documents[0])
    else:
        deliver_multiple_docs(documents)


def assert_never(a: NoReturn) -> NoReturn:
    raise RuntimeError("Should not get here")
