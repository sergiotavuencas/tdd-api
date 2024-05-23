from typing import List

import pytest
from tests.factories import product_data, products_data
from fastapi import status


async def test_controller_create_should_return_success(client, products_url):
    response = await client.post(products_url, json=product_data())

    content = response.json()
    del content["id"]
    del content["created_at"]
    del content["updated_at"]

    assert response.status_code == status.HTTP_201_CREATED
    assert content == {
        "name": "Processador Ryzen 5 5600G",
        "quantity": 20,
        "price": "1.000",
        "status": True,
    }


async def test_controller_create_many_with_price_filter_should_return_success(
    client, products_url
):
    products = [
        product
        for product in products_data()
        if product.get("price") >= "1.000" and product.get("price") < "1.700"
    ]

    responses = []

    for product in products:
        responses.append(await client.post(products_url, json=product))

    for response in responses:
        content = response.json()
        del content["id"]
        del content["created_at"]
        del content["updated_at"]

        assert response.status_code == status.HTTP_201_CREATED


async def test_controller_create_should_return_unprocessable_entity(
    client, products_url
):
    data = {
        "name": "Processador Ryzen 5 5600G",
        "quantity": 20,
        "price": 1.000,
    }
    response = await client.post(products_url, json=data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_controller_get_should_return_success(
    client, products_url, product_inserted
):
    response = await client.get(f"{products_url}{product_inserted.id}")

    content = response.json()
    del content["created_at"]
    del content["updated_at"]

    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "id": str(product_inserted.id),
        "name": "Processador Ryzen 5 5600G",
        "quantity": 20,
        "price": "1.000",
        "status": True,
    }


async def test_controller_get_should_return_not_found(client, products_url):
    response = await client.get(f"{products_url}d55dff79-54ff-4df6-8779-bf2f54daf6b1")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Product not found with filter: d55dff79-54ff-4df6-8779-bf2f54daf6b1"
    }


@pytest.mark.usefixtures("products_inserted")
async def test_controller_query_should_return_success(client, products_url):
    response = await client.get(products_url)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), List)
    assert len(response.json()) > 1


async def test_controller_patch_should_return_success(
    client, products_url, product_inserted
):
    response = await client.patch(
        f"{products_url}{product_inserted.id}", json={"price": "1.100"}
    )

    content = response.json()
    del content["created_at"]
    del content["updated_at"]

    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "id": str(product_inserted.id),
        "name": "Processador Ryzen 5 5600G",
        "quantity": 20,
        "price": "1.100",
        "status": True,
    }


async def test_controller_patch_should_return_not_found(client, products_url):
    response = await client.patch(
        f"{products_url}d55dff79-54ff-4df6-8779-bf2f54daf6b1", json={"price": "1.100"}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.content == b'{"detail":"Sorry, but we couldn\'t find the product"}'


async def test_controller_delete_should_return_no_content(
    client, products_url, product_inserted
):
    response = await client.delete(f"{products_url}{product_inserted.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_controller_delete_should_return_not_found(client, products_url):
    response = await client.get(f"{products_url}d55dff79-54ff-4df6-8779-bf2f54daf6b1")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Product not found with filter: d55dff79-54ff-4df6-8779-bf2f54daf6b1"
    }
