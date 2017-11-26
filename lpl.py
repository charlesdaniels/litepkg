#!/usr/bin/env python3

import os
import sys
import argparse
import logging
import logger
import wget


########10########20########30#### argparse ####50########60########70########80

parser = argparse.ArgumentParser(description="LitePkg LPL interpreter")
parser.add_argument("--input", "-i", default="/dev/stdin",
                    help="Input file to parse LPL code from " +
                    "(default is stdin)")
parser.add_argument("--debug", default=False, action="store_true",
                    help="Assert for debug output")
parser.add_argument("--startup", "-s", required=True,
                    help="LPL startup file")

########10########20########3 directive handlers 0########60########70########80

"""
Directives are processed by consuming a token-dict and an interpreter state.
Having so done, they mutate the interpreter state and return it for further
processing.
"""

def directive_pragma(tokens, state):
    logging.debug("processing tokens '{}' as pragma".format(tokens))

    if len(tokens['parameters']) is not 1:
        logging.error("Syntax error: pragma takes exactly 1 parameter")
        raise Exception("")

    state['pragma'] = tokens['parameters'][0]
    state['fetch_done'] = False

    return state

def directive_assign(tokens, state):
    logging.debug("processing tokens '{}' as assign".format(tokens))

    if 'variables' not in state:
        state['variables'] = {}

    if len(tokens['parameters']) < 2:
        logging.error("Syntax error: at least a variable name and value is" +
                " required to set a varaible to a value")
        raise Exception("")

    state['variables'][tokens['parameters'][0]] = \
            ' '.join(tokens['parameters'][1:])
    return state

def directive_link(tokens, state):
    logging.debug("processing tokens '{}' as link".format(tokens))

    assert_pragma_set(state)
    assert_env_initialized(state)
    assert_param_count(tokens, 1, 1)

    if not state['fetch_done']:
        run_fetch(state)

    return state

def directive_envconf(tokens, state):
    logging.debug("processing tokens '{}' as envconf".format(tokens))

    assert_param_count(tokens, 2)

    field = tokens['parameters'][0]
    value = ' '.join(tokens['parameters'][1:])

    if field not in allowed_envconf_fields:
        logging.error("Unknown envconf field '{}'".format(field))
        raise Exception("")

    if 'env' not in state:
        state['env'] = {}

    state['env'][field] = value

    return state

########10########20########30### assertions ###50########60########70########80

def assert_env_initialized(state):
    """assert_env_initialized

    crash if env has not been setup sufficiently

    :param state:
    """

    if 'env' not in state:
        logging.error("env has not been initialized")
        raise Exception("")

    for field in allowed_envconf_fields:
        if field not in state['env']:
            logging.error("env field '{}' is not initialized")
            raise Exception("")

    assert_pkg_root(state)


def assert_param_count(tokens, min=0, max=100000):
    """assert_param_count

    Crash if len(tokens['parameters']) is not >=min and <= max

    :param tokens:
    :param min:
    :param max:
    """

    if len(tokens['parameters']) < min or len(tokens['parameters']) > max:
        logging.error("Incorrect number of parameters for directive '{}'"
                      .format(tokens['directive']))

        raise Exception("")


def assert_pragma_set(state):
    """assert_pragma_set

    Crash if state['pragma'] is not set to a valid pragma

    :param state:
    """

    if 'pragma' not in state:
        logging.error("No pragma specified")
        raise Exception("")

    if state['pragma'] not in ['single']:
        logging.error("Pragma '{}' is not known".format(state['pragma']))
        raise Exception("")

def assert_variable(state, varname):
    """assert_variable

    Crash is state does not contain the variable

    :param state:
    :param varname:
    """

    if 'variables' not in state:
        logging.error("Variable '{}' not in state".format(varname))
        raise Exception("")

    if varname not in state['variables']:
        logging.error("Variable '{}' not in state".format(varname))
        raise Exception("")

