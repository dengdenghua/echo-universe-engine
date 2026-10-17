import base64
import hashlib
import hmac
import json
import time

from fastapi.testclient import TestClient

from echo_engine.api import app
from echo_engine.config import get_settings


def _token(
    subject: str,
    secret: str = "test-user-secret",
    extra_claims: dict[str, object] | None = None,
) -> str:
    def encode(value: dict[str, object]) -> str:
        raw = json.dumps(value, separators=(",", ":")).encode("utf-8")
        return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")

    header = encode({"alg": "HS256", "typ": "JWT"})
    payload = encode(
        {
            "sub": subject,
            "iat": int(time.time()),
            "exp": int(time.time()) + 3600,
            **(extra_claims or {}),
        }
    )
    signing_input = f"{header}.{payload}".encode("ascii")
    signature = base64.urlsafe_b64encode(
        hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    ).rstrip(b"=").decode("ascii")
    return f"{header}.{payload}.{signature}"


def test_production_guard_keeps_catalog_public_and_protects_state(monkeypatch):
    monkeypatch.setenv("ECHO_ADMIN_API_KEY", "test-admin-key")
    get_settings.cache_clear()
    try:
        client = TestClient(app)
        assert client.get("/").status_code == 200
        assert client.get("/home/").status_code == 200
        assert client.get("/home/styles.css").status_code == 200
        assert client.get("/universe/").status_code == 200
        assert client.get("/universe/styles.css").status_code == 200
        assert client.get("/universe/novel/").status_code == 200
        assert client.get("/universe/novel/stranger-memory/").status_code == 200
        assert client.get("/universe/novel/content/stranger-memory.zh.md").status_code == 200
        assert client.get("/review/").status_code == 200
        assert client.get("/review/app.js").status_code == 200
        for illustration_name in (
            "illustration-white-harbor-agnes-v1.png",
            "illustration-l7-collapse-agnes-v1.png",
            "illustration-stranger-hands-agnes-v1.png",
        ):
            illustration = client.get(f"/universe/novel/assets/{illustration_name}")
            assert illustration.status_code == 200
            assert illustration.headers["content-type"] == "image/png"
        assert client.get("/universe", follow_redirects=False).status_code in {307, 308}
        assert client.get("/console/").status_code == 401
        assert client.get("/console/styles.css").status_code == 401
        assert client.get("/api/health").status_code == 200
        assert client.get("/api/canon/characters").status_code == 200
        assert client.get("/api/journal/events").status_code == 200
        assert client.get("/api/bindings").status_code == 401
        assert client.post(
            "/api/economy/wallet/grant",
            json={"user_id": "guard-test", "amount": 1},
        ).status_code == 401
        assert client.get(
            "/api/bindings",
            headers={"Authorization": "Bearer test-admin-key"},
        ).status_code == 200
        assert client.get(
            "/console/",
            headers={"Authorization": "Bearer test-admin-key"},
        ).status_code == 200
    finally:
        get_settings.cache_clear()


_BROWSER = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}


def test_unknown_root_pages_get_the_designed_404_and_every_real_route_keeps_its_guard(monkeypatch):
    # Production nginx proxies every root-level path it does not serve to the app. A browser opening
    # one that has no route gets homepage/404.html; nothing with a route behind it changes.
    monkeypatch.setenv("ECHO_ADMIN_API_KEY", "test-admin-key")
    get_settings.cache_clear()
    try:
        client = TestClient(app)
        for path in ("/does-not-exist", "/deep/unknown/path/", "/index.html", "/docs/nope", "/wp-login.php"):
            for method in (client.get, client.head):
                response = method(path, headers=_BROWSER)
                assert response.status_code == 404, (method, path)
                assert response.headers["content-type"].startswith("text/html"), path
                assert response.headers["cache-control"] == "no-cache", path
                assert "default-src 'none'" in response.headers["content-security-policy"], path
            page = client.get(path, headers=_BROWSER).text
            assert "<title>ECHO · 404" in page and "NO ECHO AT THIS ADDRESS" in page, path

        # Machine requests to an unknown path, and every /api path, keep the guard's answer.
        unknown_json = client.get("/does-not-exist")
        assert unknown_json.status_code == 401
        assert unknown_json.json() == {"detail": "ECHO Universe authorization required"}
        assert client.get("/does-not-exist", headers={"Accept": "application/json"}).status_code == 401
        assert client.post("/does-not-exist", headers=_BROWSER).status_code == 401
        for path in ("/api", "/api/x", "/api/does/not/exist"):
            response = client.get(path, headers=_BROWSER)
            assert response.status_code == 401, path
            assert response.headers["content-type"] == "application/json", path

        # Protected routes and mounts stay protected for browsers too.
        for path in ("/console", "/console/", "/console/styles.css", "/console/nope", "/outputs/x", "/assets/x"):
            response = client.get(path, headers=_BROWSER, follow_redirects=False)
            assert response.status_code == 401, path
            assert response.headers["content-type"] == "application/json", path
        assert client.get("/api/bindings", headers=_BROWSER).status_code == 401
        assert client.post("/api/economy/wallet/grant", headers=_BROWSER, json={"user_id": "x", "amount": 1}).status_code == 401
        assert client.get("/console/", headers={**_BROWSER, "Authorization": "Bearer test-admin-key"}).status_code == 200

        # Public routes are unchanged; the bare site folders only redirect to their slash form.
        assert client.get("/", headers=_BROWSER).status_code == 200
        assert client.get("/docs", headers=_BROWSER).status_code == 200
        assert client.get("/openapi.json", headers=_BROWSER).status_code == 200
        assert client.get("/api/health", headers=_BROWSER).status_code == 200
        for folder in ("home", "universe", "developers", "review"):
            response = client.get(f"/{folder}", headers=_BROWSER, follow_redirects=False)
            assert response.status_code in {307, 308}, folder
            assert response.headers["location"].endswith(f"/{folder}/"), folder
            assert client.get(f"/{folder}/", headers=_BROWSER).status_code == 200, folder
    finally:
        get_settings.cache_clear()


