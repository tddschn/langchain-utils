import argparse
from . import __version__


def get_get_prompt_base_arg_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        '-V',
        '--version',
        action='version',
        version=f'%(prog)s {__version__}',
    )
    parser.add_argument(
        '-c', '--copy', help='Copy the prompt to clipboard', action='store_true'
    )
    parser.add_argument(
        '-e', '--edit', help='Edit the prompt and copy manually', action='store_true'
    )
    parser.add_argument(
        '-m',
        '--model',
        help='Model to use',
        metavar='model',
        type=str,
        default='gpt-3.5-turbo',
    )
    parser.add_argument(
        '-S',
        '--split',
        help='Split the prompt into multiple parts',
        action='store_true',
    )
    parser.add_argument(
        '-s',
        '--chunk-size',
        help='Chunk size when splitting transcript, also used to determine whether to split',
        metavar='chunk_size',
        type=int,
        default=2000,
    )
    parser.add_argument(
        '-P',
        '--parts',
        help='Parts to select in the processes list of Documents',
        type=int,
        nargs='+',
        default=None,
    )
    parser.add_argument('-n', '--dry-run', help='Dry run', action='store_true')
    return parser
