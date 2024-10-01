from fastapi import HTTPException
from app.core.deps import Session
from app.DTO.user import UserCreate,UserUpdate
from app.models.users import User
from app.utils.hashing import get_password_hash
from sqlmodel import func,select 
def get_all_users(*, session: Session, skip: int, limit: int):
    count_statement= select(func.count()).where(User.available==True).select_from(User)
    count= session.exec(count_statement).one()
    db_users= session.exec(select(User).where(User.available==True).order_by(User.full_name).offset(skip).limit(limit)).all()
    return {"users":db_users,
            "total":count
            }

def get_user_by_id(*, session: Session, id: int):
    db_user = session.get(User, id)
    if not db_user or not db_user.available:
        raise HTTPException(status_code=404, 
                            detail="User not found")
    # if not db_user.available:
    #     raise HTTPException(status_code=404, detail="Cannot delete a logically user")
    return db_user

def create_user(*, session: Session, user: UserCreate):    
    get_username(session=session, username=user.username)
    get_eamil(session=session, email=user.email)
    db_user = User.model_validate(
        user,
        update={"password":get_password_hash(user.password)})
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def delete_user(*, session: Session, id: int):
    db_user= get_user_by_id(session=session, id=id)
    db_user.available=False
    session.commit()
    return {"ok": True}

def update_user(*, session: Session, id: int, user: UserUpdate):
    db_user = get_user_by_id(session= session, id= id)
    get_username(session=session, username=user.username)
    if not db_user.available:
        raise HTTPException(status_code= 404,
                            detail="Cannot update a logically deleted user")
    user_data= user.model_dump(exclude_unset= True)
    for key, value in user_data.items():
        setattr(db_user,key,value)

    session.commit()
    session.refresh(db_user)
    return db_user    

def get_username(*, session: Session, username: str):
    db_user= session.exec(select(User).where(User.username==username)).first()
    if db_user:
        raise HTTPException(status_code=409, detail="Username already exists")
    return db_user    
def get_eamil(*, session: Session, email: str):
    db_user = session.exec(select(User).where(User.email==email)).first()
    if db_user:
        raise HTTPException(status_code=409, detail="Email already exists")
    return db_user
