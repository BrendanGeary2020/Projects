from database.mongodb import admins_collection
from models.admin import Admin


def get_all_admins():

    return list(
        admins_collection.find(
            {},
            {"_id": 0}
        )
    )


def get_admin(admin_id: int):

    return admins_collection.find_one(
        {"id": admin_id},
        {"_id": 0}
    )


def create_admin(admin: Admin):

    admins_collection.insert_one(
        admin.model_dump()
    )

    return admin


def update_admin(admin_id: int, updated_admin: Admin):

    result = admins_collection.update_one(
        {"id": admin_id},
        {"$set": updated_admin.model_dump()}
    )

    return result


def delete_admin(admin_id: int):

    admin = admins_collection.find_one(
        {"id": admin_id},
        {"_id": 0}
    )

    if admin:
        admins_collection.delete_one(
            {"id": admin_id}
        )

    return admin