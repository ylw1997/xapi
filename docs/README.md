# X API 文档

## 通用约定

- Base URL: `https://x.com`
- GraphQL URL: `/i/api/graphql/{queryId}/{operationName}`
- 大多数接口需要登录 Cookie、Bearer Authorization、`x-csrf-token`
- `x-csrf-token` 通常等于 Cookie 中的 `ct0`
- 返回外层通常为 X 原始 JSON。TouchFish 中统一包装为：

```json
{
  "code": 0,
  "message": "error message when failed",
  "data": {}
}
```

## 当前接口

- [HomeTimeline 首屏推荐时间线](apis/get-home-timeline.md)
- [HomeTimeline 下一页](apis/get-home-timeline-next.md)
- [HomeTimeline 刷新](apis/get-home-timeline-refresh.md)
- [HomeLatestTimeline 最新时间线](apis/get-home-latest-timeline.md)
- [HomeLatestTimeline 下一页](apis/get-home-latest-timeline-next.md)
- [TweetDetail 推文详情](apis/get-tweet-detail.md)
- [SearchTimeline 搜索时间线](apis/search-timeline.md)
- [UserByScreenName 用户信息](apis/user-by-screen-name.md)
- [UserTweets 用户推文](apis/user-tweets.md)
- [Following 关注列表](apis/following.md)
- [Account verify credentials 当前账号信息](apis/account-verify-credentials.md)
- [CreateTweet 发推/回复](apis/create-tweet.md)
- [RepostTweet 引用转发](apis/repost-tweet.md)
- [FavoriteTweet 点赞](apis/favorite-tweet.md)
- [UnfavoriteTweet 取消点赞](apis/unfavorite-tweet.md)
- [Follow user 关注用户](apis/follow-user.md)
- [Unfollow user 取消关注](apis/unfollow-user.md)
- [Upload media 上传媒体](apis/upload-media.md)
- [Translate post 翻译推文](apis/translate-post.md)

## 常用请求头

```http
authorization: Bearer ...
Cookie: ...
x-csrf-token: <ct0>
x-twitter-active-user: yes
x-twitter-auth-type: OAuth2Session
x-twitter-client-language: zh-cn
User-Agent: Mozilla/5.0 ...
```

部分接口还需要当前页面生成的 `x-client-transaction-id`。Python 测试脚本支持通过 `X_CLIENT_TRANSACTION_ID` 环境变量传入；没有该值时，部分写入或搜索接口可能被 X 拒绝。
