#!/usr/bin/env python3
"""
Regex-ing
"""
# from collections.abc import Mapping
import logging
import re
from typing import Any, List
import logging
import mysql.connector
import os


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


def get_logger() -> logging.Logger:
    """
    Create and configure a logger for handling user data with sensitive
    information redaction.

    Returns:
        logging.Logger: The configured logger for user data.
    """
    # Create the logger with the name user_data and set its level to
    # `loggin.INFO`
    user_data_logger = logging.getLogger("user_data")
    user_data_logger.setLevel(logging.INFO)
    # Disable propagation to other loggers (default behaviour)
    user_data_logger.propagate = False
    # create a stream handler
    stream_handler = logging.StreamHandler()
    # create a redactingformatter instance
    redacting_formatter = RedactingFormatter(list(PII_FIELDS))
    # set the formatter for the Streamhandler to the RedactingFormatter
    stream_handler.setFormatter(redacting_formatter)
    stream_handler.setLevel(logging.INFO)
    # add the stream handler to the "use_data" logger
    user_data_logger.addHandler(stream_handler)

    # user_data_logger.propagate = False
    return user_data_logger


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a connector to the database
    """
    db_host = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_username = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    db_name = os.environ.get("PERSONAL_DATA_DB_NAME", "")

    if db_name is None:
        raise ValueError("The required PERSONAL_DATA_DB_NAME is missing.")

    connection = mysql.connector.connect(
        host=db_host,
        user=db_username,
        password=db_password,
        database=db_name
    )

    return connection


def main():
    """
    Main function to retrieve and log user data from a MySQL database.

    Returns:
        None
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute = "SELECT * FROM users"
    field_names = [i[0] for i in cursor.description]

    logger = get_logger()

    for row in cursor:
        str_row = ''.join(f'{f}={str(r)};' for r, f in zip(row, field_names))
        logger.info(str_row.strip())

    cursor.close()
    db.close()


class RedactingFormatter(logging.Formatter):
    """
    Custom logging formatter for redacting sensitive information in log
    messages.
    This formatter extends the base logging.Formatter to provide redacted log
    messages by replacing sensitive information with a predefined redaction
    string.

    Attributes:
        - REDACTION (str): The redaction string used to replace sensitive
        information.
        - FORMAT (str): The log message format, including placeholders for
        various log record fields.
        SEPARATOR (str): The separator used to join multiple log messages when
        redacting multiple items.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)s-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initializes a RedactingFormatter instance.

        Args:
        fields (List[str]): A list of strings representing the fields to be
        redacted in log messages.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format a log record after redacting sensitive information in the log
        message.

         Args:
        record (logging.LogRecord): The log record to be formatted.

        Returns:
            str: The formatted log message.

        Parameters:
            - `self.fields`: A list of strings representing fields to be
            redacted.
            - `self.REDACTION`: The redaction string (e.g., '***').
            - `self.SEPARATOR`: The character used to separate fields in the
            log message.

        After filtering the log message, this method calls the `format` method
        of the parent class (logging.Formatter) to complete the formatting
        process.
        """
        # We first call the filter_datum to filter out sensitive information
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg,
                                  self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
