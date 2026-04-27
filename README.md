# xapi

X API 文档和测试仓库。

这个仓库整理当前使用的 X 接口，包含：

- `docs/apis/*.md`: 每个 API 一份 Markdown 文档
- `query_ids.json`: 当前 GraphQL Query ID
- `tests/x_api_test.py`: Python 测试客户端
- `.github/workflows/check.yml`: 基础校验

## 凭据

不要把 Cookie、Authorization 写进仓库。测试脚本从环境变量读取：

```powershell
$env:X_COOKIE="你的 Cookie"
$env:X_AUTHORIZATION="Bearer ..."
```

脚本会自动从 `X_COOKIE` 里提取 `ct0` 作为 `x-csrf-token`。也可以手动传：

```powershell
$env:X_CSRF_TOKEN="ct0 value"
```

## 安装

```powershell
cd APIS/xapi
python -m pip install -r requirements.txt
```

## 测试

读取类接口：

```powershell
python tests/x_api_test.py account
python tests/x_api_test.py user --screen-name x
python tests/x_api_test.py search --query "vscode"
python tests/x_api_test.py timeline --count 5
```

写入类接口默认不会执行，必须显式传入参数：

```powershell
python tests/x_api_test.py create-tweet --text "hello from test" --execute
python tests/x_api_test.py favorite --tweet-id 123 --execute
```

## 文档索引

见 [docs/README.md](docs/README.md)。
