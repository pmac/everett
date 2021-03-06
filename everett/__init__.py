# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Singleton indicating a non-value
NO_VALUE = object()


# Configuration error indicator
class ConfigurationError(Exception):
    pass


__author__ = 'Will Kahn-Greene'
__email__ = 'willkg@mozilla.com'

# yyyymmdd
__releasedate__ = ''
# x.y or x.y.dev
__version__ = '0.2.dev'
