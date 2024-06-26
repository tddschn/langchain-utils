import argparse
from langchain_utils import __version__
from langchain_utils.utils import (
    save_stdin_to_tempfile,
    save_clipboard_to_tempfile,
    get_default_chunk_size,
)
from langchain_utils.config import MODEL_TO_CONTEXT_LENGTH_MAPPING, DEFAULT_MODEL


def get_get_prompt_base_arg_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "-c", "--copy", help="Copy the prompt to clipboard", action="store_true"
    )
    parser.add_argument(
        "-e", "--edit", help="Edit the prompt and copy manually", action="store_true"
    )
    parser.add_argument(
        "-m",
        "--model",
        help="Model to use. This only affects the chunk size. Use -S to disable splitting (infinite chunk size).",
        metavar="model",
        type=str,
        default=DEFAULT_MODEL,
    )
    parser.add_argument(
        "-S",
        "--no-split",
        help="Do not split the prompt into multiple parts (use this if the model has a really large context size)",
        action="store_true",
    )
    parser.add_argument(
        "-s",
        "--chunk-size",
        help="Chunk size when splitting transcript, also used to determine whether to split, defaults to 1/2 of the context length limit of the model",
        metavar="chunk_size",
        type=int,
        # default to 1/2 of the context length limit
        # default=MODEL_TO_CONTEXT_LENGTH_MAPPING[DEFAULT_MODEL] // 2,
        # default=2000,
        default=None,
    )
    parser.add_argument(
        "-P",
        "--parts",
        help="Parts to select in the processes list of Documents",
        type=int,
        nargs="+",
        default=None,
    )

    parser.add_argument(
        "-r",
        "--raw",
        help="Wraps the content in triple quotes with no extra text",
        action="store_true",
    )

    parser.add_argument(
        "-R",
        "--raw-no-quotes",
        help="Output the content only",
        action="store_true",
    )

    parser.add_argument(
        "--print-percentage-non-ascii",
        help="Print percentage of non-ascii characters",
        action="store_true",
    )

    parser.add_argument("-n", "--dry-run", help="Dry run", action="store_true")

    parser.add_argument("--out", help="Output file", type=str, default=None)
    return parser


def postprocess_args(args):
    """Common post processing for args in all scripts except the YouTube one"""
    if args.from_clipboard:
        args.path = [save_clipboard_to_tempfile()]
    elif not args.path:
        args.path = [save_stdin_to_tempfile()]
    args.chunk_size = get_default_chunk_size(args.model)
    if args.out:
        args.no_split = True
    return args
