from fastapi import HTTPException


def check_permissions(user, required_permissions):
    if not set(required_permissions).issubset(set(user.permissions)):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
