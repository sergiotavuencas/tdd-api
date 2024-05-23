from pydantic import ValidationError
import pytest
from store.schemas.product import ProductIn
from tests.factories import product_data


def test_schemas_validate():
    data = product_data()
    product = ProductIn.model_validate(data)

    assert product.name == "Processador Ryzen 5 5600G"


def test_schemas_return_raise():
    data = {
        "name": "Processador Ryzen 5 5600G",
        "quantity": 20,
        "price": 1.000,
    }

    with pytest.raises(ValidationError) as err:
        ProductIn.model_validate(data)

    assert err.value.errors()[0] == {
        "type": "missing",
        "loc": ("status",),
        "msg": "Field required",
        "input": {"name": "Processador Ryzen 5 5600G", "quantity": 20, "price": 1.0},
        "url": "https://errors.pydantic.dev/2.7/v/missing",
    }
