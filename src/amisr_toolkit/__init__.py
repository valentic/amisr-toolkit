from .metadata import __version__

# Order is important to avoid circular import

from .aeustatus import * 
from .array_xml import parse_array_status_xml
