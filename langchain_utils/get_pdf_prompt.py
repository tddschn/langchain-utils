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
    pymupdf_doc_page_info,
    convert_str_slice_notation_to_slice,
)
from .loaders import load_pdf
from .config import DEFAULT_PDF_WHAT
from .utils_argparse import get_get_prompt_base_arg_parser


def get_args():
    """Get command-line arguments"""

    parser = get_get_prompt_base_arg_parser(
        description='Get a prompt consisting the text content of a PDF file'
    )

    parser.add_argument(
        'pdf_path', help='Path to the PDF file', metavar='PDF Path', type=str
    )
    parser.add_argument(
        '-p',
        '--pages',
        help='Only include specified page numbers',
        type=int,
        nargs='+',
        default=None,
    )
    parser.add_argument(
        '-l',
        '--page-slice',
        help='Use Python list slice to select page numbers',
        type=str,
        default=None,
    )
    parser.add_argument(
        '-M',
        '--merge',
        help='Merge contents of all pages before processing',
        action='store_true',
    )
    parser.add_argument(
        '-w',
        '--what',
        help='Initial knowledge you want to insert before the PDF content in the prompt',
        type=str,
        default=DEFAULT_PDF_WHAT,
    )

    args = parser.parse_args()
    return args


def main():
    """Make a jazz noise here"""

    args = get_args()

    print(f'Loading PDF from {args.pdf_path} ...', file=sys.stderr)
    docs = load_pdf(args.pdf_path)
    num_whole_pdf_pages = len(docs)
    if args.pages and args.page_slice:
        print(
            'Please specify either --pages or --page-slice, not both',
            file=sys.stderr,
        )
        sys.exit(1)
    if args.pages:
        args.pages = [p for p in args.pages if p <= num_whole_pdf_pages and p > 0]
        docs = [doc for doc in docs if doc.metadata['page_number'] in args.pages]
    if args.page_slice:
        args.pages = list(x + 1 for x in list(range(num_whole_pdf_pages))[convert_str_slice_notation_to_slice(args.page_slice)])
        docs = [doc for doc in docs if doc.metadata['page_number'] in args.pages]
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
        edit=args.edit,
        chunk_size=args.chunk_size,
        extra_chunk_info_fn=pymupdf_doc_page_info,
        dry_run=args.dry_run,
        parts=args.parts,
    )


if __name__ == '__main__':
    main()
