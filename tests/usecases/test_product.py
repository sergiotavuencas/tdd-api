from typing import List
from uuid import UUID

import pytest
from store.core.exceptions import NotFoundException
from store.schemas.product import ProductOut, ProductUpdateOut
from store.usecases.product import product_usecases


async def test_usecases_create_should_return_success(product_in):
    result = await product_usecases.create(body=product_in)

    assert isinstance(result, ProductOut)
    assert result.name == "Processador Ryzen 5 5600G"


async def test_usecases_get_should_return_success(product_inserted):
    result = await product_usecases.get(id=product_inserted.id)

    assert isinstance(result, ProductOut)
    assert result.name == "Processador Ryzen 5 5600G"


async def test_usecases_get_should_not_found():
    with pytest.raises(NotFoundException) as err:
        await product_usecases.get(id=UUID("d55dff79-54ff-4df6-8779-bf2f54daf6b1"))

    assert (
        err.value.message
        == "Product not found with filter: d55dff79-54ff-4df6-8779-bf2f54daf6b1"
    )


@pytest.mark.usefixtures("products_inserted")
async def test_usecases_query_should_return_success():
    result = await product_usecases.query()

    assert isinstance(result, List)
    assert len(result) > 1


async def test_usecases_update_should_return_success(product_inserted, product_up):
    product_up.price = "1.100"
    result = await product_usecases.update(id=product_inserted.id, body=product_up)

    assert isinstance(result, ProductUpdateOut)


async def test_usecases_delete_should_return_success(product_inserted):
    result = await product_usecases.delete(id=product_inserted.id)

    assert result is True


async def test_usecases_delete_should_not_found(product_inserted):
    with pytest.raises(NotFoundException) as err:
        await product_usecases.get(id=UUID("d55dff79-54ff-4df6-8779-bf2f54daf6b1"))

    assert (
        err.value.message
        == "Product not found with filter: d55dff79-54ff-4df6-8779-bf2f54daf6b1"
    )
