# langchain-utils

LangChain Utilities

- [langchain-utils](#langchain-utils)
  - [Prompt generation using LangChain document loaders](#prompt-generation-using-langchain-document-loaders)
    - [Demos](#demos)
    - [`urlprompt`](#urlprompt)
    - [`pdfprompt`](#pdfprompt)
    - [`ytprompt`](#ytprompt)
    - [`textprompt`](#textprompt)
    - [`htmlprompt`](#htmlprompt)
  - [Installation](#installation)
    - [pipx](#pipx)
    - [pip](#pip)
  - [Develop](#develop)

## Prompt generation using LangChain document loaders

Do you find yourself frequently copy-pasting texts from the web / PDFs / other documents into ChatGPT?

If yes, these tools are for you!

Optimized to feed into a chat interface (like ChatGPT) manually in one or multiple (to get around context length limits) goes.

Basically, the prompts generated look like this:

```python
REPLY_OK_IF_YOU_READ_TEMPLATE = '''
Below is {what}, reply "OK" if you read:

"""
{content}
"""
'''.strip()
```

You can feed it directly to a chat interface like ChatGPT, and ask follow up questions about it.

See [`prompts.py`](./langchain_utils/prompts.py) for other variations.

### Demos

- Loading `https://github.com/tddschn/langchain-utils` and copy to clipboard:

<!-- create a video tag with https://user-images.githubusercontent.com/45612704/231729153-341bd962-28cc-40a3-af8b-91e038ccaf6c.mp4 -->

<video src="https://user-images.githubusercontent.com/45612704/231729153-341bd962-28cc-40a3-af8b-91e038ccaf6c.mp4" controls width="100%"></video>

- Load 3 pages of a pdf file, open each part for inspection before copying, and optionally merge 3 pages into 2 prompts that wouldn't go over the `gpt-3.5-turbo`'s context length limit with langchain's `TokenTextSplitter`.

<!-- for https://user-images.githubusercontent.com/45612704/231731553-63cf3cef-a210-4761-8ca3-dd47bedc3393.mp4 -->

<video src="https://user-images.githubusercontent.com/45612704/231731553-63cf3cef-a210-4761-8ca3-dd47bedc3393.mp4" controls width="100%"></video>

### `urlprompt`

```
$ urlprompt --help

usage: urlprompt [-h] [-V] [-c] [-e] [-m model] [-S] [-s chunk_size]
                 [-P PARTS [PARTS ...]] [-r] [-R]
                 [--print-percentage-non-ascii] [-n] [-w WHAT] [-M] [-j] [-g]
                 [--github-path GITHUB_PATH]
                 [--github-revision GITHUB_REVISION]
                 URL

Get a prompt consisting the text content of a webpage

positional arguments:
  URL                   URL to the webpage

options:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -c, --copy            Copy the prompt to clipboard (default: False)
  -e, --edit            Edit the prompt and copy manually (default: False)
  -m model, --model model
                        Model to use (default: gpt-3.5-turbo)
  -S, --no-split        Do not split the prompt into multiple parts (use this
                        if the model has a really large context size)
                        (default: False)
  -s chunk_size, --chunk-size chunk_size
                        Chunk size when splitting transcript, also used to
                        determine whether to split, defaults to 1/2 of the
                        context length limit of the model (default: None)
  -P PARTS [PARTS ...], --parts PARTS [PARTS ...]
                        Parts to select in the processes list of Documents
                        (default: None)
  -r, --raw             Wraps the content in triple quotes with no extra text
                        (default: False)
  -R, --raw-no-quotes   Output the content only (default: False)
  --print-percentage-non-ascii
                        Print percentage of non-ascii characters (default:
                        False)
  -n, --dry-run         Dry run (default: False)
  -w WHAT, --what WHAT  Initial knowledge you want to insert before the PDF
                        content in the prompt (default: the content of a
                        webpage)
  -M, --merge           Merge contents of all pages before processing
                        (default: False)
  -j, --javascript      Use JavaScript to render the page (default: False)
  -g, --github          Load the raw file from a GitHub URL (default: False)
  --github-path GITHUB_PATH
                        Path to the GitHub file (default: README.md)
  --github-revision GITHUB_REVISION
                        Revision for the GitHub file (default: master)

```
### `pdfprompt`

```
$ pdfprompt --help

usage: pdfprompt [-h] [-V] [-c] [-e] [-m model] [-S] [-s chunk_size]
                 [-P PARTS [PARTS ...]] [-r] [-R]
                 [--print-percentage-non-ascii] [-n] [-p PAGES [PAGES ...]]
                 [-l PAGE_SLICE] [-M] [-w WHAT] [-o] [-L OCR_LANGUAGE]
                 PDF Path

Get a prompt consisting the text content of a PDF file

positional arguments:
  PDF Path              Path to the PDF file

options:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -c, --copy            Copy the prompt to clipboard (default: False)
  -e, --edit            Edit the prompt and copy manually (default: False)
  -m model, --model model
                        Model to use (default: gpt-3.5-turbo)
  -S, --no-split        Do not split the prompt into multiple parts (use this
                        if the model has a really large context size)
                        (default: False)
  -s chunk_size, --chunk-size chunk_size
                        Chunk size when splitting transcript, also used to
                        determine whether to split, defaults to 1/2 of the
                        context length limit of the model (default: None)
  -P PARTS [PARTS ...], --parts PARTS [PARTS ...]
                        Parts to select in the processes list of Documents
                        (default: None)
  -r, --raw             Wraps the content in triple quotes with no extra text
                        (default: False)
  -R, --raw-no-quotes   Output the content only (default: False)
  --print-percentage-non-ascii
                        Print percentage of non-ascii characters (default:
                        False)
  -n, --dry-run         Dry run (default: False)
  -p PAGES [PAGES ...], --pages PAGES [PAGES ...]
                        Only include specified page numbers (default: None)
  -l PAGE_SLICE, --page-slice PAGE_SLICE
                        Use Python slice syntax to select page numbers (e.g.
                        1:3, 1:10:2, etc.) (default: None)
  -M, --merge           Merge contents of all pages before processing
                        (default: False)
  -w WHAT, --what WHAT  Initial knowledge you want to insert before the PDF
                        content in the prompt (default: the content of a PDF
                        file)
  -o, --fallback-ocr    Use OCR as fallback if no text detected on page,
                        please set TESSDATA_PREFIX environment variable to the
                        path of your tesseract data directory (default: False)
  -L OCR_LANGUAGE, --ocr-language OCR_LANGUAGE
                        Language to use for Tesseract OCR (default: chi_sim)

```
### `ytprompt`

```
$ ytprompt --help

usage: ytprompt [-h] [-V] [-c] [-e] [-m model] [-S] [-s chunk_size]
                [-P PARTS [PARTS ...]] [-r] [-R]
                [--print-percentage-non-ascii] [-n]
                YouTube URL

Get a prompt consisting Title and Transcript of a YouTube Video

positional arguments:
  YouTube URL           YouTube URL

options:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -c, --copy            Copy the prompt to clipboard (default: False)
  -e, --edit            Edit the prompt and copy manually (default: False)
  -m model, --model model
                        Model to use (default: gpt-3.5-turbo)
  -S, --no-split        Do not split the prompt into multiple parts (use this
                        if the model has a really large context size)
                        (default: False)
  -s chunk_size, --chunk-size chunk_size
                        Chunk size when splitting transcript, also used to
                        determine whether to split, defaults to 1/2 of the
                        context length limit of the model (default: None)
  -P PARTS [PARTS ...], --parts PARTS [PARTS ...]
                        Parts to select in the processes list of Documents
                        (default: None)
  -r, --raw             Wraps the content in triple quotes with no extra text
                        (default: False)
  -R, --raw-no-quotes   Output the content only (default: False)
  --print-percentage-non-ascii
                        Print percentage of non-ascii characters (default:
                        False)
  -n, --dry-run         Dry run (default: False)

```
### `textprompt`

```
$ textprompt --help

usage: textprompt [-h] [-V] [-c] [-e] [-m model] [-S] [-s chunk_size]
                  [-P PARTS [PARTS ...]] [-r] [-R]
                  [--print-percentage-non-ascii] [-n] [-C] [-w WHAT] [-M]
                  [PATH ...]

Get a prompt from text files

positional arguments:
  PATH                  Paths to the text files, or stdin if not provided
                        (default: None)

options:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -c, --copy            Copy the prompt to clipboard (default: False)
  -e, --edit            Edit the prompt and copy manually (default: False)
  -m model, --model model
                        Model to use (default: gpt-3.5-turbo)
  -S, --no-split        Do not split the prompt into multiple parts (use this
                        if the model has a really large context size)
                        (default: False)
  -s chunk_size, --chunk-size chunk_size
                        Chunk size when splitting transcript, also used to
                        determine whether to split, defaults to 1/2 of the
                        context length limit of the model (default: None)
  -P PARTS [PARTS ...], --parts PARTS [PARTS ...]
                        Parts to select in the processes list of Documents
                        (default: None)
  -r, --raw             Wraps the content in triple quotes with no extra text
                        (default: False)
  -R, --raw-no-quotes   Output the content only (default: False)
  --print-percentage-non-ascii
                        Print percentage of non-ascii characters (default:
                        False)
  -n, --dry-run         Dry run (default: False)
  -C, --from-clipboard  Load text from clipboard (default: False)
  -w WHAT, --what WHAT  Initial knowledge you want to insert before the PDF
                        content in the prompt (default: the content of a
                        document)
  -M, --merge           Merge contents of all pages before processing
                        (default: False)

```
### `htmlprompt`

```
$ htmlprompt --help

usage: htmlprompt [-h] [-V] [-c] [-e] [-m model] [-S] [-s chunk_size]
                  [-P PARTS [PARTS ...]] [-r] [-R]
                  [--print-percentage-non-ascii] [-n] [-C] [-w WHAT] [-M]
                  [PATH ...]

Get a prompt from html files

positional arguments:
  PATH                  Paths to the html files, or stdin if not provided
                        (default: None)

options:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -c, --copy            Copy the prompt to clipboard (default: False)
  -e, --edit            Edit the prompt and copy manually (default: False)
  -m model, --model model
                        Model to use (default: gpt-3.5-turbo)
  -S, --no-split        Do not split the prompt into multiple parts (use this
                        if the model has a really large context size)
                        (default: False)
  -s chunk_size, --chunk-size chunk_size
                        Chunk size when splitting transcript, also used to
                        determine whether to split, defaults to 1/2 of the
                        context length limit of the model (default: None)
  -P PARTS [PARTS ...], --parts PARTS [PARTS ...]
                        Parts to select in the processes list of Documents
                        (default: None)
  -r, --raw             Wraps the content in triple quotes with no extra text
                        (default: False)
  -R, --raw-no-quotes   Output the content only (default: False)
  --print-percentage-non-ascii
                        Print percentage of non-ascii characters (default:
                        False)
  -n, --dry-run         Dry run (default: False)
  -C, --from-clipboard  Load text from clipboard (default: False)
  -w WHAT, --what WHAT  Initial knowledge you want to insert before the PDF
                        content in the prompt (default: the text content of a
                        html file)
  -M, --merge           Merge contents of all pages before processing
                        (default: False)

```

## Installation

### pipx

This is the recommended installation method.

```
$ pipx install langchain-utils
```

### [pip](https://pypi.org/project/langchain-utils/)

```
$ pip install langchain-utils
```

## Develop

```
$ git clone https://github.com/tddschn/langchain-utils.git
$ cd langchain-utils
$ poetry install
```