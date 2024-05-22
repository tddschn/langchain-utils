# langchain-utils

LangChain Utilities

- [langchain-utils](#langchain-utils)
  - [Prompt generation using LangChain document loaders](#prompt-generation-using-langchain-document-loaders)
    - [Demos](#demos)
    - [`pandocprompt`](#pandocprompt)
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

{{ prompt_commands_and_usages }}

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
