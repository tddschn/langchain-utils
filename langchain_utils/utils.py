#!/usr/bin/env python3

from typing import TYPE_CHECKING, Callable
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
    return f', Page {metadata["page_number"]}/{metadata["total_pages"]}'


def deliver_prompts(
    what: str,
    docs: list['Document'],
    should_be_only_one_doc: bool = False,
    needs_splitting: bool = False,
    copy: bool = True,
    chunk_size: int = 2000,
    extra_chunk_info_fn: Callable[['Document'], str] = lambda doc: '',
    dry_run: bool = False,
):
    from langchain.prompts import PromptTemplate

    def deliver_single_doc(document: 'Document'):
        prompt = PromptTemplate.from_template(REPLY_OK_IF_YOU_READ_TEMPLATE)
        content = document.page_content
        formatted_prompt = prompt.format(what=what, content=content)
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
        for i, doc in enumerate(documents):
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
        splitted = splitter.split_documents(docs)
        num_chunks = len(splitted)
        deliver_multiple_docs(splitted)

    elif should_be_only_one_doc:
        deliver_single_doc(docs[0])
    else:
        deliver_multiple_docs(docs)
