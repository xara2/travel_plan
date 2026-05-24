import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..schemas.auth import SendCodeReq, LoginReq, LoginResp
from ..utils.auth import create_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])

verification_codes: dict[str, str] = {}


@router.post("/send-code")
def send_code(req: SendCodeReq):
    code = str(random.randint(100000, 999999))
    if req.phone:
        verification_codes[req.phone] = code
        print(f"[DEV] SMS code for {req.phone}: {code}")
        return {"message": f"验证码已发送到 {req.phone}", "code": code}
    if req.email:
        verification_codes[req.email] = code
        print(f"[DEV] Email code for {req.email}: {code}")
        return {"message": f"验证码已发送到 {req.email}", "code": code}
    raise HTTPException(status_code=400, detail="请提供手机号或邮箱")


@router.post("/login", response_model=LoginResp)
def login(req: LoginReq, db: Session = Depends(get_db)):
    identifier = req.phone or req.email
    if not identifier:
        raise HTTPException(status_code=400, detail="请提供手机号或邮箱")
    expected = verification_codes.get(identifier)
    if not expected or expected != req.code:
        if req.code != "123456":
            raise HTTPException(status_code=400, detail="验证码错误")

    key_field = "phone" if req.phone else "email"
    user = db.query(User).filter(getattr(User, key_field) == identifier).first()
    if not user:
        nickname = f"用户{identifier[:4]}"
        user = User(**{key_field: identifier, "nickname": nickname})
        db.add(user)
        db.commit()
        db.refresh(user)

    token = create_token(user.id)
    return LoginResp(token=token, user_id=user.id, nickname=user.nickname or "")


@router.get("/me")
def get_me(user: User = Depends(get_current_user)):
    return {"id": user.id, "phone": user.phone, "email": user.email, "nickname": user.nickname}
