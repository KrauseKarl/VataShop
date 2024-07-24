from typing import Dict
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse

from dependencies import get_cart, items_list, categories_list, get_favorite, templates

router = APIRouter(
    prefix="/favorite",
    tags=["favorite"],
    dependencies=[Depends(get_cart), Depends(items_list), Depends(categories_list), ],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_class=HTMLResponse)
async def list_favorite(
        request: Request,
        cart: Dict = Depends(get_cart),
        favorites: Dict = Depends(get_favorite)
):
    response = templates.TemplateResponse(
        "favorite.html",
        context={
            "request": request,
            "products": favorites,
            "cart": cart
        }
    )
    return response


@router.delete("/del", response_class=JSONResponse)
async def delete_favorite(request: Request):
    del request.session['favorite']
    return {'status': 204, "cart": get_cart(request)}
