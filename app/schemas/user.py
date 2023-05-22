from pydantic import BaseModel


class UserBase(BaseModel):
    login: str


class UserCreate(UserBase):
    nickname: str | None = None
    password: str


class UserUpdate(UserBase):
    nickname: str


class UserInDBBase(UserBase):
    id: int
    is_active: bool = True
    is_admin = False

    class Config:
        orm_mode = True


class User(UserInDBBase):
    ...


class UserInDB(UserInDBBase):
    hashed_password: str


class UserCredentials(BaseModel):
    login: str
    password: str
