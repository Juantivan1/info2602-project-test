from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status, Request
from typing import Annotated
from fastapi import Depends, HTTPException, status
from app.models.user import User
from app.dependencies.session import SessionDep
from app.models.user import User
from app.repositories.user import UserRepository


# ✅ SAFE: returns None instead of crashing globally
async def get_current_user(request: Request, db: SessionDep) -> Optional[User]:

    token = request.cookies.get("access_token")

    if not token:
        return None  # 🔥 IMPORTANT: do NOT throw 401 here

    try:
        user_id = int(token)
    except ValueError:
        return None

    user = UserRepository.get_by_id(db, user_id)

    if not user:
        return None

    return user


# ✅ Dependency alias
AuthDep = Annotated[Optional[User], Depends(get_current_user)]


# (optional keep, but safe)
async def is_logged_in(user: AuthDep):
    return user is not None


IsUserLoggedIn = Annotated[bool, Depends(is_logged_in)]


async def is_admin(user: AuthDep):
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to access this page",
        )

    return user


AdminDep = Annotated[User, Depends(is_admin)]