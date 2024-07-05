def get_user_url(idUsuario: int) -> str:
    sql_query = (
    "SELECT "
    "usuario.foto "
    "FROM "
    "tb_usuario AS usuario "
    f"WHERE usuario.id = {idUsuario};"
)
    
    return sql_query