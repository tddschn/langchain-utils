#!/usr/bin/env python3
from pathlib import Path

DEFAULT_PDF_WHAT = "the content of a PDF file"
DEFAULT_URL_WHAT = "the content of a webpage"
DEFAULT_HTML_WHAT = "the text content of a html file"
DEFAULT_GENERAL_WHAT = "the content of a document"
MODEL_TO_CONTEXT_LENGTH_MAPPING = {
    "gpt-3.5-turbo": 4096,
    "text-davinci-003": 4096,
    "gpt-4": 8192,
    "gpt-4-32k": 32768,
}
DEFAULT_MODEL = "gpt-3.5-turbo"
DEFAULT_MODEL = "gpt-4-32k"
_REPO_ROOT_DIR = Path(__file__).parent.parent
TEMPLATE_DIR = _REPO_ROOT_DIR / "templates"
_README_PATH = _REPO_ROOT_DIR / "README.md"
_README_COMMANDS = [
    "pandocprompt",
    "urlprompt",
    "pdfprompt",
    "ytprompt",
    "textprompt",
    "htmlprompt",
]
_README_TEMPLATE = TEMPLATE_DIR / "README.jinja.md"
_COMMAND_USAGE_TEMPLATE = TEMPLATE_DIR / "readme-command-usage.jinja.md"
LOW_QUALITY_PAGE_CONTENT_PUNC_WHITESPACE_PCT_THRESHOLD = 0.15
# TESSERACT_OCR_DEFAULT_LANG = 'chi_sim'
TESSERACT_OCR_DEFAULT_LANG = "eng"
tesseract_langs = "\nafr\namh\nara\nasm\naze\naze_cyrl\nbel\nben\nbod\nbos\nbre\nbul\ncat\nceb\nces\nchi_sim\nchi_sim_vert\nchi_tra\nchi_tra_vert\nchr\ncos\ncym\ndan\ndeu\ndiv\ndzo\nell\neng\nenm\nepo\nequ\nest\neus\nfao\nfas\nfil\nfin\nfra\nfrk\nfrm\nfry\ngla\ngle\nglg\ngrc\nguj\nhat\nheb\nhin\nhrv\nhun\nhye\niku\nind\nisl\nita\nita_old\njav\njpn\njpn_vert\nkan\nkat\nkat_old\nkaz\nkhm\nkir\nkmr\nkor\nkor_vert\nlao\nlat\nlav\nlit\nltz\nmal\nmar\nmkd\nmlt\nmon\nmri\nmsa\nmya\nnep\nnld\nnor\noci\nori\nosd\npan\npol\npor\npus\nque\nron\nrus\nsan\nscript/Arabic\nscript/Armenian\nscript/Bengali\nscript/Canadian_Aboriginal\nscript/Cherokee\nscript/Cyrillic\nscript/Devanagari\nscript/Ethiopic\nscript/Fraktur\nscript/Georgian\nscript/Greek\nscript/Gujarati\nscript/Gurmukhi\nscript/HanS\nscript/HanS_vert\nscript/HanT\nscript/HanT_vert\nscript/Hangul\nscript/Hangul_vert\nscript/Hebrew\nscript/Japanese\nscript/Japanese_vert\nscript/Kannada\nscript/Khmer\nscript/Lao\nscript/Latin\nscript/Malayalam\nscript/Myanmar\nscript/Oriya\nscript/Sinhala\nscript/Syriac\nscript/Tamil\nscript/Telugu\nscript/Thaana\nscript/Thai\nscript/Tibetan\nscript/Vietnamese\nsin\nslk\nslv\nsnd\nsnum\nspa\nspa_old\nsqi\nsrp\nsrp_latn\nsun\nswa\nswe\nsyr\ntam\ntat\ntel\ntgk\ntha\ntir\nton\ntur\nuig\nukr\nurd\nuzb\nuzb_cyrl\nvie\nyid\nyor\n".strip().splitlines()
_MACOS_CONDA_ENV_EG_TESSDATA_PREFIX = (
    "/usr/local/Caskroom/miniconda/base/envs/eg/share/tessdata/"
)
USER_AGENT_WINDOWS_CHROME = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"


def _load_pdf_with_apple_vision(pdf_path: str, ocr_language: str) -> list["Document"]:
    """Helper to load PDF with Apple Vision, only called on macOS."""
    from apple_vision_utils.utils import pdf_to_images, image_to_text
    from langchain.docstore.document import Document
    import tempfile
    import fitz

    docs = []
    fitz_doc = fitz.open(pdf_path)  # type: ignore
    doc_metadata = {
        k: fitz_doc.metadata[k]
        for k in fitz_doc.metadata
        if type(fitz_doc.metadata[k]) in [str, int]
    }
    with tempfile.TemporaryDirectory() as temp_dir:
        image_paths = pdf_to_images(pdf_path, output_dir=temp_dir)
        apple_vision_lang = _map_tesseract_lang_to_apple_vision(ocr_language)
        for i, img_path in enumerate(image_paths):
            ocr_results = image_to_text(img_path, lang=apple_vision_lang)
            page_text = "\n".join([res["text"] for res in ocr_results])
            metadata = {
                "source": pdf_path,
                "file_path": pdf_path,
                "page": i,
                "total_pages": len(fitz_doc),
                **doc_metadata,
            }
            doc = Document(page_content=page_text, metadata=metadata)
            docs.append(doc)
    return docs


def _map_tesseract_lang_to_apple_vision(lang: str) -> str:
    """Helper to map tesseract language codes to Apple Vision language codes."""
    return TESSERACT_TO_APPLE_VISION_LANG_MAP.get(lang, lang)
