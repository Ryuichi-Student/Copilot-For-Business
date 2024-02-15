import importlib
import pkgutil, os
from src.backend.visualisation.Visualisation import Visualisation

for (_module_loader, name, _ispkg) in pkgutil.iter_modules([os.path.dirname(__file__)]):
    importlib.import_module(f'.{name}', __package__)

visualisation_subclasses = {cls.getChartName():cls for cls in Visualisation.__subclasses__()}