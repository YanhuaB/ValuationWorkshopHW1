# valuation/__init__.py

# Import key classes into the package namespace for easier access
from .yield_curve import YieldCurve
from .curve_bootstrapping import CurveBootstrapping

# Optionally, define a __version__ for your package
__version__ = '0.1.1'

# You could also include any necessary initial setup code here, such as configuration setup:
import logging

# Set up default logging configuration (just an example)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')