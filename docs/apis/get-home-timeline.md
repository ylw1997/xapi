# getHomeTimeline

获取 Home 推荐时间线首屏。

## 请求

- Method: `GET`
- URL: `https://x.com/i/api/graphql/{HomeTimeline}/HomeTimeline`
- Query ID: `query_ids.json` 中的 `HomeTimeline`
- Referer: `https://x.com/home`

## Query 参数

```json
{
  "variables": {
    "count": 20,
    "includePromotedContent": true,
    "requestContext": "launch",
    "withCommunity": true
  },
  "features": {
    "responsive_web_graphql_timeline_navigation_enabled": true,
    "responsive_web_edit_tweet_api_enabled": true
  }
}
```

`features` 实际字段较多，以 `src/api/x.ts` 的 `HOME_TIMELINE_FEATURES` 为准。

## 返回数据

成功时主要结构：

```json
{
  "data": {
    "home": {
      "home_timeline_urt": {
        "instructions": [
          {
            "type": "TimelineAddEntries",
            "entries": []
          }
        ]
      }
    }
  }
}
```

xapi 测试脚本会输出 X 原始响应。
