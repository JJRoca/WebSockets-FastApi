from fastapi import APIRouter, Depends, HTTPException
from app.core.deps import TokenDeps, SessionDeps
from app.DTO.user import UserCreate, UserPublic,UserUpdate
from app.services import user_service
from app.utils.pagination import ResponseModel,MetaData
router=APIRouter(tags=["User"])

@router.get('/users',response_model=ResponseModel[UserPublic])
def get_all_users(*, session: SessionDeps, skip:int=0 , limit: int=5):
    page= (skip//limit)+1    
    users= user_service.get_all_users(session= session, skip= skip, limit= limit)
    total_pages=(users["total"]//limit)+(1 if users["total"]%limit>0 else 0)
    #calculate the previous and next pages
    previous_page= page - 1 if page>1 else None
    next_page= page + 1 if page < total_pages else None
    
    #avoid "skip" being greater than "total"
    if skip >= users["total"]:
        raise HTTPException(status_code=400, detail="skip value is greater than total items.")
    return ResponseModel(
        data=users["users"],
        meta=MetaData(
            total=users["total"],
            current_page=page,
            per_page=limit,
            total_page=total_pages,
            previous_page=previous_page,
            next_page=next_page
        )
    )

@router.get('/user/{user_id}', response_model=UserPublic)
def get_user_by_id(*, session: SessionDeps, user_id: int):
    user = user_service.get_user_by_id(session= session, id= user_id)
    return user
@router.post('/user',response_model=UserPublic)
def create_user(*, session: SessionDeps, user:UserCreate):
    user= user_service.create_user(session=session, user= user )
    return user

@router.patch('/user/{user_id}',response_model=UserPublic)
def update_user(*, session: SessionDeps, user_id: int, user: UserUpdate):
    user = user_service.update_user(session= session, id= user_id, user=user)
    return user

@router.delete('/user/{user_id}')
def delete_user(*, session: SessionDeps, user_id:int):
    user = user_service.delete_user(session= session, id= user_id)
    return user
    
