from app import db,app

class Logs(db.Model):
    __tablename__ = 'logs'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(255),nullable=True)
    domain_category = db.Column(db.String(255),nullable=True)
    key_words = db.Column(db.Text,nullable=True)
    title = db.Column(db.Text, nullable=False)
    title_decision = db.Column(db.String(255),nullable=True)
    title_score = db.Column(db.Float,nullable=True)
    content = db.Column(db.Text,nullable=True)
    content_decision = db.Column(db.String(255),nullable=True)
    content_score = db.Column(db.Float,nullable=True)
    time = db.Column(db.DateTime, nullable=True)

# with app.app_context():
#     db.create_all()