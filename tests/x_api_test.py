import argparse
import base64
import hashlib
import json
import mimetypes
import os
import re
import sys
from urllib.parse import quote
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
QUERY_IDS = json.loads((ROOT / "query_ids.json").read_text(encoding="utf-8"))

X_BASE_URL = "https://x.com"
API_BASE_URL = "https://api.x.com"
UPLOAD_BASE_URL = "https://upload.x.com"


HOME_TIMELINE_FEATURES = {
    "rweb_video_screen_enabled": False,
    "profile_label_improvements_pcf_label_in_post_enabled": True,
    "responsive_web_profile_redirect_enabled": False,
    "rweb_tipjar_consumption_enabled": False,
    "verified_phone_label_enabled": False,
    "creator_subscriptions_tweet_preview_api_enabled": True,
    "responsive_web_graphql_timeline_navigation_enabled": True,
    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
    "premium_content_api_read_enabled": False,
    "communities_web_enable_tweet_community_results_fetch": True,
    "c9s_tweet_anatomy_moderator_badge_enabled": True,
    "responsive_web_grok_analyze_button_fetch_trends_enabled": False,
    "responsive_web_grok_analyze_post_followups_enabled": True,
    "responsive_web_jetfuel_frame": True,
    "responsive_web_grok_share_attachment_enabled": True,
    "responsive_web_grok_annotations_enabled": True,
    "articles_preview_enabled": True,
    "responsive_web_edit_tweet_api_enabled": True,
    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
    "view_counts_everywhere_api_enabled": True,
    "longform_notetweets_consumption_enabled": True,
    "responsive_web_twitter_article_tweet_consumption_enabled": True,
    "content_disclosure_indicator_enabled": True,
    "content_disclosure_ai_generated_indicator_enabled": True,
    "responsive_web_grok_show_grok_translated_post": True,
    "responsive_web_grok_analysis_button_from_backend": True,
    "post_ctas_fetch_enabled": False,
    "freedom_of_speech_not_reach_fetch_enabled": True,
    "standardized_nudges_misinfo": True,
    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
    "longform_notetweets_rich_text_read_enabled": True,
    "longform_notetweets_inline_media_enabled": False,
    "responsive_web_grok_image_annotation_enabled": True,
    "responsive_web_grok_imagine_annotation_enabled": True,
    "responsive_web_grok_community_note_auto_translation_is_enabled": True,
    "responsive_web_enhance_cards_enabled": False,
}

SEARCH_TIMELINE_FEATURES = {
    **HOME_TIMELINE_FEATURES,
    "rweb_cashtags_enabled": False,
}

CREATE_TWEET_FEATURES = {
    **HOME_TIMELINE_FEATURES,
    "rweb_cashtags_enabled": False,
}

USER_PROFILE_FEATURES = {
    "hidden_profile_likes_enabled": True,
    "hidden_profile_subscriptions_enabled": True,
    "rweb_tipjar_consumption_enabled": True,
    "responsive_web_graphql_exclude_directive_enabled": True,
    "verified_phone_label_enabled": False,
    "subscriptions_verification_info_is_identity_verified_enabled": True,
    "subscriptions_verification_info_verified_since_enabled": True,
    "highlights_tweets_tab_ui_enabled": True,
    "responsive_web_twitter_article_notes_tab_enabled": True,
    "creator_subscriptions_tweet_preview_api_enabled": True,
    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
    "responsive_web_graphql_timeline_navigation_enabled": True,
}

TWEET_DETAIL_FIELD_TOGGLES = {
    "withArticleRichContentState": True,
    "withArticlePlainText": False,
    "withArticleSummaryText": True,
    "withArticleVoiceOver": True,
    "withGrokAnalyze": False,
    "withDisallowedReplyControls": False,
}

SEARCH_TIMELINE_FIELD_TOGGLES = {
    "withArticleRichContentState": True,
    "withArticlePlainText": False,
    "withGrokAnalyze": False,
    "withDisallowedReplyControls": False,
}

USER_PROFILE_FIELD_TOGGLES = {
    "withAuxiliaryUserLabels": False,
}

USER_TWEETS_FIELD_TOGGLES = {
    "withArticlePlainText": False,
}


def dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def extract_ct0(cookie: str) -> str | None:
    match = re.search(r"(?:^|;\s*)ct0=([^;]+)", cookie)
    return match.group(1) if match else None


class XApiClient:
    def __init__(self) -> None:
        self.cookie = os.getenv("X_COOKIE", "")
        self.authorization = os.getenv("X_AUTHORIZATION", "")
        self.csrf_token = os.getenv("X_CSRF_TOKEN") or extract_ct0(self.cookie) or ""
        self.transaction_id = os.getenv("X_CLIENT_TRANSACTION_ID", "")

        if not self.cookie or not self.authorization or not self.csrf_token:
            raise SystemExit(
                "Missing credentials. Set X_COOKIE and X_AUTHORIZATION. "
                "X_CSRF_TOKEN is optional when ct0 exists in X_COOKIE."
            )

        import requests

        self.session = requests.Session()
        self.session.timeout = 30

    def headers(self, referer: str = "https://x.com/home", extra: dict[str, str] | None = None) -> dict[str, str]:
        headers = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "authorization": self.authorization,
            "Cookie": self.cookie,
            "content-type": "application/json",
            "Referer": referer,
            "x-csrf-token": self.csrf_token,
            "x-twitter-active-user": "yes",
            "x-twitter-auth-type": "OAuth2Session",
            "x-twitter-client-language": "zh-cn",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/147.0.0.0 Safari/537.36"
            ),
        }
        if self.transaction_id:
            headers["x-client-transaction-id"] = self.transaction_id
        if extra:
            headers.update(extra)
        return headers

    def graphql_url(self, operation: str) -> str:
        return f"{X_BASE_URL}/i/api/graphql/{QUERY_IDS[operation]}/{operation}"

    def request(self, method: str, url: str, **kwargs: Any) -> Any:
        response = self.session.request(method, url, timeout=30, **kwargs)
        try:
            data = response.json()
        except ValueError:
            data = response.text
        if response.status_code >= 400:
            raise SystemExit(f"HTTP {response.status_code}: {json.dumps(data, ensure_ascii=False)[:2000]}")
        return data

    def account(self) -> Any:
        return self.request(
            "GET",
            f"{X_BASE_URL}/i/api/1.1/account/verify_credentials.json",
            headers=self.headers(),
            params={"include_entities": "true", "skip_status": "true", "include_email": "false"},
        )

    def home_timeline(self, count: int) -> Any:
        return self.request(
            "GET",
            self.graphql_url("HomeTimeline"),
            headers=self.headers(),
            params={
                "variables": dumps(
                    {
                        "count": count,
                        "includePromotedContent": True,
                        "requestContext": "launch",
                        "withCommunity": True,
                    }
                ),
                "features": dumps(HOME_TIMELINE_FEATURES),
            },
        )

    def home_timeline_next(self, count: int, cursor: str | None, seen_tweet_ids: list[str]) -> Any:
        variables = {
            "count": count,
            "requestContext": "launch",
            "includePromotedContent": True,
            "withCommunity": True,
            "seenTweetIds": seen_tweet_ids,
        }
        if cursor:
            variables["cursor"] = cursor
        return self.request(
            "POST",
            self.graphql_url("HomeTimeline"),
            headers=self.headers(),
            json={
                "variables": variables,
                "features": HOME_TIMELINE_FEATURES,
                "queryId": QUERY_IDS["HomeTimeline"],
            },
        )

    def latest_timeline(self, count: int, cursor: str | None = None) -> Any:
        variables = {
            "count": count,
            "seenTweetIds": [],
            "enableRanking": False,
            "includePromotedContent": True,
        }
        if cursor:
            variables["cursor"] = cursor
            return self.request(
                "POST",
                self.graphql_url("HomeLatestTimeline"),
                headers=self.headers(),
                json={
                    "variables": variables,
                    "features": {**HOME_TIMELINE_FEATURES, "responsive_web_edit_tweet_api_enabled": True},
                    "queryId": QUERY_IDS["HomeLatestTimeline"],
                },
            )
        return self.request(
            "GET",
            self.graphql_url("HomeLatestTimeline"),
            headers=self.headers(),
            params={
                "variables": dumps(variables),
                "features": dumps({**HOME_TIMELINE_FEATURES, "responsive_web_edit_tweet_api_enabled": True}),
            },
        )

    def tweet_detail(self, tweet_id: str) -> Any:
        return self.request(
            "GET",
            self.graphql_url("TweetDetail"),
            headers=self.headers(referer=f"https://x.com/i/status/{tweet_id}"),
            params={
                "variables": dumps(
                    {
                        "focalTweetId": tweet_id,
                        "referrer": "home",
                        "with_rux_injections": False,
                        "rankingMode": "Relevance",
                        "includePromotedContent": True,
                        "withCommunity": True,
                        "withQuickPromoteEligibilityTweetFields": True,
                        "withBirdwatchNotes": True,
                        "withVoice": True,
                    }
                ),
                "features": dumps(HOME_TIMELINE_FEATURES),
                "fieldToggles": dumps(TWEET_DETAIL_FIELD_TOGGLES),
            },
        )

    def search(self, query: str, product: str, count: int, cursor: str | None = None) -> Any:
        variables = {
            "rawQuery": query,
            "count": count,
            "querySource": "typed_query",
            "product": product,
            "withGrokTranslatedBio": True,
        }
        if cursor:
            variables["cursor"] = cursor
        referer = f"https://x.com/search?q={quote(query)}&src=typed_query"
        if product == "Latest":
            referer += "&f=live"
        return self.request(
            "GET",
            self.graphql_url("SearchTimeline"),
            headers=self.headers(referer=referer),
            params={
                "variables": dumps(variables),
                "features": dumps(SEARCH_TIMELINE_FEATURES),
                "fieldToggles": dumps(SEARCH_TIMELINE_FIELD_TOGGLES),
            },
        )

    def user(self, screen_name: str) -> Any:
        return self.request(
            "GET",
            self.graphql_url("UserByScreenName"),
            headers=self.headers(referer=f"https://x.com/{screen_name}"),
            params={
                "variables": dumps({"screen_name": screen_name.lower(), "withSafetyModeUserFields": True}),
                "features": dumps(USER_PROFILE_FEATURES),
                "fieldToggles": dumps(USER_PROFILE_FIELD_TOGGLES),
            },
        )

    def user_tweets(self, user_id: str, count: int, cursor: str | None = None) -> Any:
        variables = {
            "userId": user_id,
            "count": count,
            "includePromotedContent": True,
            "withQuickPromoteEligibilityTweetFields": True,
            "withVoice": True,
            "withV2Timeline": True,
        }
        if cursor:
            variables["cursor"] = cursor
        return self.request(
            "GET",
            self.graphql_url("UserTweets"),
            headers=self.headers(),
            params={
                "variables": dumps(variables),
                "features": dumps(SEARCH_TIMELINE_FEATURES),
                "fieldToggles": dumps(USER_TWEETS_FIELD_TOGGLES),
            },
        )

    def following(self, user_id: str, count: int, cursor: str | None = None) -> Any:
        variables = {
            "userId": user_id,
            "count": count,
            "includePromotedContent": False,
            "withGrokTranslatedBio": True,
        }
        if cursor:
            variables["cursor"] = cursor
        return self.request(
            "GET",
            self.graphql_url("Following"),
            headers=self.headers(referer=f"https://x.com/i/user/{user_id}/following"),
            params={"variables": dumps(variables), "features": dumps({**HOME_TIMELINE_FEATURES, "rweb_cashtags_enabled": True})},
        )

    def create_tweet_payload(
        self,
        text: str,
        reply_to_id: str | None = None,
        attachment_url: str | None = None,
        media_ids: list[str] | None = None,
    ) -> dict[str, Any]:
        return {
            "variables": {
                "tweet_text": text,
                "reply": (
                    {"in_reply_to_tweet_id": reply_to_id, "exclude_reply_user_ids": []}
                    if reply_to_id
                    else None
                ),
                "attachment_url": attachment_url,
                "media": {
                    "media_entities": [{"media_id": media_id, "tagged_users": []} for media_id in (media_ids or [])],
                    "possibly_sensitive": False,
                },
                "semantic_annotation_ids": [],
                "disallowed_reply_options": None,
                "semantic_annotation_options": {"source": "Unknown"},
            },
            "features": CREATE_TWEET_FEATURES,
            "queryId": QUERY_IDS["CreateTweet"],
        }

    def create_tweet(self, payload: dict[str, Any], referer: str) -> Any:
        return self.request(
            "POST",
            self.graphql_url("CreateTweet"),
            headers=self.headers(referer=referer),
            json=payload,
        )

    def favorite(self, tweet_id: str, unfavorite: bool = False) -> Any:
        operation = "UnfavoriteTweet" if unfavorite else "FavoriteTweet"
        return self.request(
            "POST",
            self.graphql_url(operation),
            headers=self.headers(referer=f"https://x.com/i/status/{tweet_id}"),
            json={"variables": {"tweet_id": tweet_id}, "queryId": QUERY_IDS[operation]},
        )

    def friendship(self, user_id: str, destroy: bool = False) -> Any:
        endpoint = "destroy" if destroy else "create"
        form = {
            "include_profile_interstitial_type": "1",
            "include_blocking": "1",
            "include_blocked_by": "1",
            "include_followed_by": "1",
            "include_want_retweets": "1",
            "include_mute_edge": "1",
            "include_can_dm": "1",
            "include_can_media_tag": "1",
            "include_ext_is_blue_verified": "1",
            "include_ext_verified_type": "1",
            "include_ext_profile_image_shape": "1",
            "skip_status": "1",
            "user_id": user_id,
        }
        return self.request(
            "POST",
            f"{X_BASE_URL}/i/api/1.1/friendships/{endpoint}.json",
            headers=self.headers(extra={"content-type": "application/x-www-form-urlencoded"}),
            data=form,
        )

    def translate(self, tweet_id: str) -> Any:
        result = self.request(
            "POST",
            f"{API_BASE_URL}/2/grok/translation.json",
            headers=self.headers(extra={"content-type": "text/plain;charset=UTF-8"}),
            json={"content_type": "POST", "id": tweet_id, "dst_lang": "zh"},
        )
        if isinstance(result, str):
            try:
                return json.loads(base64.b64decode(result).decode("utf-8"))
            except Exception:
                return result
        return result

    def upload_media(self, file_path: Path) -> Any:
        content = file_path.read_bytes()
        media_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        init = self.request(
            "POST",
            f"{UPLOAD_BASE_URL}/i/media/upload.json",
            headers=self.headers(extra={"content-type": "application/x-www-form-urlencoded"}),
            params={
                "command": "INIT",
                "total_bytes": str(len(content)),
                "media_type": media_type,
                "media_category": "tweet_image",
            },
        )
        media_id = init["media_id_string"]
        self.request(
            "POST",
            f"{UPLOAD_BASE_URL}/i/media/upload.json",
            headers=self.headers(),
            params={"command": "APPEND", "media_id": media_id, "segment_index": "0"},
            files={"media": (file_path.name, content, media_type)},
        )
        return self.request(
            "POST",
            f"{UPLOAD_BASE_URL}/i/media/upload.json",
            headers=self.headers(extra={"content-type": "application/x-www-form-urlencoded"}),
            params={
                "command": "FINALIZE",
                "media_id": media_id,
                "original_md5": hashlib.md5(content).hexdigest(),
            },
        )


