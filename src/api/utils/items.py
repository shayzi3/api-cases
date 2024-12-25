


async def get_by_id_name(
     id: str | None = None,
     name: str | None = None,
) -> dict[str, str]:
     
     get_by = {"id": id}
     if id is None:
          get_by = {"name": name}
          
     if name is None:
          return {}
     return get_by