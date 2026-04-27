# createXTweet

发送推文或回复。

## 请求

- Method: `POST`
- URL: `https://x.com/i/api/graphql/{CreateTweet}/CreateTweet`
- Query ID: `CreateTweet`
- Header: 需要 `x-client-transaction-id`

## Body

```json
{
  "variables": {
    "tweet_text": "hello",
    "reply": {
      "in_reply_to_tweet_id": "optional tweet id",
      "exclude_reply_user_ids": []
    },
    "attachment_url": "optional quote url",
    "media": {
      "media_entities": [
        {
          "media_id": "media id",
          "tagged_users": []
        }
      ],
      "possibly_sensitive": false
    },
    "semantic_annotation_ids": [],
    "disallowed_reply_options": null,
    "semantic_annotation_options": {
      "source": "Unknown"
    }
  },
  "features": {},
  "queryId": "c50A_puUoQGK_4SXseYz3A"
}
```

## 返回数据

TouchFish 返回：

```json
{
  "rest_id": "tweet id",
  "core": {},
  "legacy": {
    "full_text": "hello"
  }
}
```

如果 X 返回结构变化，则回退返回完整 `response.data`。

## 风险

这是写入接口。测试脚本默认 dry-run，必须加 `--execute` 才会真实发送。
