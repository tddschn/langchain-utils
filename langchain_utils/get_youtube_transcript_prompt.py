#!/usr/bin/env python3
"""
Author : Xinyuan Chen <45612704+tddschn@users.noreply.github.com>
Date   : 2023-04-09
Purpose: Get a prompt consisting Title and Transcript of a YouTube Video
"""

import argparse

from .utils import get_token_count
from .prompts import (
    REPLY_OK_IF_YOU_READ_TEMPLATE,
    REPLY_OK_IF_YOU_READ_TEMPLATE_SPLITTED_FIRST,
    REPLY_OK_IF_YOU_READ_TEMPLATE_SPLITTED_CONTINUED,
)


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

    return parser.parse_args()


def main():
    """Make a jazz noise here"""

    args = get_args()
    from langchain.document_loaders import YoutubeLoader
    from langchain.prompts import PromptTemplate

    loader = YoutubeLoader.from_youtube_channel(args.youtube_url, add_video_info=True)
    docs = loader.load()
    if args.split or get_token_count(docs[0].page_content) > args.chunk_size:
        needs_splitting = True
    else:
        needs_splitting = False
    if needs_splitting:
        from langchain.text_splitter import TokenTextSplitter

        splitter = TokenTextSplitter(encoding_name='cl100k_base', chunk_size=2000)
        splitted = splitter.split_documents(docs)
        num_chunks = len(splitted)
        title = docs[0].metadata['title']
        for i, doc in enumerate(splitted):
            if i == 0:
                prompt = PromptTemplate.from_template(
                    REPLY_OK_IF_YOU_READ_TEMPLATE_SPLITTED_FIRST
                )
            else:
                prompt = PromptTemplate.from_template(
                    REPLY_OK_IF_YOU_READ_TEMPLATE_SPLITTED_CONTINUED
                )
            what = f'the transcript of a YouTube video titled "{title}"'
            content = doc.page_content
            formatted_prompt = prompt.format(what=what, content=content, x=i + 1)
            input(f'Press Enter to copy prompt {i+1}/{num_chunks}: ')
            import pyperclip

            pyperclip.copy(formatted_prompt)

        return
    transcript = docs[0].page_content
    title = docs[0].metadata['title']
    prompt = PromptTemplate.from_template(REPLY_OK_IF_YOU_READ_TEMPLATE)
    what = f'the transcript of a YouTube video titled "{title}"'
    content = transcript
    formatted_prompt = prompt.format(what=what, content=content)
    if args.copy:
        import pyperclip

        pyperclip.copy(formatted_prompt)
        print('Prompt copied to clipboard.')
    else:
        print(formatted_prompt)


if __name__ == '__main__':
    main()
