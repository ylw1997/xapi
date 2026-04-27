# unfavoriteXTweet

取消点赞推文。

## 请求

- Method: `POST`
- URL: `https://x.com/i/api/graphql/{UnfavoriteTweet}/UnfavoriteTweet`
- Query ID: `UnfavoriteTweet`
- Referer: `https://x.com/i/status/{tweetId}`
- Header: 需要 `x-client-transaction-id`

## Body

```json
{
  "variables": {
    "tweet_id": "tweet id"
  },
  "queryId": "ZYKSe-w7KEslx3JhSIk5LA"
}
```

## 返回数据

```json
{
  "data": {
    "unfavorite_tweet": "Done"
  }
}
```

## 风险

这是写入接口。测试脚本默认 dry-run。
