# repostXTweet

引用转发推文。

## 请求

这是 `createXTweet` 的包装：把 `attachment_url` 设置为 `https://x.com/{screenName}/status/{tweetId}`。

- Method: `POST`
- URL: `https://x.com/i/api/graphql/{CreateTweet}/CreateTweet`

## 参数

```json
{
  "comment": "引用转发文案",
  "tweetId": "target tweet id",
  "screenName": "target user screen name, optional"
}
```

## 返回数据

返回结构同 [createXTweet](create-tweet.md)。

## 风险

这是写入接口。测试脚本默认 dry-run。
