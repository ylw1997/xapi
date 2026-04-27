# getAccountVerifyCredentials

获取当前登录账号的基本信息。

## 请求

- Method: `GET`
- URL: `https://x.com/i/api/1.1/account/verify_credentials.json`

## Query 参数

```json
{
  "include_entities": true,
  "skip_status": true,
  "include_email": false
}
```

## 返回数据

```json
{
  "id_str": "1477631870674210819",
  "screen_name": "your_screen_name",
  "name": "your name",
  "profile_image_url_https": "https://...",
  "verified": false,
  "protected": false
}
```

字段会随账号状态变化，测试脚本优先用这个接口验证 Cookie 是否有效。
