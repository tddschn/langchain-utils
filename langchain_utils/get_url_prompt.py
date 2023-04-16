#!/usr/bin/env python3
"""
Author : Xinyuan Chen <45612704+tddschn@users.noreply.github.com>
Date   : 2023-04-09
"""

import sys

from langchain_utils import __version__
from langchain_utils.utils import (
    deliver_prompts,
    get_word_count,
    deliver_prompts,
    general_document_source_info,
    get_default_chunk_size,
)
from langchain_utils.loaders import load_url
from langchain_utils.config import DEFAULT_URL_WHAT
from langchain_utils.utils_argparse import get_get_prompt_base_arg_parser


def get_args():
    """Get command-line arguments"""

    parser = get_get_prompt_base_arg_parser(
        description='Get a prompt consisting the text content of a webpage'
    )

    parser.add_argument('url', help='URL to the webpage', metavar='URL', type=str)
    parser.add_argument(
        '-w',
        '--what',
        help='Initial knowledge you want to insert before the PDF content in the prompt',
        type=str,
        default=DEFAULT_URL_WHAT,
    )
    parser.add_argument(
        '-M',
        '--merge',
        help='Merge contents of all pages before processing',
        action='store_true',
    )
    parser.add_argument(
        '-j',
        '--javascript',
        help='Use JavaScript to render the page',
        action='store_true',
    )

    args = parser.parse_args()
    args.chunk_size = get_default_chunk_size(args.model)
    return args


def main():
    """Make a jazz noise here"""

    args = get_args()

    print(f'Loading webpage from {args.url} ...', file=sys.stderr)
    docs = load_url(urls=[args.url], javascript=args.javascript)
    texts = [doc.page_content for doc in docs]
    all_text = '\n'.join(texts)
    word_count = get_word_count((all_text))
    print(
        f'Loaded {len(docs)} pages. Word count: {word_count} Char count: {len(all_text)}',
        file=sys.stderr,
    )
    if args.merge:
        from langchain.docstore.document import Document

        merged = Document(
            page_content=all_text,
            # metadata={
            #     k: v for k, v in docs[0].metadata.items() if k not in {'page_number'}
            # },
        )
    if args.no_split:
        needs_splitting = False
    if word_count > args.chunk_size * 0.75:
        needs_splitting = True
    else:
        needs_splitting = False
    deliver_prompts(
        what=args.what,
        documents=[merged] if args.merge else docs,  # type: ignore
        needs_splitting=needs_splitting,
        copy=args.copy,
        edit=args.edit,
        should_be_only_one_doc=True,
        chunk_size=args.chunk_size,
        extra_chunk_info_fn=general_document_source_info,
        dry_run=args.dry_run,
        raw_triple_quotes=args.raw,
        parts=args.parts,
    )


if __name__ == '__main__':
    main()
