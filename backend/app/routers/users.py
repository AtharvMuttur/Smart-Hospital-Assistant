from fastapi import APIRouter, Depends, HTTPException, Request, status
from datetime import date
from typing import Optional
from sqlalchemy.orm import Session

from ..deps import get_db
from ..models import Appointment, User
from ..schemas import AppointmentRead, UserCreate, UserRead, UserUpdate
from ..crud_factory import register_crud_routes
from ..auth import get_password_hash, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    # hash the password before storing
    hashed = get_password_hash(user.password)
    new_user = User(name=user.name, email=user.email, phone=user.phone, password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "id": new_user.id}


@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    content_type = request.headers.get("content-type", "")

    if content_type.startswith("application/x-www-form-urlencoded") or content_type.startswith("multipart/form-data"):
        form_data = await request.form()
        email = form_data.get("username") or form_data.get("email")
        password = form_data.get("password")
    else:
        payload = await request.json()
        email = payload.get("email") or payload.get("username")
        password = payload.get("password")

    if not email or not password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Email and password are required")

    existing_user = db.query(User).filter(User.email == email).first()
    if not existing_user or not verify_password(password, existing_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token({"sub": str(existing_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/appointments", response_model=list[AppointmentRead])
def get_logged_in_user_appointments(
    upcoming: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Appointment).filter(Appointment.user_id == current_user.id)

    if upcoming is True:
        query = query.filter(Appointment.appointment_date >= date.today())
    elif upcoming is False:
        query = query.filter(Appointment.appointment_date < date.today())

    return query.order_by(Appointment.appointment_date, Appointment.appointment_time).all()


# attach generic CRUD for users
register_crud_routes(router, User, UserCreate, UserUpdate, UserRead, "user")
