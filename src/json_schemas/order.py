ORDER_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "string", "pattern": r"^[1-9]([0-9]{1,3})?$"},
        "price": {"type": "string", "pattern": r"^[1-9]([0-9]{1,3})?$|^[0-9]{1,4}[.]\d{1,2}?$"},
        "quantity": {"type": "string", "pattern": r"^\d{1,4}$"},
        "side": {"type": "string", "enum": ["sell", "buy"]}
    },
    "required": ["id", "price", "quantity", "side"]
}
