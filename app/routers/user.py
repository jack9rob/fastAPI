from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter
from app import models, schemas
from app.database import get_db
from .. import models, schemas, utils

router = APIRouter(
    prefix="/users",
    tags=['users']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model= schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    #hash password - user.password
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password

    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@router.get('/{id}', response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} was not found")
    
    return user