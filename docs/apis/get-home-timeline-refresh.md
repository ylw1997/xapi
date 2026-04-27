# getHomeTimelineRefresh

刷新 Home 推荐时间线。

这是 `getHomeTimelineNext` 的包装调用，不传 `cursor`，只传 `seenTweetIds`。

## 请求

- Method: `POST`
- URL: `https://x.com/i/api/graphql/{HomeTimeline}/HomeTimeline`

## Body

```json
{
  "variables": {
    "count": 20,
    "requestContext": "launch",
    "includePromotedContent": true,
    "withCommunity": true,
    "seenTweetIds": ["tweet_id_1", "tweet_id_2"]
  },
  "features": {},
  "queryId": "3tb-_5Lf7kdCZ1cFHmsEfg"
}
```

## 返回数据

返回结构同 [getHomeTimelineNext](get-home-timeline-next.md)。
