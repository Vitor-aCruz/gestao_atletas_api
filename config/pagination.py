from fastapi import Query

def pagination_params(
    page: int = Query(1, ge=1, le=100, description="Número da pagina (inicia em 1)"),
    limit: int = Query(10, ge=1, le=100, description="Número de itens por página"),
):
    offset = (page - 1) * limit
    return {"limit": limit, "offset": offset}