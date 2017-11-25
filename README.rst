#######
LitePkg
#######

*Small packages for small projects*

Overview
========

LitePkg is still early in it's development, and is mostly undergoing planning
and early testing at this time. It is not ready for production use, and many
features may be missing, incomplete, or broken.

LitePkg is a simple, lightweight package manager for small projects. LitePkg is
intended to package small projects of the sort that frequently are not picked
up by larger package managers like Aptitude, Yum, or Homebrew. In particular,
it aims to make packaging as easy an fuss-free for developers as possible.

LitePkg's roots like in the Toolchest_ of Charles Daniels, which set out
with similar goals. LitePkg starts fresh with the insights gained from the
toolchest.

LitePkg, aside from the Toolchest, draws inspiration from the BSD ports
system and the ArchLinux AUR.

Implementation
==============

LitePkg is principally implemented by a set of utilities and glue logic
surrounding a domain-specific language used for describing how packages should
be installed, called the *Lite Package Language*, or LPL.

LPL is still under development, and does not have a formal specification yet.

In lieu of a formal specification, consider some LPL samples.

::

        # this is a comment

        # the project we are packaging is hosted in a git repository
        pragma git

        # URL to clone from
        assign url git://example.com/someproject.git

        # output directory to clone the repository to
        assign dir someproject

        # set the branch (default is "master")
        assign branch v1-RELEASE

        # specify what files relative to $dir need to be linked into PATH
        link bin/sometool  # this is relative to the dir assigned above
        link bin/anothertool


::

        pragma git
        assign url git://example.com/coolproject.git
        assign dir coolproject

        # shell commands to build the project
        build make clean
        build ./configure
        build make

        link coolbinary

::

        pragma archive
        assign url https://example.com/releases/1.1.4-neatprogram.tar.gz
        assign file neatprogram.tar.gz
        untar neatprogram # untars $file into a directory neatprogram

        # build commands happen in the dir we untar to
        build make clean
        build make

        link build/neatprogram


::

        # URL points directly to a file to stick into $PATH
        pragma single
        assign url...
        assign name coolfile

LPL Overview
------------

LPL takes a bit after TCL in that a single *statement* is simply a line of
text, which contains several space-delimited *elements*, the first of which
is the *directive*, and the remaining of which are *parameters*.

Leading and trailing whitespaces are ignored.

Lines where the first non-whitespace character is ``#`` are ignored.

Before execution of an LPL script begins in earnest, a *pragma* must be defined;
this lets LitePkg know what type of package it is dealing with. Pragmas
include:

* ``git`` - implies the package's sources should be obtained by ``git``
* ``archive`` - implies the package's sources are contained in a ``tar``
  archive
* ``single`` - implies the package consists of a single file to be downloaded
  and linked into ``$PATH``.

Pragmas generally require that some information is provided in order to operate
in a useful fashion. Such information is populated via the ``assign``
directive, which populates *variables*. Unlike variables in more traditional
programming languages, the variables that can be defined by an LPL program are
restricted by the interpreter according to what pragma is in use.  Assignment
directives take the form of ``assign varname value of the variable`` which
would result in ``varname`` holding the value ``value of the variable``.

In some cases, certain shell commands need to be issued in order for a package
to be compiler or otherwise prepared for installation or use. This is
accomplished through the use of ``build`` statements, for which all parameters
are executed as a shell command. If the command returns a non-zero exit code,
the LPL script crashes itself for softy. An example of a build command might
be ``build make``, which would run the command ``make``. Build commands are
always executed from the top-level directory of the package's sources.

The ``link`` directive is used to specify files relative to the package source
root to symbolically link into ``$PATH``. By convention (for ``build`` can
execute arbitrary code, preventing technical enforcement), LitePkg packages
never write outside of their prefix - any executables are simply symlinked into
a directory which is in the user's ``$PATH``, by default ``~/bin``. In this
way, a package can be uninstalled by simply deleting it's prefix.

The ``untar`` directive runs ``tar xf`` to decompress a context-specific
tarfile (usually one that has been downloaded previously). The first and only
parameter to this directive is the directory into which the given archive file
should be extracted, and which is treated thereafter as the source code root.

The ``require`` directive is used to signify dependencies for a package.  The
first parameter is the type of dependency, and the remaining parameters are
used to provide information about the dependency. The following dependency
types are available:

* ``command`` every following parameter is checked for existence within
  ``$PATH``.
* ``python`` every following parameter should be able to be imported in Python
  without error.
* ``perl`` every following parameter should be able to be ``require``-ed in 
  Perl without error.

If a require statement fails, the LPL script crashes.


.. _Toolchest: http://cdaniels.net/projects.html#the-toolchest
