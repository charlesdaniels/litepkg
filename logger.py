########10########20########30## DOCUMENTATION #50########60########70########80
#
#  OVERVIEW
#  ========
#
#  This library serves to wrap a few simple, useful logging-related tools and
#  functionalities. It utilizes Python's built in `logging` module, as well as
#  `pprint`. This module has no external dependencies, and should work in
#  Python 2.7.x and Python 3.x.
#
#  LOG FORMAT
#  ==========
#
#  This module is hard-coded to use the following log format::
#
#    <[ timestamp | caller | loglevel | message ]>
#
#  An example log message follows::
#
#    TODO
#
#  TABLE OF METHOD SIGNATURES
#  ==========================
#
#  setup(logPath, fileLevel, consoleLevel)
#  logWithExplicitLevel(msg, level)
#  prettyLog(obj, level="DEBUG", msg='')
#
########10########20########30##### LICENSE ####50########60########70########80
#  Copyright (c) 2016, Charles Daniels
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#
#  1. Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
#  3. Neither the name of the copyright holder nor the names of its
#     contributors may be used to endorse or promote products derived from
#     this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
#  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#  POSSIBILITY OF SUCH DAMAGE.
#
########10########20########30########40########50########60########70########80

import sys
import logging
import os
import pprint

########10########20########30###### setup #####50########60########70########80
#
#  OVERVIEW
#  ========
#
#  This method is used to set up Python's `logging` module.
#
#  USAGE
#  =====
#
#    logPath  . . . absolute or relative path to log file (defaults to
#                   ./$0.log)
#
#    fileLevel  . . lowest log level which will go to the log file (defaults
#                   to DEBUG)
#
#    consoleLevel . the lowest log level which will go to the console
#                   (defaults to INFO)
#
def setup(logPath="./"+sys.argv[0]+".log",
          fileLevel="DEBUG",
          consoleLevel="INFO"):

    formatString = '<[ %(asctime)s | %(funcName)15.15s() | %(levelname)-10.10s | %(message)s ]>'

    # setup logging
    # http://stackoverflow.com/questions/13733552/logger-configuration-to-log-to-file-and-print-to-stdout
    logFormatter = logging.Formatter(formatString)
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.DEBUG)

    fileHandler = logging.FileHandler(os.path.join(logPath))
    fileHandler.setFormatter(logFormatter)
    fileHandler.setLevel(fileLevel)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)

    consoleHandler.setLevel(consoleLevel)
    rootLogger.addHandler(consoleHandler)


########10########20########30########40########50########60########70########80
#
#  OVERVIEW
#  ========
#
#  Logs a string using the python logging module, with the log level passed
#  explicitly as an argument. Useful when loglevel is generated programatially.
#
#  USAGE
#  =====
#
#    msg . . . the message to log
#
#    level . . the log level to use (as a string)
#
def logWithExplicitLevel(msg, level):


    logLevels = {"DEBUG":     10,
                 "INFO":      20,
                 "WARNING":   30,
                 "ERROR:":    40,
                 "CRITICAL":  50}

    if level not in logLevels.keys():
        try:
            # maybe somebody passed us an integer log level directly
            level = int(level)
        except ValueError:
            # nope, this was not an integer log level
            logging.error("failed to log  message with level '{}': \n{}"
                          .format(level, msg))
    else:
        # the level is for a loglevel we know about
        level = logLevels[level]

    assert isinstance(level, int) # level should always be an int by this point
    # actually do the logging part
    logging.log(level, msg)


########10########20########30########40########50########60########70########80
#
#  OVERVIEW
#  ========
#
#  Logs an object to the console, but runs it through pprint first (via
#  pformat). This is handy when you want to log large data structures that can
#  be unreadable when using __repr__ or __str__
#
#  USAGE
#  =====
#
#    obj . . . . the object to log (must be supported by pprint.pformat) -
#                this is NOT checked
#
#    level . . . log level to log the object with (defaults to  "DEBUG")
#
#    msg   . . . optional message to prepend to the object's pretty
#                representation
def prettyLog(obj, level="DEBUG", msg=''):
    prettyStr = pprint.pformat(obj)  # prettify the object
    prettyStr = msg + "\n" + prettyStr
    for line in prettyStr.split("\n"):
        logWithExplicitLevel(line, level)  # now perform the logging

