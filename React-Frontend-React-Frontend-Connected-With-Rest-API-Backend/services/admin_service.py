from fastapi import HTTPException

from database.mongodb import users_collection


def get_all_admins():

    return list(
        users_collection.find(
            {"user_type": "admin"},
            {"_id": 0}
        )
    )


def get_admin(admin_id: int):

    return users_collection.find_one(
        {
            "id": admin_id,
            "user_type": "admin"
        },
        {"_id": 0}
    )


def create_admin(admin):

    existing_user = users_collection.find_one(
        {"id": admin.id}
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User ID already exists"
        )

    admin_data = admin.model_dump()

    admin_data["user_type"] = "admin"

    users_collection.insert_one(
        admin_data
    )

    return admin


def update_admin(
    admin_id: int,
    updated_admin
):

    existing_admin = get_admin(admin_id)

    if not existing_admin:
        return None

    updated_data = updated_admin.model_dump()

    updated_data["user_type"] = "admin"

    return users_collection.update_one(
        {
            "id": admin_id,
            "user_type": "admin"
        },
        {
            "$set": updated_data
        }
    )


def delete_admin(admin_id: int):

    admin = get_admin(admin_id)

    if not admin:
        raise HTTPException(
            status_code=404,
            detail="Admin not found"
        )

    users_collection.delete_one(
        {
            "id": admin_id,
            "user_type": "admin"
        }
    )

    return admin