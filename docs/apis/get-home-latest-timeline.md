# getHomeLatestTimeline

获取 Home 最新时间线。

## 请求

- Method: `GET`
- URL: `https://x.com/i/api/graphql/{HomeLatestTimeline}/HomeLatestTimeline`
- Query ID: `HomeLatestTimeline`

## Query 参数

```json
{
  "variables": {
    "count": 20,
    "seenTweetIds": [],
    "enableRanking": false,
    "includePromotedContent": true
  },
  "features": {}
}
```

## 返回数据

```json
{
  "data": {
    "home": {
      "home_timeline_urt": {
        "instructions": []
      }
    }
  }
}
```
