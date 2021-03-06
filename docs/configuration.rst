=============
Configuration
=============

.. contents::


Setting up configuration in your app
====================================

Configuration is handled by a ``ConfigManager``. When you instantiate the
``ConfigManager``, you pass it a list of sources that it should look at when
resolving configuration requests. The list of sources are consulted in the order
you specify.

For example::

    import os

    from everett.manager import (
        ConfigManager,
        ConfigOSEnv,
        ConfigIniEnv
    )


    config = ConfigManager([
        ConfigOSEnv,
        ConfigIniEnv([
            os.environ.get('FOO_INI'),
        ])
    ])
        

If you want to make configuration a global singleton, that's cool.

``ConfigManager`` should be thread-safe and re-entrant with the provided
sources. If you implement your own sources, then it depends on whether your
sources are safe.


Configuration sources
=====================

ConfigOSEnv
-----------

.. autoclass:: everett.manager.ConfigOSEnv
   :noindex:


ConfigIniEnv
------------

.. autoclass:: everett.manager.ConfigIniEnv
   :noindex:


ConfigDictEnv
-------------

.. autoclass:: everett.manager.ConfigDictEnv
   :noindex:


Implementing your own sources
-----------------------------

You can implement your own sources. They just need to implement the ``.get()``
method. A no-op implementation is this::

    from everett import NO_VALUE

    class NoOpEnv(object):
        def get(self, key, namespace=None):
            # The namespace is either None or a list of strings specifying
            # the namespace.
            if namespace is None:
                namespace = []

            return NO_VALUE


You might want to pull configuration from a database or Redis or something.


Extracting values
=================

Once you have a configuration manager set up with sources, you can pull
configuration values from it.

Configuration must have a key. Other than that, everything is optionally
specified.

.. automethod:: everett.manager.ConfigManager.__call__


Some examples:

``config('password')``
    The key is "password".

    The value is parsed as a string.

    There is no default value provided so if "password" isn't provided in any of
    the configuration sources, then this will raise a
    ``everett.ConfigurationError``.

    This is what you want to do to require that a configuration value exist.

``config('name', raise_rror=False)``
    The key is "name".

    The value is parsed as a string.

    There is no default value provided and raise_error is set to False, so if
    this configuration variable isn't set anywhere, the result of this will be
    ``everett.NO_VALUE``.

``config('debug', default='false', parser=bool)``
    The key is "debug".

    The value is parsed using the special Everett bool parser.

    There is a default provided, so if this configuration variable isn't set in
    the specified sources, the default will be false.

``config('username', namespace='db')``

    The key is "username".

    The namespace is "db".

    There's no default, so if there's no "username" in namespace "db"
    configuration variable set in the sources, this will raise a
    ``everett.ConfigurationError``.


Namespaces
==========

Everett has namespaces for grouping related configuration values.

For example, say you had database code that required a username, password
and port. You could do something like this::

    def open_db_connection(config):
        username = config('username', namespace='db')
        password = config('password', namespace='db')
        port = config('port', namespace='db', default=5432, parser=int)


    conn = open_db_connection(config)


These variables in the environment would be ``DB_USERNAME``, ``DB_PASSWORD``
and ``DB_PORT``.

This is helpful when you need to create two of the same thing, but using
separate configuration. Extending this example, you could pass the namespace as
an argument.

For example, say you wanted to use ``open_db_connection`` for a source
db and for a dest db::

    def open_db_connection(config, namespace):
        username = config('username', namespace=namespace)
        password = config('password', namespace=namespace)
        port = config('port', namespace=namespace, default=5432, parser=int)


    source = open_db_connection(config, 'source_db')
    dest = open_db_connection(config, 'dest_db')


Then you end up with ``SOURCE_DB_USERNAME`` and friends and
``DEST_DB_USERNAME`` and friends.


Parsers
=======

Python types are parsers: str, int, unicode (Python 2 only), float
------------------------------------------------------------------

Python types can convert strings to Python values. You can use these as
parsers:

* ``str``
* ``int``
* ``unicode`` (Python 2 only)
* ``float``


bools
-----

Everett provides a special bool parser that handles more explicit values
for "true" and "false":

* true: t, true, yes, y, 1 (and uppercase versions)
* false: f, false, no, n, 0 (and uppercase versions)

.. autofunction:: everett.manager.parse_bool
   :noindex:


classes
-------

Everett provides a ``everett.manager.parse_class`` that takes a
string specifying a module and class and returns the class.

.. autofunction:: everett.manager.parse_class
   :noindex:


ListOf
------

Everett provides a special ``everett.manager.ListOf`` parser which
parses a list of some other type. For example::

    ListOf(str)  # comma-delimited list of strings
    ListOf(int)  # comma-delimited list of ints

.. autofunction:: everett.manager.ListOf
   :noindex:


Implementing your own parsers
-----------------------------

It's easy to implement your own parser. You just need to build a callable that
takes a string and returns the Python value you want.

If the value is not parseable, then it should raise a ``ValueError``.

For example, say we wanted to implement 
