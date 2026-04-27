# getXUserInfo

根据用户名获取用户信息。

## 请求

- Method: `GET`
- URL: `https://x.com/i/api/graphql/{UserByScreenName}/UserByScreenName`
- Query ID: `UserByScreenName`
- Referer: `https://x.com/{screenName}`

## Query 参数

```json
{
  "variables": {
    "screen_name": "x",
    "withSafetyModeUserFields": true
  },
  "features": {},
  "fieldToggles": {
    "withAuxiliaryUserLabels": false
  }
}
```

## 返回数据

```json
{
  "data": {
    "user": {
      "result": {
        "rest_id": "783214",
        "core": {
          "name": "X",
          "screen_name": "X"
        },
        "legacy": {
          "description": "",
          "followers_count": 0,
          "friends_count": 0
        }
      }
    }
  }
}
```
