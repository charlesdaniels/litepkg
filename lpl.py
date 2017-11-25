#!/usr/bin/env python3

import os
import sys
import argparse
import logging
import logger

parser = argparse.ArgumentParser(description="LitePkg LPL interpreter")
parser.add_argument("--input", "-i", default="/dev/stdin",
                    help="Input file to parse LPL code from " +
                    "(default is stdin)")
parser.add_argument("--debug", default=False, action="store_true",
                    help="Assert for debug output")

def tokenize_line(line):
    """tokenize_line

    :param line: the line to tokenize

    :returns: None if the line should be ignored, or hashtable with the key
    'directive' for the line directive, and 'parameters' for a string list
    of parameters.
    """

    line = line.strip()

    logging.debug("\ttokenizing line '{}'".format(line))

    # ignore blank lines
    if len(line) <= 0:
        logging.debug("\t\tline is empty")
        return None

    # ignore lines that begin with #
    if line[0] is '#':
        logging.debug("\t\tline is a comment")
        return None

    tokenlist = line.split()
    directive = tokenlist[0]
    parameters = []
    if len(tokenlist) > 1:
        parameters = tokenlist[1:]

    logging.debug("\t\tdirective is '{}'".format(directive))
    logging.debug("\t\tparameters are '{}'".format(parameters))

    tokens = {}
    tokens["directive"] = directive
    tokens["parameters"] = parameters

    return tokens

def main():
    args = parser.parse_args()
    consoleLevel = "INFO"
    if args.debug:
        consoleLevel = "DEBUG"

    logger.setup(logPath="/dev/null", consoleLevel=consoleLevel)

    logging.debug("starting LPL interpreter")
    logger.prettyLog(args, msg="Arguments")

    fin = None
    try:
        fin = open(args.input, "r")
    except Exception as e:
        logging.error("Failed to open input file '{}' with exception '{}'"
                      .format(args.input, fin))
        exit(1)

    for line in fin:
        tok = tokenize_line(line)



    fin.close()



if __name__ == "__main__":
    main()
