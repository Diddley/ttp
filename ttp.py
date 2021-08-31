from app import create_app, db
from app.models import Role, User, Division, Club, Prison, Category, Cohort, Contact, Comment, Media, Kit, Funding

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return{'db': db, 'User': User, 'Division': Division, 'Club': Club, 'Prison': Prison, 'Cohort': Cohort, 'Contact': Contact, 'Comment': Comment, 'Media': Media, 'Kit': Kit, 'Funding': Funding, 'Role':Role}
