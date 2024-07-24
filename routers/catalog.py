from typing import Optional, Dict
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from dependencies import get_cart, items_list, categories_list, get_pagination_params, templates

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
        category: Optional[str] = None,
        products: Dict = Depends(items_list),
        cart: Dict = Depends(get_cart),
        pagination: dict = Depends(get_pagination_params)
):
    if category in [x['slug'] for x in categories_list()]:
        category = [x['category'] for x in categories_list() if x['slug'] == category][0]
        products = [
            v for k, v in products.items()
            if v['category'] == category
        ]
    else:
        products = [v for k, v in products.items()]
    if sort_by in ['price-asc', 'price-desc']:
        products = [
            v for v in sorted(
                products,
                key=lambda x: int(x[1]["price"]),
                reverse=True if sort_by == 'price-desc' else False
            )]

    limit = pagination["limit"]
    offset = pagination["offset"]

    # total_pages = len(queryset) // int(limit)
    # prod_len = len(queryset)
    start = (limit - 1) * offset
    end = start + limit
    context = {
        "cart": cart,
        "request": request,
        "categories": categories_list(),
        "all_products": products[start:end],
        "per_page": limit,
        "current_page": offset,
    }
    # context = {
    #     "cart": cart,
    #     "request": request,
    #     "categories": categories_list(),
    #     "all_products": queryset[start:end],
    #     "prod_len": total_pages,
    #     "per_page": limit,
    #     "current_page": offset,
    #     "pagination": {}
    # }
    # context['pagination']['first'] = f'/catalog/?offset=1&limit={limit}'
    # context['pagination']['last'] = f'/catalog/?offset={total_pages}&limit={limit}'
    # if end >= prod_len:
    #     context['pagination']['next'] = None
    #     if offset > 1:
    #         context['pagination']['previous'] = f'/catalog/?offset={offset - 1}&limit={limit}'
    #     else:
    #         context['pagination']['previous'] = None
    # else:
    #     if offset > 1:
    #         context['pagination']['previous'] = f'/catalog/?offset={offset - 1}&limit={limit}'
    #     else:
    #         context['pagination']['previous'] = None
    #     context['pagination']['next'] = f'/catalog/?offset={offset + 1}&limit={limit}'

    return templates.TemplateResponse(
        "catalog.html",
        context=context
    )


@router.get("/load/more", response_class=HTMLResponse)
async def catalog_more(
        request: Request,
        sort_by: Optional[str] = None,
        category: Optional[str] = None,
        products: Dict = Depends(items_list),
        cart: Dict = Depends(get_cart),
        limit: Optional[int] = None,
        offset: Optional[int] = None
):
    if category in [x['slug'] for x in categories_list()]:
        category = [x['category'] for x in categories_list() if x['slug'] == category][0]
        products = [
            v for k, v in products.items()
            if v['category'] == category
        ]
    else:
        products = [v for k, v in products.items()]
    start = (int(offset) - 1) * int(limit)
    end = start + int(limit)
    context = {
        "cart": cart,
        "request": request,
        "categories": categories_list(),
        "all_products": products[start:end],
        "nothing": "yes" if len(products[start:end]) > 0 else "no"
    }

    return templates.TemplateResponse(
        "catalog-more.html",
        context=context
    )


@router.get("/{item_id}", response_class=HTMLResponse)
async def item(
        item_id: str,
        request: Request,
        cart: Dict = Depends(get_cart),
        products: Dict = Depends(items_list),
        categories: Dict = Depends(categories_list)
):
    default = list(products.get(item_id)['colors'].values())[0]
    context = {
        "request": request,
        "cart": cart,
        "product": products.get(item_id),
        "categories": categories,
        "all_products": products,
        "default": default
    }
    return templates.TemplateResponse(
        "item.html",
        context=context
    )


@router.get("/sort", response_class=HTMLResponse)
async def catalog(
        request: Request,
        sort_by: Optional[str] = None,
        products: Dict = Depends(items_list),
        template: str = "catalog.html"
):
    if sort_by in ['price-asc', 'price-desc']:
        products = [{k: v} for k, v in sorted(
            products.items(),
            key=lambda x: int(x[1]["price"]),
            reverse=True if sort_by == 'price-desc' else False
        )]
    context = {
        "status": "ok",
        "request": request,
        "all_products": products,
    }
    return templates.TemplateResponse(
        name=template,
        context=context
    )


@router.get("/category/{category}", response_class=HTMLResponse)
async def one_category_list(
        request: Request,
        sort_by: Optional[str] = None,
        category: Optional[str] = None,
        products: Dict = Depends(items_list),
        cart: Dict = Depends(get_cart),
        categories: Dict = Depends(categories_list),
        pagination: dict = Depends(get_pagination_params)
):
    if category in [x['category'] for x in categories_list()]:
        products = [
            v for k, v in products.items()
            if v['category'] == category
        ]

    if sort_by in ['price-asc', 'price-desc']:
        products = [
            v for k, v in sorted(
                products.items(),
                key=lambda x: int(x[1]["price"]),
                reverse=True if sort_by == 'price-desc' else False
            )]
    limit = pagination["limit"]
    offset = pagination["offset"]
    total_pages = len(products) // int(limit)

    start = (offset - 1) * limit
    end = start + limit
    print(products)

    context = {
        "cart": cart,
        "request": request,
        "categories": categories_list(),
        "all_products": products,
        "prod_len": total_pages,
        "per_page": limit,
        "current_page": offset,
    }

    return templates.TemplateResponse(
        "catalog.html",
        context=context
    )
