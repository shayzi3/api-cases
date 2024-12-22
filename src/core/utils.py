


async def get_by_username_id(
     request_user_id: str,
     id: str | None = None,
     username: str | None = None,
) -> dict[str, str]:
     get_by = {"id": id}
     if id is None:
          get_by = {"username": username}
     
     if username is None:
          get_by = {"id": request_user_id}
     return get_by


