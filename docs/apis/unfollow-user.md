# unfollowXUser

取消关注用户。

## 请求

- Method: `POST`
- URL: `https://x.com/i/api/1.1/friendships/destroy.json`
- Content-Type: `application/x-www-form-urlencoded`

## Form Data

同 [followXUser](follow-user.md)，核心字段是 `user_id`。

## 返回数据

```json
{
  "id_str": "target user id",
  "screen_name": "screen",
  "following": false
}
```

## 风险

这是写入接口。测试脚本默认 dry-run。
