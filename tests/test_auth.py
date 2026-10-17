from product_demo.auth import hash_password, verify_password


def test_hash_is_salted_and_verifies(record_property):
    record_property("executes", "TSPEC_HASH")
    first = hash_password("s3cret")
    second = hash_password("s3cret")
    assert first != second  # fresh salt per hash
    assert verify_password("s3cret", first)
    assert not verify_password("wrong", first)
