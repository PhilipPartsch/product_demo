"""Password hashing for user authentication."""

import hashlib
import hmac
import os

# Parameters of scrypt (memory-hard): N=2**14, r=8, p=1 needs 16 MiB.
_N, _R, _P = 2**14, 8, 1
_SALT_BYTES = 16


# @Salted scrypt password hashing, IMPL_HASH, impl, [SPEC_HASH], false, true
def hash_password(password: str) -> str:
    """Return ``salt$hash`` (hex) of ``password`` with a fresh random salt."""
    salt = os.urandom(_SALT_BYTES)
    digest = hashlib.scrypt(password.encode(), salt=salt, n=_N, r=_R, p=_P)
    return f"{salt.hex()}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    """Check ``password`` against a value returned by :func:`hash_password`."""
    salt_hex, digest_hex = stored.split("$", 1)
    digest = hashlib.scrypt(
        password.encode(), salt=bytes.fromhex(salt_hex), n=_N, r=_R, p=_P
    )
    return hmac.compare_digest(digest.hex(), digest_hex)
