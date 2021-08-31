from app.models import Permission
from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import routes

@bp.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)