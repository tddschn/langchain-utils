#!/usr/bin/env python3
import sys
from langchain_utils.config import (
    TESSERACT_OCR_DEFAULT_LANG,
    TESSERACT_TO_APPLE_VISION_LANG_MAP,
)
from typing import TYPE_CHECKING, Literal, Union, Sequence
from langchain_utils.utils import extract_github_info, get_github_file_raw_url

if TYPE_CHECKING:
    from langchain.docstore.document import Document


def load_youtube_url(
    youtube_url: str, language: Union[str, Sequence[str]] = "en"
) -> list["Document"]:
    from langchain.document_loaders import YoutubeLoader

    loader = YoutubeLoader.from_youtube_url(
        youtube_url, add_video_info=True, language=language
    )
    docs = loader.load()
    return docs


def load_pdf(
    pdf_path: str,
    use_ocr_if_no_text_detected_on_page: bool = False,
    ocr_language: str = TESSERACT_OCR_DEFAULT_LANG,
    force_ocr: bool = False,
    ocr_engine: str = "tesseract",
) -> list["Document"]:
    if (
        (force_ocr or use_ocr_if_no_text_detected_on_page)
        and ocr_engine == "apple-vision"
        and (sys.platform == "darwin")
    ):
        try:
            return _load_pdf_with_apple_vision(pdf_path, ocr_language=ocr_language)
        except ImportError:
            # Fallback to tesseract if apple-vision-utils is not installed
            # This is a safeguard, the CLI should have already handled this.
            pass
    if force_ocr or use_ocr_if_no_text_detected_on_page:
        from langchain_utils.document_loaders import PyMuPDFLoaderWithFallbackOCR

        loader_cls = PyMuPDFLoaderWithFallbackOCR
        load_kwargs = {"ocr_language": ocr_language, "force_ocr": force_ocr}
    else:
        from langchain.document_loaders import PyMuPDFLoader

        loader_cls = PyMuPDFLoader
        load_kwargs = {}
    loader = loader_cls(pdf_path)
    docs = loader.load(**load_kwargs)
    return docs


def load_url(urls: list[str], javascript: bool = False) -> list["Document"]:
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

    partition_html(url="https://mp.weixin.qq.com/s/FsrDnCFKGD-FzP5YD76tbA")
    loader = loader_class(urls=urls, **kwargs)
    docs = loader.load()
    return docs


def load_text(path: str, encoding: str | None = None) -> list["Document"]:
    from langchain.document_loaders import TextLoader

    loader = TextLoader(path, encoding=encoding)
    docs = loader.load()
    return docs


def load_html(
    path: str, open_encoding: str | None = None, bs_kwargs: dict | None = None
) -> list["Document"]:
    from langchain.document_loaders import BSHTMLLoader

    loader = BSHTMLLoader(path, open_encoding=open_encoding, bs_kwargs=bs_kwargs)
    docs = loader.load()
    return docs


UnstructuredLoadingMode = Literal["single", "elements"]


def load_word(path: str, mode: UnstructuredLoadingMode = "single") -> list["Document"]:
    # UnstructuredWordDocumentLoader
    from langchain.document_loaders import UnstructuredWordDocumentLoader

    loader = UnstructuredWordDocumentLoader(path, mode=mode)
    docs = loader.load()
    return docs


def load_github_raw(
    github_url: str, github_revision: str = "master", github_path: str = "README.md"
) -> list["Document"]:
    from langchain.requests import TextRequestsWrapper
    from langchain.docstore.document import Document

    github_info = extract_github_info(github_url)
    if github_info is None:
        raise ValueError(f"Invalid GitHub URL: {github_url}")
    github_info |= {"revision": github_revision, "file_path": github_path}
    url = get_github_file_raw_url(**github_info)
    text = TextRequestsWrapper().get(url)
    docs = [Document(page_content=text, metadata={"url": url})]
    return docs


def load_pandoc(
    input_file: str, output_format: str = "gfm", input_format: str | None = None
) -> list["Document"]:
    import subprocess
    from langchain.docstore.document import Document

    command = ["pandoc", input_file, "-t", output_format]
    if input_format:
        command.extend(["-f", input_format])
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    docs = [Document(page_content=result.stdout)]
    return docs


def _map_tesseract_lang_to_apple_vision(lang: str) -> str:
    """Helper to map tesseract language codes to Apple Vision language codes."""
    return TESSERACT_TO_APPLE_VISION_LANG_MAP.get(lang, lang)


def _load_pdf_with_apple_vision(pdf_path: str, ocr_language: str) -> list["Document"]:
    """Helper to load PDF with Apple Vision, only called on macOS."""
    from apple_vision_utils.utils import pdf_to_images, image_to_text
    from langchain.docstore.document import Document
    import tempfile
    import fitz
    import logging

    logging.info(f"Starting PDF processing with Apple Vision for: {pdf_path}")
    docs = []
    fitz_doc = fitz.open(pdf_path)  # type: ignore
    doc_metadata = {}
    if fitz_doc.metadata:
        doc_metadata = {
            k: fitz_doc.metadata[k]
            for k in fitz_doc.metadata
            if type(fitz_doc.metadata[k]) in [str, int]
        }
    with tempfile.TemporaryDirectory() as temp_dir:
        logging.info("Converting PDF to images...")
        image_paths = pdf_to_images(pdf_path, output_dir=temp_dir)
        logging.info(f"Converted PDF to {len(image_paths)} images.")
        apple_vision_lang = _map_tesseract_lang_to_apple_vision(ocr_language)
        logging.info(f"Using Apple Vision language code: '{apple_vision_lang}'")
        for i, img_path in enumerate(image_paths):
            logging.info(
                f"Performing OCR on page {i + 1}/{len(image_paths)}: {img_path}"
            )
            ocr_results = image_to_text(img_path, lang=apple_vision_lang)
            page_text = "\n".join([res["text"] for res in ocr_results])
            logging.info(
                f"Page {i + 1} OCR complete. Found {len(ocr_results)} text blocks."
            )
            metadata = {
                "source": pdf_path,
                "file_path": pdf_path,
                "page": i,
                "total_pages": len(fitz_doc),
                **doc_metadata,
            }
            doc = Document(page_content=page_text, metadata=metadata)
            docs.append(doc)
    logging.info(f"Finished PDF processing for: {pdf_path}")
    return docs
