


async def get_by_id_username(
     request_user_id: str,
     id: str | None = None,
     username: str | None = None,
) -> dict[str, str]:
     get_by = {"username": username} if username else {"id": id}
     
     if (id is None) and (username is None):
          get_by = {"id": request_user_id}
     return get_by


