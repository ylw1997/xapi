# getTweetDetail

获取单条推文详情和回复时间线。

## 请求

- Method: `GET`
- URL: `https://x.com/i/api/graphql/{TweetDetail}/TweetDetail`
- Query ID: `TweetDetail`
- Referer: `https://x.com/i/status/{tweetId}`

## Query 参数

```json
{
  "variables": {
    "focalTweetId": "tweet id",
    "referrer": "home",
    "with_rux_injections": false,
    "rankingMode": "Relevance",
    "includePromotedContent": true,
    "withCommunity": true,
    "withQuickPromoteEligibilityTweetFields": true,
    "withBirdwatchNotes": true,
    "withVoice": true
  },
  "features": {},
  "fieldToggles": {
    "withArticleRichContentState": true,
    "withArticlePlainText": false,
    "withArticleSummaryText": true,
    "withArticleVoiceOver": true,
    "withGrokAnalyze": false,
    "withDisallowedReplyControls": false
  }
}
```

## 返回数据

```json
{
  "data": {
    "threaded_conversation_with_injections_v2": {
      "instructions": [
        {
          "type": "TimelineAddEntries",
          "entries": []
        }
      ]
    }
  }
}
```
