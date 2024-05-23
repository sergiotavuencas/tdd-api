from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from pydantic import UUID4

from store.core.exceptions import NotFoundException
from store.schemas.product import ProductIn, ProductOut, ProductUpdate
from store.usecases.product import ProductUsecases

router = APIRouter(tags=["products"])


@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def post(
    body: ProductIn = Body(...), usecase: ProductUsecases = Depends()
) -> ProductOut:
    try:
        return await usecase.create(body=body)

    except NotFoundException as exec:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=exec.message
        )


@router.get(path="/{id}", status_code=status.HTTP_200_OK)
async def get(
    id: UUID4 = Path(alias="id"), usecase: ProductUsecases = Depends()
) -> ProductOut:
    try:
        return await usecase.get(id=id)

    except NotFoundException as exec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exec.message)


@router.get(path="/", status_code=status.HTTP_200_OK)
async def query(usecase: ProductUsecases = Depends()) -> List[ProductOut]:
    return await usecase.query()


@router.patch(path="/{id}", status_code=status.HTTP_200_OK)
async def patch(
    id: UUID4 = Path(alias="id"),
    body: ProductUpdate = Body(...),
    usecase: ProductUsecases = Depends(),
) -> ProductOut:
    try:
        result = await usecase.get(id=id)

        if result:
            return await usecase.update(id=id, body=body)

    except NotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sorry, but we couldn't find the product",
        )


@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id: UUID4 = Path(alias="id"),
    usecase: ProductUsecases = Depends(),
) -> None:
    try:
        return await usecase.delete(id=id)

    except NotFoundException as exec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exec.message)
