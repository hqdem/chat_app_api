from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.crud.base import CRUDBase
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_user_by_login(self, db: Session, *, login: str) -> User | None:
        return db.query(User).filter(User.login == login).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        obj_in_dict = obj_in.dict()
        plain_password = obj_in_dict.pop('password')

        db_obj = User(**obj_in_dict, hashed_password=get_password_hash(plain_password))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


crud_user = CRUDUser(User)
