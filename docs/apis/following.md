# getXFollowing

获取某个用户的关注列表。

## 请求

- Method: `GET`
- URL: `https://x.com/i/api/graphql/{Following}/Following`
- Query ID: `Following`
- Referer: `https://x.com/i/user/{userId}/following`

## Query 参数

```json
{
  "variables": {
    "userId": "user rest_id",
    "count": 20,
    "cursor": "optional cursor",
    "includePromotedContent": false,
    "withGrokTranslatedBio": true
  },
  "features": {}
}
```

## 返回数据

X 原始结构：

```json
{
  "data": {
    "user": {
      "result": {
        "timeline": {
          "timeline": {
            "instructions": []
          }
        }
      }
    }
  }
}
```

如果业务层需要展示关注列表，可以从 `entries` 进一步解析为：

```json
{
  "users": [
    {
      "id": "123",
      "screen_name": "Name (@screen)",
      "screen_name_raw": "screen",
      "name": "Name",
      "avatar_hd": "https://...",
      "avatar_large": "https://...",
      "following": true,
      "followers_count": 1000,
      "followers_count_str": "1.0K",
      "friends_count_str": "10",
      "descText": "",
      "verified_reason": ""
    }
  ],
  "cursor": "next cursor"
}
```
