"""What each product costs, in euros."""

PRICES = {"Widget": 2.50, "Gadget": 10.00, "Gizmo": 7.25}


def price_of(product):
    if product not in PRICES:
        raise LookupError(f"no price for {product!r}")
    return PRICES[product]
