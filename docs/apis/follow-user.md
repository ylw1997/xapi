# followXUser

关注用户。

## 请求

- Method: `POST`
- URL: `https://x.com/i/api/1.1/friendships/create.json`
- Content-Type: `application/x-www-form-urlencoded`

## Form Data

```text
include_profile_interstitial_type=1
include_blocking=1
include_blocked_by=1
include_followed_by=1
include_want_retweets=1
include_mute_edge=1
include_can_dm=1
include_can_media_tag=1
include_ext_is_blue_verified=1
include_ext_verified_type=1
include_ext_profile_image_shape=1
skip_status=1
user_id=<user id>
```

## 返回数据

```json
{
  "id_str": "target user id",
  "screen_name": "screen",
  "following": true
}
```

## 风险

这是写入接口。测试脚本默认 dry-run。
