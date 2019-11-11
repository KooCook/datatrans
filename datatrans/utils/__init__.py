from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent

from .classes import *
from .functions import *
import datatrans.utils.fooddata as fooddata
import datatrans.utils.structured_data as schema