def require_execute(args: argparse.Namespace, preview: Any) -> bool:
    if args.execute:
        return True
    print("Dry-run only. Add --execute to send this mutating request.")
    print_json(preview)
    return False


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Test TouchFish X APIs")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("account")

    p = sub.add_parser("timeline")
    p.add_argument("--count", type=int, default=20)
    p.add_argument("--cursor")
    p.add_argument("--seen", default="")

    p = sub.add_parser("latest")
    p.add_argument("--count", type=int, default=20)
    p.add_argument("--cursor")

    p = sub.add_parser("tweet")
    p.add_argument("--tweet-id", required=True)

    p = sub.add_parser("search")
    p.add_argument("--query", required=True)
    p.add_argument("--product", choices=["Top", "Latest"], default="Top")
    p.add_argument("--count", type=int, default=20)
    p.add_argument("--cursor")

    p = sub.add_parser("user")
    p.add_argument("--screen-name", required=True)

    p = sub.add_parser("user-tweets")
    p.add_argument("--user-id", required=True)
    p.add_argument("--count", type=int, default=20)
    p.add_argument("--cursor")

    p = sub.add_parser("following")
    p.add_argument("--user-id", required=True)
    p.add_argument("--count", type=int, default=20)
    p.add_argument("--cursor")

    p = sub.add_parser("create-tweet")
    p.add_argument("--text", required=True)
    p.add_argument("--reply-to-id")
    p.add_argument("--attachment-url")
    p.add_argument("--media-id", action="append", default=[])
    p.add_argument("--execute", action="store_true")

    p = sub.add_parser("repost")
    p.add_argument("--comment", required=True)
    p.add_argument("--tweet-id", required=True)
    p.add_argument("--screen-name", default="i")
    p.add_argument("--execute", action="store_true")

    for name in ["favorite", "unfavorite"]:
        p = sub.add_parser(name)
        p.add_argument("--tweet-id", required=True)
        p.add_argument("--execute", action="store_true")

    for name in ["follow", "unfollow"]:
        p = sub.add_parser(name)
        p.add_argument("--user-id", required=True)
        p.add_argument("--execute", action="store_true")

    p = sub.add_parser("translate")
    p.add_argument("--tweet-id", required=True)

    p = sub.add_parser("upload-media")
    p.add_argument("--file", type=Path, required=True)
    p.add_argument("--execute", action="store_true")

    return parser