def assert_pkg_root(state):
    """assert_pkg_root

    Make sure pkg_root exists, if not create it, crash on failure.

    :param state:
    """

    pkg_root = state['env']['lpl_pkg_root']
    pkg_root = os.path.expanduser(pkg_root)
    if not os.path.exists(pkg_root):
        os.makedirs(pkg_root, exist_ok=True)

    if not os.path.exists(pkg_root):
        logging.error("lpl_pkg_root '{}' does not exist".format(pkg_root))
        raise Exception("")

########10########20########30# utility methods 50########60########70########80

def run_fetch(state):
    """run_fetch

    Perform  the appropriate fetch stage for the set pragma.

    :param state:
    """

    assert_pragma_set(state)
    assert_variable(state, "url")
    assert_variable(state, "name")

    fetch_URL = state['variables']['url']
    fetch_name = state['variables']['name']

    logging.debug("Fetching URL '{}'".format(fetch_URL))

    if state['pragma'] == 'single':

        output_file_path = os.path.join(state['env']['lpl_pkg_root'],
                                        fetch_name)
        output_file_path = os.path.expanduser(output_file_path)

        if os.path.exists(output_file_path):
            os.remove(output_file_path)

        wget.download(fetch_URL, output_file_path)

    else:

        logging.error("Unsupported pragma for run_fetch '{}'"
                      .format(state['pragma']))

########10########20####### language implementation ######60########70########80

def tokenize_line(line):
    """tokenize_line

    :param line: the line to tokenize

    :returns: None if the line should be ignored, or hashtable with the key
    'directive' for the line directive, and 'parameters' for a string list
    of parameters.
    """

    line = line.strip()

    logging.debug("tokenizing line '{}'".format(line))

    # ignore blank lines
    if len(line) <= 0:
        logging.debug("line is empty")
        return None

    # ignore lines that begin with #
    if line[0] is '#':
        logging.debug("line is a comment")
        return None

    tokenlist = line.split()
    directive = tokenlist[0]
    parameters = []
    if len(tokenlist) > 1:
        parameters = tokenlist[1:]

    logging.debug("directive is '{}'".format(directive))
    logging.debug("parameters are '{}'".format(parameters))

    tokens = {}
    tokens["directive"] = directive
    tokens["parameters"] = parameters

    return tokens

def execute(data, state = {}):
    """execute

    Execute the argument (which should be iterable as LPL statements) as
    LPL source and return the state afterwards.

    :param inputfile:
    """

    linum = 0

    for line in data:
        linum += 1
        tok = tokenize_line(line)

        if tok is None:
            # line requires no further processing
            continue

        # pass the line to an appropriate handler, or panic
        if tok['directive'] in directive_handlers:
            #  try:
            if True:
                state = directive_handlers[tok['directive']](tok, state)
            #  except Exception as e:
            #      logging.error("Failed to handle directive '{}' on line '{}"
            #                    .format(tok['directive'], linum))
            #      logger.prettyLog(e, "DEBUG", "Encountered exception ")

            logger.prettyLog(state,
                    msg="Interpreter state at after line {}: ".format(linum))

        else:
            logging.error("Unrecognized directive '{}' on line {}"
                          .format(tok['directive'], linum))
            continue  # change to exit(1) once all directives impelemented

    return state


########10########20########30### static data ##50########60########70########80

allowed_envconf_fields = ["lpl_pkg_root"]

directive_handlers = {"pragma" : directive_pragma,
                      "assign" : directive_assign,
                      "link"   : directive_link,
                      "envconf": directive_envconf}

########10########20########30 CLI app handling 50########60########70########80

def main():
    args = parser.parse_args()
    consoleLevel = "INFO"
    if args.debug:
        consoleLevel = "DEBUG"

    logger.setup(logPath="/dev/null", consoleLevel=consoleLevel)

    logging.debug("starting LPL interpreter")
    logger.prettyLog(args, msg="Arguments")

    fin = open(args.input, "r")
    startupfin = open(args.startup, "r")

    logging.debug("executing startup file")
    state = execute(startupfin)

    logging.debug("executing program")
    state = execute(fin, state)

    fin.close()

if __name__ == "__main__":
    main()

