from typing import Optional, Dict
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse

from dependencies import templates, get_cart, items_list, categories_list

router = APIRouter(
    prefix="/catalog",
    tags=["catalog"],
    dependencies=[Depends(get_cart), Depends(items_list), Depends(categories_list), ],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_class=HTMLResponse)
async def catalog(
        request: Request,
        sort_by: Optional[str] = None,
        products: Dict = Depends(items_list),
        cart: Dict = Depends(get_cart)
):
    if sort_by == 'price-asc':
        queryset = {
            k: v for k, v in sorted(
                products.items(),
                key=lambda x: int(x[1]["price"])
            )}
    elif sort_by == 'price-desc':
        queryset = {
            k: v for k, v in sorted(
                products.items(),
                key=lambda x: int(x[1]["price"]),
                reverse=True)
        }
    else:
        queryset = products
    context = {
        "cart": cart,
        "request": request,
        "categories": categories_list(),
        "all_products": queryset,
    }
    return templates.TemplateResponse(
        "catalog.html",
        context=context
    )


@router.get("/sort", response_class=HTMLResponse)
async def catalog(
        request: Request,
        sort_by: Optional[str] = None,
        products: Dict = Depends(items_list)
):
    if sort_by == 'price-asc':
        queryset = {
            k: v for k, v in sorted(
                products.items(),
                key=lambda x: int(x[1]["price"])
            )}
    elif sort_by == 'price-desc':
        queryset = {
            k: v for k, v in sorted(
                products.items(),
                key=lambda x: int(x[1]["price"]),
                reverse=True
            )}
    else:
        queryset = products

    context = {
        "status": "ok",
        "request": request,
        "all_products": queryset,
    }
    return templates.TemplateResponse(
        "catalog.html",
        context=context
    )


@router.get("/{category}", response_class=HTMLResponse)
async def a_category_list(
        request: Request,
        sort_by: Optional[str] = None,
        category: Optional[str] = None,
        products: Dict = Depends(items_list),
        cart: Dict = Depends(get_cart),
        categories: Dict = Depends(categories_list)
):
    if category in [x['category'] for x in categories_list()]:
        products = {
            k: v for k, v in products.items()
            if v['category'] == category
        }
    if sort_by == 'price-asc':
        products = {
            k: v for k, v in sorted(
                products.items(), key=lambda x: int(x[1]["price"])
            )}
    elif sort_by == 'price-desc':
        products = {
            k: v for k, v in sorted(
                products.items(), key=lambda x: int(x[1]["price"]), reverse=True)}

    context = {
        "cart": cart,
        "request": request,
        "categories": categories,
        "all_products": products,
    }
    return templates.TemplateResponse(
        "catalog.html",
        context=context
    )
