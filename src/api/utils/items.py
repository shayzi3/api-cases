


async def get_by_id_name(
     id: str | None = None,
     name: str | None = None,
) -> dict[str, str]:
     get_by = {"id": id} if id else {"name": name}
     
     if (id is None) and (name is None):
          return {}
     return get_by