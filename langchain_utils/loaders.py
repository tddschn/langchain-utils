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


def load_url(url: str | list[str], javascript: bool = False) -> list['Document']:
    from langchain.document_loaders import UnstructuredURLLoader, SeleniumURLLoader

    if javascript:
        loader_class = SeleniumURLLoader
    else:
        loader_class = UnstructuredURLLoader

    loader = loader_class(urls=[url] if isinstance(url, str) else url)
    docs = loader.load()
    return docs
