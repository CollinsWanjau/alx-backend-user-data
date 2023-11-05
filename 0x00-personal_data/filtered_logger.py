#!/usr/bin/env python3
"""
Regex-ing
"""
# from collections.abc import Mapping
import logging
import re
from typing import Any, List
import logging


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    A function that returns the log message obfuscated
    Args:
        - Fields: a list of strings representing all the fields to obfuscated
        - Redaction: a string representing by what the field will be obfuscated
        - message: a string representing the log line
        - separator: a string representing by which character is separating all
        fields in the log line (message)
    """
    for f in fields:
        message = re.sub(f'{f}=.*?{separator}',
                         f'{f}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)s-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        # We first call the filter_datum to filter out sensitive information
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg,
                                  self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
