# translateXPost

调用 X/Grok 翻译推文。

## 请求

- Method: `POST`
- URL: `https://api.x.com/2/grok/translation.json`
- Content-Type: `text/plain;charset=UTF-8`
- Header: 需要 `x-client-transaction-id`

## Body

```json
{
  "content_type": "POST",
  "id": "tweet id",
  "dst_lang": "zh"
}
```

## 返回数据

X 可能直接返回 JSON，也可能返回 base64 编码字符串。TouchFish 处理后返回：

```json
{
  "result": {
    "text": "翻译后的文本"
  }
}
```

TouchFish 最终取 `result.text`。
