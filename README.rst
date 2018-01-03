.. contents::

Introduction
============

LitePkg is the spiritual successor to the project referred to as `"the
Toolchest"`_, which was a highly portable package manager implemented as a set
of POSIX shell scripts.  Litepkg shares no code, nor even fundamental design
princiiples with the Toolchest, although it does attempt to solve the same
problem: managing installation for very small projects. This is the solution
for dealing with one-off shell scripts, small C programs, and so on. Key
features include:

* Portability: written in pure Python 3, litepkg should work on any UNIX-like
  system that supports Python 3.

* Ease of use: minimal fuss to install and update packages.

* Ease of packaging: LitePkg is targeted at developers of small projects who
  want a convenient way to distribute them; LitePkg intended to make
  packaging as easy as possible, so a lone developer can package their
  software in a few minutes of work.

How it Works
------------

LitePkg is in fact a clever abuse of Python's import system. Package installers
(which use the extension ``.litepkg`` by convention) are simply valid Python
files, which must contain a single specially named class that contains package
metadata and an installation script. An API is provided to handle common
installation-related tasks such as "download this URL", "untar this file", "run
this build script", and so on.

LitePkg packages are installed by first downloading any necessary files into a
temporary directory, then running any required compilation or configuration
steps. Then, the packager can mark any number of the resulting files and
directories as "artifacts" that need to be present on the system for the
program to run. Finally, the packager specifies which of the artifacts need to
be symlinked into ``$PATH`` in order for the program to be usable. The
temporary directory is then discarded. All of the ugly file management,
symlinking, and so on is handled by LitePkg, so developers can get on with
their business and not be bogged down in complicated packaging details.

This approach was selected because it allows for maximum utility in exchange
for minimal development effort - Python is already an excellent and complete
language. The first attempt at LitePkg cam in Fall 2017, and attempted to
define an entire DSL from scratch to accomplish essentially the same task, and
the project fizzled due to the difficulty of so doing. By using a tried and
trusted language, LitePkg can focus on being a great package manager, rather
than also having to implement a mediocre programming language on the side.

Project Status
==============

LitePkg is in a very early stage of development, and is not yet ready for
production use. Namely, the package installer API is not stabilized, so
installers written against the current implementation may or may not be
compatible with the first release (0.0.1).

Planned Features
----------------

* Package repositories in the form of git repositories.

* Adding package installers by URL.

* Adding package installers by GitHub name (i.e. ``jsmith/reponame``).

* Package update operation.

* Robust configuration & automation support.


.. _`"the Toolchest"`: http://cdaniels.net/projects.html#the-toolchest
