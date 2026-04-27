# getXUserTweets

获取用户主页推文列表。

## 请求

- Method: `GET`
- URL: `https://x.com/i/api/graphql/{UserTweets}/UserTweets`
- Query ID: `UserTweets`

## Query 参数

```json
{
  "variables": {
    "userId": "user rest_id",
    "count": 20,
    "cursor": "optional cursor",
    "includePromotedContent": true,
    "withQuickPromoteEligibilityTweetFields": true,
    "withVoice": true,
    "withV2Timeline": true
  },
  "features": {},
  "fieldToggles": {
    "withArticlePlainText": false
  }
}
```

## 返回数据

```json
{
  "data": {
    "user": {
      "result": {
        "timeline_v2": {
          "timeline": {
            "instructions": []
          }
        }
      }
    }
  }
}
```
