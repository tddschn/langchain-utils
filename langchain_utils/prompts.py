#!/usr/bin/env python3

REPLY_OK_IF_YOU_READ_TEMPLATE = '''
Below is {what}, reply "OK" if you read:

"""
{content}
"""
'''.strip()

REPLY_OK_IF_YOU_READ_TEMPLATE_SPLITTED_FIRST = '''
Below is the first part of {what}, reply "Read part 1 OK" if you read:

"""
{content}
"""
'''.strip()

REPLY_OK_IF_YOU_READ_TEMPLATE_SPLITTED_CONTINUED = '''
Below is the next part of {what}, reply "Read part {x} OK" if you read:

"""
{content}
"""
'''.strip()
