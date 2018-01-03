#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse
import logging
import logger
import litepkg
import pkgutils
import imp
import re
import config
import tempfile
import shutil

def ensure_dir_exists(directory):
    """ensure_dir_exists

    Make sure the directory exists, creating it if it does not.

    :param directory:
    """

    logging.debug("Ensuring that '{}' exists... ".format(directory))

    if not os.path.exists(directory):
        logging.debug("'{}' does not exist, attempting to create it... ")
        os.makedirs(directory, exist_ok=True)
    else:
        logging.debug("'{}' exists already, no action required."
                      .format(directory))

    if not os.path.exists(directory):
        logging.error("'{}' does not exist and could not bre created.")
        exit(1)


def validate_dirs():
    """validate_dirs

    Ensure that the package, artifacts, and binaries directories all exist,
    and create them if they do not already exist.

    """

    logging.debug("Validating directories... ")

    for d in [config.args.package_directory,
              config.args.artifacts_directory,
              config.args.binaries_directory]:
        ensure_dir_exists(d)


    logging.debug("Validation successfully.")


def show_verb_help():
    print("Placeholder help message.")

def load_module(path):
    logging.debug("Attempting to load module from '{}'".format(path))
    module_name = "LitePkgPackage"
    module = imp.load_source(module_name, path)
    logging.debug("Module loaded successfully")
    return module

def validate_package_module(mod):
    try:
        foo = mod.package_name
        foo = mod.package_synopsis
        return True
    except Exception as e:
        return False

def index_packages():
    """index_packages

    Retrieve a list of module objects from the files in the package directory.
    """
    installer_files = []
    for root, dirs, files in os.walk(config.args.package_directory):
        for f in files:
            if f.endswith(".litepkg"):
                 installer_files.append(os.path.join(root, f))
    logger.prettyLog(installer_files, msg="candidate files:")

    installer_modules = []
    for f in installer_files:
        try:
            m = load_module(f)
            m = m.LitePkgPackage() # instantiate a singleton
            if validate_package_module(m):
                installer_modules.append(m)
            else:
                logging.warning("Malformed package: {}".format(m))
        except Exception as e:
            logging.debug("Exception while loading module: {}".format(e))

    return installer_modules

def format_package_list(packages):
    s = ""
    for package in packages:
        s += "{} - {}".format(package.package_name, package.package_synopsis)
        s += "\n"

    return s

def search_package_by_name(packages, query):
    r = re.compile(query)
    matches = []
    for p in packages:
        if r.match(p.package_name):
            matches.append(p)
    return matches

def enter_work_dir():
    """enter_work_dir

    Create and cd to a temp directory, it's name is returned.
    """

    temp_dir = tempfile.mkdtemp()
    logging.debug("Setup work directory '{}'".format(temp_dir))
    os.chdir(temp_dir)

    return temp_dir


def remove_work_dir(temp_dir):
    logging.debug("Cleaning work dir '{}'".format(temp_dir))
    os.chdir(config.start_cwd)
    shutil.rmtree(temp_dir)


def install_package(package_name):
    work_dir = enter_work_dir()
    packages = index_packages()
    candidates = \
            search_package_by_name(packages, ".*{}.*".format(package_name))
    if len(candidates) == 0:
        logging.error("No results found for query: '{}'".format(package_name))
    elif len(candidates) > 1:
        logging.error(
                "Too many results found for query '{}', request is ambiguous"
                .format(package_name))
        print(format_package_list(candidates))
    else:
        candidates[0].install_package()

    remove_work_dir(work_dir)


def handle_verb():
    """handle_verb

    Consider config.args.verb and take an appropriate action.

    """

    verb = config.args.verb
    targets = config.args.targets

    if verb == "help":
        show_verb_help()
        exit(0)
    elif verb == "list":
        print(format_package_list(index_packages()))
    elif verb == "install":
        for package_name in targets:
            install_package(package_name)
    else:
        logging.error("Unknown verb '{}'".format(verb))
        exit(1)


def main():
    home_dir = os.path.expanduser("~")

    parser = argparse.ArgumentParser()

    parser.add_argument("--package_directory", "-p",
                        default=os.path.join(home_dir, ".litepkg/packages"),
                        help="Set directory for package installer directory." +
                        " (default: ~/.litepkg/packages)")

    parser.add_argument("--artifacts_directory", "-a",
                        default=os.path.join(home_dir, ".litepkg/artifacts"),
                        help="Directory for any artifacts. (default: " +
                        "~/.litepkg/artifacts")

    parser.add_argument("--binaries_directory", "-b",
                        default=os.path.join(home_dir, "bin"),
                        help="Directory where executables should be " +
                        "symlinked. (default: ~/bin)")

    parser.add_argument("--console_log_level", "-l",
                        default="INFO", help="Log level for console output." +
                        " (default: INFO)")

    parser.add_argument("--file_log_level", "-L",
                        default="DEBUG", help="Log level for log file." +
                        " (default: DEBUG)")

    parser.add_argument("--log_file", "-f", default="/dev/null",
                        help="Log file path. (default: /dev/null)")

    parser.add_argument("--verbose", "-v", default=False, action="store_true",
                        help="Show verbose output on the console, implies" +
                        " --console_log_level DEBUG.")

    parser.add_argument("verb", help="litepkg verb")

    parser.add_argument("targets", nargs="*", help="verb targets")

    config.args = parser.parse_args()
    config.start_cwd = os.getcwd()

    if config.args.verbose:
        config.args.console_log_level = "DEBUG"

    logger.setup(logPath=config.args.log_file,
                 fileLevel=config.args.file_log_level,
                 consoleLevel=config.args.console_log_level)

    logging.debug("Application started.")
    logger.prettyLog(config.args, msg="args")


    config.args.package_directory = \
            os.path.realpath(config.args.package_directory)
    config.args.artifacts_directory= \
            os.path.realpath(config.args.artifacts_directory)
    config.args.binaries_directory= \
            os.path.realpath(config.args.binaries_directory)

    validate_dirs()

    handle_verb()



if __name__ == "__main__":
    main()
