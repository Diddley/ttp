

from flask import Blueprint

bp = Blueprint('main', __name__)

from app.models import Permission
from app.main import routes, errors

@bp.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
