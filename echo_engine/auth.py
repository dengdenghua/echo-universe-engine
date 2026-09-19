from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
from typing import Any


class JWTError(ValueError):
    """Raised when an EchoAI account token cannot be trusted."""


def _decode_segment(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    try:
        return base64.urlsafe_b64decode(value + padding)
    except (ValueError, TypeError) as exc:
        raise JWTError("malformed token") from exc


def decode_hs256(token: str, secret: str, *, now: int | None = None) -> dict[str, Any]:
    """Verify the account service's compact HS256 JWT and return its claims."""
    parts = token.split(".")
    if len(parts) != 3 or not secret:
        raise JWTError("malformed token")
    header_part, payload_part, signature_part = parts
    try:
        header = json.loads(_decode_segment(header_part))
        claims = json.loads(_decode_segment(payload_part))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise JWTError("malformed token") from exc
    if not isinstance(header, dict) or header.get("alg") != "HS256":
        raise JWTError("unsupported token algorithm")
    if not isinstance(claims, dict):
        raise JWTError("invalid token claims")

    signing_input = f"{header_part}.{payload_part}".encode("ascii")
    expected = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    supplied = _decode_segment(signature_part)
    if not hmac.compare_digest(supplied, expected):
        raise JWTError("invalid token signature")

    subject = claims.get("sub")
    if not isinstance(subject, str) or not subject.strip():
        raise JWTError("token subject missing")
    expires_at = claims.get("exp")
    if not isinstance(expires_at, (int, float)) or expires_at <= (now or int(time.time())):
        raise JWTError("token expired")
    return claims
