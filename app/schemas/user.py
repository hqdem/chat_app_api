from pydantic import BaseModel


class UserBase(BaseModel):
    login: str
    is_active: bool = True
    is_admin = False
    nickname: str | None = None


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    nickname: str


class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode = True


class User(UserInDBBase):
    ...


class UserInDB(UserInDBBase):
    hashed_password: str
