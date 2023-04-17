#!/usr/bin/env python3

from pathlib import Path

DEFAULT_PDF_WHAT = 'the content of a PDF file'
DEFAULT_URL_WHAT = 'the content of a webpage'
DEFAULT_HTML_WHAT = 'the text content of a html file'
DEFAULT_GENERAL_WHAT = 'the content of a document'

MODEL_TO_CONTEXT_LENGTH_MAPPING = {
    'gpt-3.5-turbo': 4096,
    'text-davinci-003': 4096,
    'gpt-4': 8192,
    'gpt-4-32k': 32768,
}

DEFAULT_MODEL = 'gpt-3.5-turbo'


_REPO_ROOT_DIR = Path(__file__).parent.parent
TEMPLATE_DIR = _REPO_ROOT_DIR / 'templates'

_README_PATH = _REPO_ROOT_DIR / 'README.md'
_README_COMMANDS = ['urlprompt', 'pdfprompt', 'ytprompt', 'textprompt', 'htmlprompt']
_README_TEMPLATE = TEMPLATE_DIR / 'README.jinja.md'
_COMMAND_USAGE_TEMPLATE = TEMPLATE_DIR / 'readme-command-usage.jinja.md'