def main() -> int:
    args = build_parser().parse_args()
    client = XApiClient()

    if args.command == "account":
        print_json(client.account())
    elif args.command == "timeline":
        seen = [item for item in args.seen.split(",") if item]
        result = client.home_timeline_next(args.count, args.cursor, seen) if args.cursor or seen else client.home_timeline(args.count)
        print_json(result)
    elif args.command == "latest":
        print_json(client.latest_timeline(args.count, args.cursor))
    elif args.command == "tweet":
        print_json(client.tweet_detail(args.tweet_id))
    elif args.command == "search":
        print_json(client.search(args.query, args.product, args.count, args.cursor))
    elif args.command == "user":
        print_json(client.user(args.screen_name))
    elif args.command == "user-tweets":
        print_json(client.user_tweets(args.user_id, args.count, args.cursor))
    elif args.command == "following":
        print_json(client.following(args.user_id, args.count, args.cursor))
    elif args.command == "create-tweet":
        payload = client.create_tweet_payload(args.text, args.reply_to_id, args.attachment_url, args.media_id)
        referer = f"https://x.com/i/status/{args.reply_to_id}" if args.reply_to_id else args.attachment_url or "https://x.com/home"
        if require_execute(args, payload):
            print_json(client.create_tweet(payload, referer))
    elif args.command == "repost":
        attachment_url = f"https://x.com/{args.screen_name}/status/{args.tweet_id}"
        payload = client.create_tweet_payload(args.comment, attachment_url=attachment_url)
        if require_execute(args, payload):
            print_json(client.create_tweet(payload, attachment_url))
    elif args.command == "favorite":
        if require_execute(args, {"tweet_id": args.tweet_id, "operation": "FavoriteTweet"}):
            print_json(client.favorite(args.tweet_id))
    elif args.command == "unfavorite":
        if require_execute(args, {"tweet_id": args.tweet_id, "operation": "UnfavoriteTweet"}):
            print_json(client.favorite(args.tweet_id, unfavorite=True))
    elif args.command == "follow":
        if require_execute(args, {"user_id": args.user_id, "operation": "friendships/create"}):
            print_json(client.friendship(args.user_id))
    elif args.command == "unfollow":
        if require_execute(args, {"user_id": args.user_id, "operation": "friendships/destroy"}):
            print_json(client.friendship(args.user_id, destroy=True))
    elif args.command == "translate":
        print_json(client.translate(args.tweet_id))
    elif args.command == "upload-media":
        if require_execute(args, {"file": str(args.file), "operation": "media/upload"}):
            print_json(client.upload_media(args.file))
    return 0


if __name__ == "__main__":
    sys.exit(main())
