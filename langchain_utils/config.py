#!/usr/bin/env python3

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
