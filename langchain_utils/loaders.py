#!/usr/bin/env python3

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain.docstore.document import Document


def load_youtube_url(youtube_url: str) -> list['Document']:
    from langchain.document_loaders import YoutubeLoader

    loader = YoutubeLoader.from_youtube_channel(youtube_url, add_video_info=True)
    docs = loader.load()
    return docs


def load_pdf(pdf_path: str) -> list['Document']:
    from langchain.document_loaders import PyMuPDFLoader

    loader = PyMuPDFLoader(pdf_path)
    docs = loader.load()
    return docs


def load_url(urls: list[str], javascript: bool = False) -> list['Document']:
    from langchain.document_loaders import UnstructuredURLLoader, SeleniumURLLoader

    if javascript:
        loader_class = SeleniumURLLoader
        kwargs = {}
    else:
        loader_class = UnstructuredURLLoader
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'
        # }

        # kwargs = {'headers': headers}
        # You are using old version of unstructured. The headers parameter is ignored
        kwargs = {}

    from unstructured.partition.html import partition_html

    partition_html(url='https://mp.weixin.qq.com/s/FsrDnCFKGD-FzP5YD76tbA')
    loader = loader_class(urls=urls, **kwargs)
    docs = loader.load()

    return docs
