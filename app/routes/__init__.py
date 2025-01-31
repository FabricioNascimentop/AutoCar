from flask import Blueprint

routes = Blueprint('routes', __name__)

from .main import *
from .auth import *
from .cars import *
from .images import *

