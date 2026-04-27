# getHomeTimelineNext

获取 Home 推荐时间线下一页。

## 请求

- Method: `POST`
- URL: `https://x.com/i/api/graphql/{HomeTimeline}/HomeTimeline`
- Query ID: `HomeTimeline`
- Content-Type: `application/json`

## Body

```json
{
  "variables": {
    "count": 20,
    "cursor": "cursor from previous response",
    "requestContext": "launch",
    "includePromotedContent": true,
    "withCommunity": true,
    "seenTweetIds": []
  },
  "features": {},
  "queryId": "3tb-_5Lf7kdCZ1cFHmsEfg"
}
```

## 返回数据

```json
{
  "data": {
    "home": {
      "home_timeline_urt": {
        "instructions": [
          {
            "type": "TimelineAddEntries",
            "entries": [
              {
                "entryId": "tweet-...",
                "content": {}
              }
            ]
          }
        ]
      }
    }
  }
}
```
