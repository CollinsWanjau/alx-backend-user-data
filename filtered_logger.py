#!/usr/bin/env python3
"""
Regex-ing
"""
import re


def filter_datum(fields, redaction, message, separator):
    for f in fields:
        message = re.sub(f'{f}=.*?{separator}',
                         f'{f}={redaction}{separator}', message)
    return message