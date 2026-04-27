# uploadXMedia

上传图片媒体，供发推使用。

## 请求流程

Base URL: `https://upload.x.com/i/media/upload.json`

### 1. INIT

- Method: `POST`
- URL:

```text
?command=INIT&total_bytes={size}&media_type={mime}&media_category=tweet_image
```

返回：

```json
{
  "media_id_string": "media id"
}
```

### 2. APPEND

- Method: `POST`
- URL:

```text
?command=APPEND&media_id={media_id}&segment_index=0
```

Body: `multipart/form-data`，字段名 `media`。

### 3. FINALIZE

- Method: `POST`
- URL:

```text
?command=FINALIZE&media_id={media_id}&original_md5={file_md5}
```

返回：

```json
{
  "media_id_string": "media id"
}
```

## 返回数据

```json
{
  "media_id_string": "media id"
}
```

## 风险

这是上传接口。测试脚本必须显式传 `--execute`。
