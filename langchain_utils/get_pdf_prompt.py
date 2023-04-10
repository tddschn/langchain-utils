#!/usr/bin/env python3
"""
Author : Xinyuan Chen <45612704+tddschn@users.noreply.github.com>
Date   : 2023-04-09
Purpose: Get a prompt consisting Title and Transcript of a YouTube Video
"""

import argparse
import sys

from . import __version__
from .utils import (
    deliver_prompts,
    format_date,
    get_word_count,
    deliver_prompts,
    pymupdf_doc_page_info,
)
from .loaders import load_pdf
from .config import DEFAULT_PDF_WHAT


def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Get a prompt consisting Title and Transcript of a YouTube Video',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        'pdf_path', help='Path to the PDF file', metavar='PDF Path', type=str
    )
    parser.add_argument(
        '-V',
        '--version',
        action='version',
        version=f'%(prog)s {__version__}',
    )
    parser.add_argument(
        '-c', '--copy', help='Copy the prompt to clipboard', action='store_true'
    )
    parser.add_argument(
        '-m',
        '--model',
        help='Model to use',
        metavar='model',
        type=str,
        default='gpt-3.5-turbo',
    )
    parser.add_argument(
        '-S',
        '--split',
        help='Split the prompt into multiple parts',
        action='store_true',
    )
    parser.add_argument(
        '-M',
        '--merge',
        help='Merge contents of all pages before processing',
        action='store_true',
    )
    parser.add_argument(
        '-s',
        '--chunk-size',
        help='Chunk size when splitting transcript, also used to determine whether to split',
        metavar='chunk_size',
        type=int,
        default=2000,
    )
    parser.add_argument(
        '-w',
        '--what',
        help='Initial knowledge you want to insert before the PDF content in the prompt',
        type=str,
        default=DEFAULT_PDF_WHAT,
    )
    parser.add_argument('-n', '--dry-run', help='Dry run', action='store_true')

    args = parser.parse_args()
    return args


def main():
    """Make a jazz noise here"""

    args = get_args()

    print(f'Loading PDF from {args.pdf_path} ...', file=sys.stderr)
    docs = load_pdf(args.pdf_path)
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
            metadata={
                k: v for k, v in docs[0].metadata.items() if k not in {'page_number'}
            },
        )
    if args.split or word_count > args.chunk_size * 0.75:
        needs_splitting = True
    else:
        needs_splitting = False
    deliver_prompts(
        what=args.what,
        documents=[merged] if args.merge else docs,  # type: ignore
        needs_splitting=needs_splitting,
        copy=args.copy,
        chunk_size=args.chunk_size,
        extra_chunk_info_fn=pymupdf_doc_page_info,
        dry_run=args.dry_run,
    )


if __name__ == '__main__':
    main()
