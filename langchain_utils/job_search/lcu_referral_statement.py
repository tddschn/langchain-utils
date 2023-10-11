#!/usr/bin/env python3
"""
Author : Xinyuan Chen <45612704+tddschn@users.noreply.github.com>
Date   : 2023-10-10
Purpose: Generate and copy the referral statement
"""

import argparse
from pathlib import Path
import sys
from langchain_utils.job_search.config import (
    referral_default_schools_list,
    referral_statement_default_relationship_with_referral,
    referral_statement_default_referral_name,
    referral_statement_default_additional_requirements,
    referral_statement_default_resume_markdown_path,
)

from langchain_utils.job_search.prompts import REFERRAL_STATEMENT
import pyperclip


def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Generate and copy the referral statement',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # add options for every config options
    parser.add_argument(
        '-s',
        '--school',
        help='the schools they both attended',
        metavar='str',
        type=str,
        choices=referral_default_schools_list,
        default=referral_default_schools_list[0],
    )

    parser.add_argument(
        '-r',
        '--relationship',
        help='the relationship with the referral',
        metavar='str',
        type=str,
        default=referral_statement_default_relationship_with_referral,
    )

    parser.add_argument(
        '-n',
        '--name',
        help='the name of the referral',
        metavar='str',
        type=str,
        default=referral_statement_default_referral_name,
    )

    parser.add_argument(
        '-a',
        '--additional-requirements',
        help='additional requirements for the referral',
        metavar='str',
        type=str,
        default=referral_statement_default_additional_requirements,
    )

    parser.add_argument(
        '-r',
        '--resume-path',
        help='the path to the markdown resume',
        metavar='PATH',
        type=Path,
        default=referral_statement_default_resume_markdown_path,
    )

    return parser.parse_args()


def main():
    """Make a jazz noise here"""

    args = get_args()

    from langchain.prompts import PromptTemplate

    prompt = PromptTemplate.from_template(REFERRAL_STATEMENT)
    formatted_prompt = prompt.format(
        company_name=args.school,
        relationship_with_referral=args.relationship,
        referral_name=args.name,
        additional_requirements=args.additional_requirements,
        resume_markdown_content=args.resume_path.read_text(),
    )

    pyperclip.copy(formatted_prompt)
    char_count = len(formatted_prompt)
    print(
        f'Referral statement copied to clipboard. {char_count} chars in total',
        file=sys.stderr,
    )


if __name__ == '__main__':
    main()