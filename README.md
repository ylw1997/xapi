# xapi

X API 文档和测试仓库。

这个仓库整理当前使用的 X 接口，包含：

- `docs/apis/*.md`: 每个 API 一份 Markdown 文档
- `query_ids.json`: 当前 GraphQL Query ID
- `tests/x_api_test.py`: Python 测试客户端
- `.github/workflows/check.yml`: 基础校验

## 当前支持接口

- [account 当前账号信息](docs/apis/account-verify-credentials.md)
- [timeline Home 推荐时间线](docs/apis/get-home-timeline.md)
- [timeline-next Home 推荐时间线下一页](docs/apis/get-home-timeline-next.md)
- [timeline-refresh Home 推荐时间线刷新](docs/apis/get-home-timeline-refresh.md)
- [latest Home 最新时间线](docs/apis/get-home-latest-timeline.md)
- [latest-next Home 最新时间线下一页](docs/apis/get-home-latest-timeline-next.md)
- [tweet 推文详情](docs/apis/get-tweet-detail.md)
- [search 搜索时间线](docs/apis/search-timeline.md)
- [user 根据 screen name 获取用户信息](docs/apis/user-by-screen-name.md)
- [user-tweets 获取用户推文列表](docs/apis/user-tweets.md)
- [following 获取关注列表](docs/apis/following.md)
- [create-tweet 发推或回复](docs/apis/create-tweet.md)
- [repost 引用转发](docs/apis/repost-tweet.md)
- [favorite 点赞](docs/apis/favorite-tweet.md)
- [unfavorite 取消点赞](docs/apis/unfavorite-tweet.md)
- [follow 关注用户](docs/apis/follow-user.md)
- [unfollow 取消关注用户](docs/apis/unfollow-user.md)
- [translate 翻译推文](docs/apis/translate-post.md)
- [upload-media 上传媒体](docs/apis/upload-media.md)

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

## 每天自动更新 Query ID

仓库内置 GitHub Actions：`.github/workflows/update-query-ids.yml`。

它会每天自动访问 `x.com`，从前端模块中提取最新 GraphQL Query ID，并只更新 `query_ids.json` 中已经维护的接口。如果有变化，会自动创建 `chore/update-query-ids` 分支并向 `master` 提交 PR。

也可以手动运行：

```powershell
npm install
npm run update-query-ids
```

## 文档索引

见 [docs/README.md](docs/README.md)。
