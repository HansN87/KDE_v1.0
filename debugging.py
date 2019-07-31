# -*- coding: utf-8 -*-

import logging
import os.path
import sys

from config import CFG

def setup_logger(name, log_level):
    """Initializes logger with a given name and a log level.

    Parameters
    ----------
    name : str
        Logger name. Loggers hierarchy is defined using dots as separators.
    log_level : int
        The log level.  The ``logging`` module predefines levels, e.g.
        ``logging.DEBUG``.
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

def setup_console_handler(name, log_level, log_format=None, stream=None):
    """Initializes `StreamHandler` for a logger with a given name and sets its
    handling level.

    Parameters
    ----------
    name : str
        Logger name. Loggers hierarchy is defined using dots as separators.
    log_level : int
        The log level. The ``logging`` module predefines levels, e.g.
        ``logging.DEBUG``.
    log_format : str | None
        The format of log records in the final output.
        If set to `None`, the log format is taken from the configuration.
    stream : data stream | None
        The stream that the handler should use. Default stream is `sys.stderr`.
    """
    if(log_format is None):
        log_format = CFG['debugging']['log_format']
    if(stream is None):
        stream = sys.stderr

    logger = logging.getLogger(name)

    # Create and add `StreamHandler` to the logger.
    sh = logging.StreamHandler(stream=stream)
    sh.setLevel(log_level)
    sh.setFormatter(logging.Formatter(log_format))
    logger.addHandler(sh)

def setup_file_handler(name, log_level, filename, path=None, log_format=None,
        mode='a'):
    """Initializes `FileHandler` for a logger with a given name and sets its
    handling level.

    Parameters
    ----------
    name : str
        Logger name. Loggers hierarchy is defined using dots as separators.
    log_level : int
        The log level. There are predefined levels, e.g. ``logging.DEBUG``.
    filename : str
        The filename of the specified file which is opened and used as the
        stream for logging.
    path : str | None
        The path under which the log file should be stored.
        If set to `None`, the project's working directory will be used.
    log_format : str | None
        The format of log records in the final output.
        If set to `None`, the log format is taken from the configuration.
    mode : str
        File opening mode. Default is 'a' for appending.
    """
    if(log_format is None):
        log_format = CFG['debugging']['log_format']
    if(path is None):
        path = CFG['project']['working_directory']

    logger = logging.getLogger(name)

    pathfilename = os.path.join(path, filename)

    # Create and add `FileHandler` to the logger.
    fh = logging.FileHandler(pathfilename, mode=mode)
    fh.setLevel(log_level)
    fh.setFormatter(logging.Formatter(log_format))
    logger.addHandler(fh)
