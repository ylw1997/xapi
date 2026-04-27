# getXSearchTimeline

搜索推文时间线。

## 请求

- Method: `GET`
- URL: `https://x.com/i/api/graphql/{SearchTimeline}/SearchTimeline`
- Query ID: `SearchTimeline`
- Referer: `https://x.com/search?q={query}&src=typed_query`
- Header: 建议带 `x-client-transaction-id`

## Query 参数

```json
{
  "variables": {
    "rawQuery": "vscode",
    "count": 20,
    "cursor": "optional cursor",
    "querySource": "typed_query",
    "product": "Top",
    "withGrokTranslatedBio": true
  },
  "features": {},
  "fieldToggles": {
    "withArticleRichContentState": true,
    "withArticlePlainText": false,
    "withGrokAnalyze": false,
    "withDisallowedReplyControls": false
  }
}
```

`product` 可选：`Top` 或 `Latest`。

## 返回数据

```json
{
  "data": {
    "search_by_raw_query": {
      "search_timeline": {
        "timeline": {
          "instructions": []
        }
      }
    }
  }
}
```