def test_unknown_root_pages_get_the_404_page_without_an_admin_key_too(monkeypatch):
    monkeypatch.delenv("ECHO_ADMIN_API_KEY", raising=False)
    monkeypatch.delenv("ECHO_ADMIN_API_KEY_FILE", raising=False)
    monkeypatch.setenv("ECHO_ENVIRONMENT", "production")
    get_settings.cache_clear()
    try:
        client = TestClient(app)
        assert client.get("/does-not-exist", headers=_BROWSER).status_code == 404
        # An unconfigured production server still refuses everything else.
        assert client.get("/does-not-exist").status_code == 503
        assert client.get("/api/x", headers=_BROWSER).status_code == 503
        assert client.get("/console/", headers=_BROWSER).status_code == 503
    finally:
        get_settings.cache_clear()


def test_user_jwt_is_self_scoped_and_cannot_call_admin_routes(monkeypatch):
    monkeypatch.setenv("ECHO_ADMIN_API_KEY", "test-admin-key")
    monkeypatch.setenv("ECHO_USER_JWT_SECRET", "test-user-secret")
    get_settings.cache_clear()
    try:
        client = TestClient(app)
        headers = {"Authorization": f"Bearer {_token('user-a')}"}

        # The missing binding proves the request passed authentication and ownership checks.
        assert client.get("/api/bindings/user-a", headers=headers).status_code == 404
        assert client.get("/api/bindings/user-b", headers=headers).status_code == 403
        assert client.get("/api/bindings", headers=headers).status_code == 403
        assert client.get("/api/canon/governance/candidates", headers=headers).status_code == 403
        assert client.post(
            "/api/economy/wallet/grant",
            headers=headers,
            json={"user_id": "user-a", "amount": 100},
        ).status_code == 403
    finally:
        get_settings.cache_clear()


def test_governance_review_requires_an_explicit_reviewer_role_and_seat(monkeypatch, tmp_path):
    monkeypatch.setenv("ECHO_ADMIN_API_KEY", "test-admin-key")
    monkeypatch.setenv("ECHO_USER_JWT_SECRET", "test-user-secret")
    monkeypatch.setenv("ECHO_DATABASE_PATH", str(tmp_path / "echo.sqlite3"))
    get_settings.cache_clear()
    try:
        client = TestClient(app)
        route = "/api/canon/governance/candidates/stranger-memory/committee-votes"
        body = {
            "reviewer": "core_author",
            "decision": "approve",
            "expected_revision_sha256": "0" * 64,
        }
        ordinary_user = client.post(
            route,
            headers={"Authorization": f"Bearer {_token('core_author')}"},
            json=body,
        )
        assert ordinary_user.status_code == 403
        assert "reviewer claim" in ordinary_user.json()["detail"]

        reviewer_with_wrong_seat = client.post(
            route,
            headers={
                "Authorization": f"Bearer {_token('account-123', extra_claims={'roles': ['canon_reviewer'], 'reviewer_id': 'world_brain'})}"
            },
            json=body,
        )
        assert reviewer_with_wrong_seat.status_code == 403
        assert "must match" in reviewer_with_wrong_seat.json()["detail"]

        reviewer_headers = {
            "Authorization": f"Bearer {_token('account-123', extra_claims={'roles': ['canon_reviewer'], 'reviewer_id': 'core_author'})}"
        }
        reviewer_queue = client.get(
            "/api/canon/governance/candidates",
            headers=reviewer_headers,
        )
        assert reviewer_queue.status_code == 200
        assert reviewer_queue.json()[0]["committee"]["members"]
    finally:
        get_settings.cache_clear()
