from fastapi import APIRouter, HTTPException

from models.admin import Admin

from services.admin_service import (
    get_all_admins,
    get_admin,
    create_admin,
    update_admin,
    delete_admin
)


router = APIRouter(
    prefix="/admins",
    tags=["Admins"]
)


# GET - Get all admins
@router.get("/")
def get_admins():

    return get_all_admins()


# GET - Get one admin
@router.get("/{admin_id}")
def get_one_admin(admin_id: int):

    admin = get_admin(admin_id)

    if not admin:
        raise HTTPException(
            status_code=404,
            detail="Admin not found"
        )

    return admin


# POST - Create admin
@router.post("/", status_code=201)
def create_new_admin(admin: Admin):

    existing_admin = get_admin(admin.id)

    if existing_admin:
        raise HTTPException(
            status_code=400,
            detail="Admin ID already exists"
        )

    return create_admin(admin)


# PUT - Update admin
@router.put("/{admin_id}")
def update_existing_admin(
    admin_id: int,
    updated_admin: Admin
):

    result = update_admin(
        admin_id,
        updated_admin
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Admin not found"
        )

    return updated_admin

# DELETE - Delete admin
@router.delete("/{admin_id}")
def delete_existing_admin(admin_id: int):

    admin = delete_admin(admin_id)

    if not admin:
        raise HTTPException(
            status_code=404,
            detail="Admin not found"
        )

    return admin