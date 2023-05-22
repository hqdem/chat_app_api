from typing import List

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.schemas.user import UserCreate, UserUpdate, UserBase
from app.models.user import User


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_user_by_login(self, db: Session, *, login: str) -> User | None:
        return db.query(self.model).filter(User.login == login).first()

    def get_users_by_logins(self, db: Session, users: List[UserBase]) -> List[User]:
        logins = {user.login for user in users}
        db_users = db.query(self.model).filter(User.login.in_(logins)).all()
        return db_users

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        obj_in_dict = obj_in.dict()
        plain_password = obj_in_dict.pop('password')

        db_obj = User(**obj_in_dict, hashed_password=get_password_hash(plain_password))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(self, db: Session, *, login: str, password: str) -> User | None:
        user = self.get_user_by_login(db, login=login)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user


crud_user = CRUDUser(User)
