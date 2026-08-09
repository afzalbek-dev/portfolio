from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.models import AdminUser

def get_db_session(db: Session = Depends(get_db)):
    return db
