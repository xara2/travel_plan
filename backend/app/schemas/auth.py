from pydantic import BaseModel


class SendCodeReq(BaseModel):
    phone: str = ""
    email: str = ""


class LoginReq(BaseModel):
    phone: str = ""
    email: str = ""
    code: str = ""


class LoginResp(BaseModel):
    token: str
    user_id: int
    nickname: str
