from os import PathLike
from pathlib import Path
from typing import Callable
from langchain.docstore.document import Document
from langchain.document_loaders.pdf import BasePDFLoader
from langchain.document_loaders.base import BaseLoader
from langchain_utils.config import (
    LOW_QUALITY_PAGE_CONTENT_PUNC_WHITESPACE_PCT_THRESHOLD,
    _MACOS_CONDA_ENV_EG_TESSDATA_PREFIX,
    TESSERACT_OCR_DEFAULT_LANG,
)
from langchain_utils.utils_doc_loaders import get_str_punc_and_whitespace_chars_pct


def set_tessdata(tessdata_prefix: str = _MACOS_CONDA_ENV_EG_TESSDATA_PREFIX):
    import os

    if 'TESSDATA_PREFIX' not in os.environ:
        os.environ['TESSDATA_PREFIX'] = tessdata_prefix


set_tessdata()


class PyMuPDFLoaderWithFallbackOCR(BasePDFLoader):
    """Loader that uses PyMuPDF to load PDF files."""

    def __init__(self, file_path: str):
        """Initialize with file path."""
        try:
            import fitz  # noqa:F401
        except ImportError:
            raise ValueError(
                "PyMuPDF package not found, please install it with "
                "`pip install pymupdf`"
            )

        super().__init__(file_path)

    def load(
        self,
        ocr_language: str = TESSERACT_OCR_DEFAULT_LANG,
    ) -> list[Document]:
        """Load file."""
        import fitz

        doc = fitz.open(self.file_path)  # open document # type: ignore
        file_path = self.file_path if self.web_path is None else self.web_path

        # documents = [
        #     Document(
        #         page_content=page.get_text().encode("utf-8") or page.get_text(textpage=page.get_textpage_ocr(flags=0, dpi=300, full=True, language=ocr_language)).encode("utf-8"),
        #         metadata=dict(
        #             {
        #                 "source": file_path,
        #                 "file_path": file_path,
        #                 "page_number": page.number + 1,
        #                 "total_pages": len(doc),
        #             },
        #             **{
        #                 k: doc.metadata[k]
        #                 for k in doc.metadata
        #                 if type(doc.metadata[k]) in [str, int]
        #             }
        #         ),
        #     )
        #     for page in doc
        # ]
        from tqdm import tqdm

        documents = [
            Document(
                page_content=page.get_text().encode("utf-8")
                or page.get_text(
                    textpage=page.get_textpage_ocr(
                        flags=0, dpi=300, full=True, language=ocr_language
                    )
                ).encode("utf-8"),
                metadata=dict(
                    {
                        "source": file_path,
                        "file_path": file_path,
                        # "page_number": page.number + 1,
                        "page": page.number,
                        "total_pages": len(doc),
                    },
                    **{
                        k: doc.metadata[k]
                        for k in doc.metadata
                        if type(doc.metadata[k]) in [str, int]
                    }
                ),
            )
            for page in tqdm(doc, desc="Processing pages")
        ]

        return [document for document in documents if document.page_content]


class DocumentJSONLoader(BaseLoader):
    def __init__(
        self, doc_json_path: PathLike, filter: Callable[[dict], bool] | None = None
    ):
        self.doc_json_path = Path(doc_json_path)
        self.filter = filter

    # convert utils.load_doc_json to the load() method
    def load(
        self,
        low_quality_threshold: float = LOW_QUALITY_PAGE_CONTENT_PUNC_WHITESPACE_PCT_THRESHOLD,
    ) -> list[Document]:
        import json

        documents = []
        included_keys = {'page_content', 'metadata'}
        doc_dicts: list[dict] = json.loads(self.doc_json_path.read_text())
        for doc_dict in filter(
            lambda doc: get_str_punc_and_whitespace_chars_pct(doc['page_content'])
            <= low_quality_threshold,
            doc_dicts,
        ):
            if self.filter is not None and not self.filter(doc_dict):
                continue
            # skip if metadata.file_path in blacklist
            # if doc_dict['metadata']['file_path'] in pdf_path_blacklist:
            #     continue
            documents.append(
                Document(**{k: v for k, v in doc_dict.items() if k in included_keys})
            )
        return documents
