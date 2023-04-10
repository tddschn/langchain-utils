# langchain-utils

LangChain Utilities


- [langchain-utils](#langchain-utils)
  - [Prompt generation using LangChain document loaders](#prompt-generation-using-langchain-document-loaders)
    - [`urlprompt`](#urlprompt)
    - [`pdfprompt`](#pdfprompt)
    - [`ytprompt`](#ytprompt)
  - [Installation](#installation)
    - [pipx](#pipx)
    - [pip](#pip)
  - [Develop](#develop)


## Prompt generation using LangChain document loaders

Optimized to feed into a chat interface (like ChatGPT) manually in one or multiple (to get around context length limits) goes.

### `urlprompt`

```
$ urlprompt --help

usage: urlprompt [-h] [-V] [-c] [-e] [-m model] [-S] [-s chunk_size] [-n]
                 [-w WHAT] [-M] [-j]
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
  -S, --split           Split the prompt into multiple parts (default: False)
  -s chunk_size, --chunk-size chunk_size
                        Chunk size when splitting transcript, also used to
                        determine whether to split (default: 2000)
  -n, --dry-run         Dry run (default: False)
  -w WHAT, --what WHAT  Initial knowledge you want to insert before the PDF
                        content in the prompt (default: the content of a
                        webpage)
  -M, --merge           Merge contents of all pages before processing
                        (default: False)
  -j, --javascript      Use JavaScript to render the page (default: False)

```

### `pdfprompt`

```
$ pdfprompt --help

usage: pdfprompt [-h] [-V] [-c] [-e] [-m model] [-S] [-s chunk_size] [-n]
                 [-p PAGES [PAGES ...]] [-M] [-w WHAT]
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
  -S, --split           Split the prompt into multiple parts (default: False)
  -s chunk_size, --chunk-size chunk_size
                        Chunk size when splitting transcript, also used to
                        determine whether to split (default: 2000)
  -n, --dry-run         Dry run (default: False)
  -p PAGES [PAGES ...], --pages PAGES [PAGES ...]
                        Only include specified page numbers (default: None)
  -M, --merge           Merge contents of all pages before processing
                        (default: False)
  -w WHAT, --what WHAT  Initial knowledge you want to insert before the PDF
                        content in the prompt (default: the content of a PDF
                        file)


```

### `ytprompt`

```
$ ytprompt --help

usage: ytprompt [-h] [-V] [-c] [-e] [-m model] [-S] [-s chunk_size] [-n]
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
  -S, --split           Split the prompt into multiple parts (default: False)
  -s chunk_size, --chunk-size chunk_size
                        Chunk size when splitting transcript, also used to
                        determine whether to split (default: 2000)
  -n, --dry-run         Dry run (default: False)

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