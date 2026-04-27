# favoriteXTweet

点赞推文。

## 请求

- Method: `POST`
- URL: `https://x.com/i/api/graphql/{FavoriteTweet}/FavoriteTweet`
- Query ID: `FavoriteTweet`
- Referer: `https://x.com/i/status/{tweetId}`
- Header: 需要 `x-client-transaction-id`

## Body

```json
{
  "variables": {
    "tweet_id": "tweet id"
  },
  "queryId": "lI07N6Otwv1PhnEgXILM7A"
}
```

## 返回数据

```json
{
  "data": {
    "favorite_tweet": "Done"
  }
}
```

## 风险

这是写入接口。测试脚本默认 dry-run。
