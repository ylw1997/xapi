# getHomeLatestTimelineNext

获取 Home 最新时间线下一页。

## 请求

- Method: `POST`
- URL: `https://x.com/i/api/graphql/{HomeLatestTimeline}/HomeLatestTimeline`
- Query ID: `HomeLatestTimeline`

## Body

```json
{
  "variables": {
    "count": 20,
    "cursor": "cursor from previous response",
    "seenTweetIds": [],
    "enableRanking": false,
    "includePromotedContent": true
  },
  "features": {},
  "queryId": "eObmT5Nuapp04u8bYWf49Q"
}
```

## 返回数据

返回结构同 [getHomeLatestTimeline](get-home-latest-timeline.md)。
