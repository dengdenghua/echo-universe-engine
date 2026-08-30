from pathlib import Path
import shutil
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# 受 ECHO_AUTO_GIT_COMMIT 自动提交的 canon 资产目录（见 config.git_commit_paths）。
_DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def _data_entries() -> set[str]:
    return {p.name for p in _DATA_DIR.iterdir()} if _DATA_DIR.exists() else set()


def _is_sqlite_sidecar(name: str) -> bool:
    """WAL 模式下 SQLite 自己管理的 -wal/-shm 边车文件。

    governance.py 打开库时会设 journal_mode=WAL，未隔离 cwd 的测试因此会在真实
    data/ 里生成边车。它们是 SQLite 的临时产物而非伪造状态，且已在 .gitignore
    里排除，删掉即可，不必让守卫失败——守卫要拦的是 *_state.json/yaml 那类假数据。
    """
    return name.startswith("echo.sqlite3-")


def _clean_leaks(reference: set[str]) -> list[str]:
    """删除 reference 之后新出现在真实 data/ 的条目，返回被删名字列表。"""
    leaked = sorted(_data_entries() - reference)
    for name in leaked:
        path = _DATA_DIR / name
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
        else:
            path.unlink(missing_ok=True)
    return [name for name in leaked if not _is_sqlite_sidecar(name)]


# 会话开始时真实 data/ 的基线（即已提交的 catalog/policy 文件集合）。
_BASELINE = _data_entries()


@pytest.fixture(autouse=True)
def _guard_canon_data_not_polluted(request):
    """若某个测试把状态写进真实的项目 data/ 目录则失败（并清理）。

    bindings/economy/identities/digital_life 等模块在 root=None 时回退到
    Path.cwd()，因此忘记传 root=tmp_path 的测试会悄悄生成
    data/user_bindings.json、economy_state.json、user_identities.json、
    digital_life_state.yaml 等假状态文件，进而有被 ECHO_AUTO_GIT_COMMIT
    误提交的风险。测试必须改用 root=tmp_path / monkeypatch.chdir(tmp_path)
    / subprocess cwd=tmp_path / 设置 ECHO_JOURNAL_PATH 来隔离写入。
    """
    before = _data_entries()
    yield
    leaked = _clean_leaks(before)
    assert not leaked, (
        f"{request.node.nodeid} leaked state into real data/: {leaked}; "
        "pass root=tmp_path (or monkeypatch.chdir / subprocess cwd=tmp_path, "
        "or set ECHO_JOURNAL_PATH)"
    )


@pytest.fixture
def api_client(tmp_path):
    """注入 root=tmp_path 的 FastAPI TestClient。

    通过 app.dependency_overrides 覆盖 get_root，让所有端点把状态读写到 tmp_path，
    而不是依赖 monkeypatch.chdir + Path.cwd()。后者与 Starlette TestClient 的工作线程
    存在竞态：写盘发生时工作目录可能已被还原成项目根，从而把假状态泄漏进真实 data/。
    """
    from fastapi.testclient import TestClient

    from echo_engine.api import app, get_root

    app.dependency_overrides[get_root] = lambda: tmp_path
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.pop(get_root, None)


def pytest_sessionfinish(session, exitstatus):
    """兜底：捕获落在任何单个测试窗口之外的泄漏。

    曾观察到极偶发的泄漏能绕过逐用例守卫（疑似 TestClient 工作线程在用例
    结束后仍执行 get_universe_feed_for_user 的写盘）。这里在会话收尾时再核对
    一次真实 data/，清理残留并把退出码标红，确保「跑完 pytest 工作树干净」。
    """
    leaked = _clean_leaks(_BASELINE)
    if leaked and session.exitstatus == 0:
        session.exitstatus = 1
        reporter = session.config.pluginmanager.get_plugin("terminalreporter")
        if reporter is not None:
            reporter.write_line(
                f"ERROR: tests leaked state into real data/ (cleaned): {leaked}; "
                "a write escaped tmp_path isolation",
                red=True,
            )
