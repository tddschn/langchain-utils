#!/usr/bin/env python3
"""
Author : Xinyuan Chen <45612704+tddschn@users.noreply.github.com>
Date   : 2023-04-09
Purpose: Get a prompt consisting Title and Transcript of a YouTube Video
"""

import argparse
from .prompts import REPLY_OK_IF_YOU_READ_TEMPLATE


def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Get a prompt consisting Title and Transcript of a YouTube Video',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument('youtube_url', metavar='YouTube URL', help='YouTube URL')

    return parser.parse_args()


def main():
    """Make a jazz noise here"""

    args = get_args()
    from langchain.document_loaders import YoutubeLoader
    from langchain.prompts import PromptTemplate

    loader = YoutubeLoader.from_youtube_channel(args.youtube_url, add_video_info=True)
    docs = loader.load()
    transcript = docs[0].page_content
    title = docs[0].metadata['title']
    prompt = PromptTemplate.from_template(REPLY_OK_IF_YOU_READ_TEMPLATE)
    what = f'the transcript of a YouTube video titled "{title}"'
    content = transcript
    formatted_prompt = prompt.format(what=what, content=content)
    print(formatted_prompt)


if __name__ == '__main__':
    main()
