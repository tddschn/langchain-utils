#!/usr/bin/env python3
"""
Author : Xinyuan Chen <45612704+tddschn@users.noreply.github.com>
Date   : 2023-04-09
Purpose: Get a prompt consisting Title and Transcript of a YouTube Video
"""

import sys

from . import __version__
from .utils import (
    deliver_prompts,
    format_date,
    get_word_count,
    deliver_prompts,
    get_default_chunk_size,
    get_percentage_non_ascii,
    get_token_count,
)
from .loaders import load_youtube_url
from .utils_argparse import get_get_prompt_base_arg_parser


def get_args():
    """Get command-line arguments"""

    parser = get_get_prompt_base_arg_parser(
        description='Get a prompt consisting Title and Transcript of a YouTube Video'
    )

    parser.add_argument('youtube_url', metavar='YouTube URL', help='YouTube URL')

    args = parser.parse_args()
    args.youtube_url = args.youtube_url.split('&')[0]
    args.chunk_size = get_default_chunk_size(args.model)
    return args


def main():
    """Make a jazz noise here"""

    args = get_args()
    print(f'Loading transcript from {args.youtube_url} ...', file=sys.stderr)
    docs = load_youtube_url(args.youtube_url)
    print(
        f'Loaded transcript. Word count: {get_word_count((t := docs[0].page_content))} Char count: {len(t)}',
        file=sys.stderr,
    )
    texts = [doc.page_content for doc in docs]
    all_text = '\n'.join(texts)
    word_count = get_word_count((all_text))
    char_count = len(all_text)
    if args.print_percentage_non_ascii:
        print(
            f'Percentage of non-ascii characters: {get_percentage_non_ascii(all_text) * 100:.2f}%',
            file=sys.stderr,
        )
        token_count = get_token_count(all_text)
        print(f'Token count: {token_count}', file=sys.stderr)
        print(f'Token / Word: {token_count / word_count:.2f}', file=sys.stderr)
        print(f'Token / Char: {token_count / char_count:.2f}', file=sys.stderr)
        return

    metadata = docs[0].metadata
    title = metadata['title']
    author = metadata['author']
    publish_date = format_date(metadata['publish_date'])
    what = f'''the transcript of a YouTube video titled "{title}" uploaded by "{author}" on {publish_date}'''
    print(f'Title: {title}', file=sys.stderr)
    print(f'Author: {author}', file=sys.stderr)
    print(f'Publish date: {publish_date}', file=sys.stderr)
    if args.no_split:
        needs_splitting = False
    elif word_count > args.chunk_size * 0.75:
        needs_splitting = True
    else:
        needs_splitting = False
    deliver_prompts(
        what=what,
        documents=docs,
        should_be_only_one_doc=True,
        needs_splitting=needs_splitting,
        copy=args.copy,
        edit=args.edit,
        chunk_size=args.chunk_size,
        dry_run=args.dry_run,
        raw_triple_quotes=args.raw,
        raw=args.raw_no_quotes,
        parts=args.parts,
    )


if __name__ == '__main__':
    main()
