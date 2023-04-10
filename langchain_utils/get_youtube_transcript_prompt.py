#!/usr/bin/env python3
"""
Author : Xinyuan Chen <45612704+tddschn@users.noreply.github.com>
Date   : 2023-04-09
Purpose: Get a prompt consisting Title and Transcript of a YouTube Video
"""

import argparse
import sys

from .utils import deliver_prompts, format_date, get_word_count, deliver_prompts
from .loaders import load_youtube_url


def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Get a prompt consisting Title and Transcript of a YouTube Video',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument('youtube_url', metavar='YouTube URL', help='YouTube URL')
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
        '-s',
        '--chunk-size',
        help='Chunk size when splitting transcript, also used to determine whether to split',
        metavar='chunk_size',
        type=int,
        default=2000,
    )

    parser.add_argument('-n', '--dry-run', help='Dry run', action='store_true')

    args = parser.parse_args()
    args.youtube_url = args.youtube_url.split('&')[0]
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
    metadata = docs[0].metadata
    title = metadata['title']
    author = metadata['author']
    publish_date = format_date(metadata['publish_date'])
    what = f'''the transcript of a YouTube video titled "{title}" uploaded by "{author}" on {publish_date}'''
    print(f'Title: {title}', file=sys.stderr)
    print(f'Author: {author}', file=sys.stderr)
    print(f'Publish date: {publish_date}', file=sys.stderr)
    # if args.split or get_token_count(docs[0].page_content) > args.chunk_size:
    if args.split or get_word_count(docs[0].page_content) > args.chunk_size * 0.75:
        needs_splitting = True
    else:
        needs_splitting = False
    deliver_prompts(
        what=what,
        docs=docs,
        should_be_only_one_doc=True,
        needs_splitting=needs_splitting,
        copy=args.copy,
        chunk_size=args.chunk_size,
        dry_run=args.dry_run,
    )


if __name__ == '__main__':
    main()
