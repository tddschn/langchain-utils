#!/usr/bin/env python3
"""
Author : Xinyuan Chen <45612704+tddschn@users.noreply.github.com>
Date   : 2023-04-09
"""

import sys

from . import __version__
from .utils import (
    deliver_prompts,
    get_word_count,
    deliver_prompts,
    general_document_source_info,
    save_stdin_to_tempfile,
    save_clipboard_to_tempfile,
)
from .loaders import load_text
from .config import DEFAULT_GENERAL_WHAT
from .utils_argparse import get_get_prompt_base_arg_parser


def get_args():
    """Get command-line arguments"""

    parser = get_get_prompt_base_arg_parser(
        description='Get a prompt from text files'
    )

    parser.add_argument(
        'path', help='Paths to the text files, or stdin if not provided', metavar='PATH', type=str, default=None, nargs='*'
    )

    parser.add_argument(
        '-C', '--from-clipboard', help='Load text from clipboard', action='store_true'
    )

    parser.add_argument(
        '-w',
        '--what',
        help='Initial knowledge you want to insert before the PDF content in the prompt',
        type=str,
        default=DEFAULT_GENERAL_WHAT,
    )
    parser.add_argument(
        '-M',
        '--merge',
        help='Merge contents of all pages before processing',
        action='store_true',
    )

    args = parser.parse_args()
    if args.from_clipboard:
        args.path = [save_clipboard_to_tempfile()]
    elif not args.path:
        args.path = [save_stdin_to_tempfile()]
    return args


def main():
    """Make a jazz noise here"""

    args = get_args()

    print(f'Loading text file(s) from {args.path} ...', file=sys.stderr)
    docs = [load_text(p)[0] for p in args.path]
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
            # metadata=docs[0].metadata,
            # metadata={
            #     k: v for k, v in docs[0].metadata.items() if k not in {'page_number'}
            # },
        )
    documents = [merged] if args.merge else docs # type: ignore
    num_docs = len(documents)
    if args.split or word_count > args.chunk_size * 0.75:
        needs_splitting = True
    else:
        needs_splitting = False
    deliver_prompts(
        what=args.what,
        documents=documents, # type: ignore
        needs_splitting=needs_splitting,
        copy=args.copy,
        edit=args.edit,
        should_be_only_one_doc=True if num_docs == 1 else False,
        chunk_size=args.chunk_size,
        extra_chunk_info_fn=general_document_source_info,
        dry_run=args.dry_run,
        parts=args.parts,
    )


if __name__ == '__main__':
    main()
