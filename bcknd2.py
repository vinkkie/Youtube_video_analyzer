import datetime
from yt_dlp import YoutubeDL

def extract_video_id(url):
    if "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1]
    return None

# # Placeholder functions - replace these with your actual logic
# def performance_score(views_per_day):
#     # Add your actual scoring algorithm here
#     return min(100, int(views_per_day / 100))

# def analyze_title(title):
#     # Add your actual title grading algorithm here
#     # Must return a tuple: (score, details_dict)
#     return 85, {"length": "Good", "keywords": "Excellent"}


class YouTubeAnalyzer:
    def get_video_info(self, video_url):
        ydl_opts = {'quiet': True, 'skip_download': True}
        with YoutubeDL(ydl_opts) as ydl:
            try:
                info_dict = ydl.extract_info(video_url, download=False)
                # Ensure we return a dictionary, fallback to empty dictionary if None
                return info_dict if info_dict else {}
            except Exception as e:
                print(f"Error extracting info: {e}")
                return {}

    def calculate_views_per_day(self, views, upload_date_str):
        if not upload_date_str:
            return views
        try:
            # yt-dlp returns date as 'YYYYMMDD' string
            upload_date = datetime.datetime.strptime(upload_date_str, "%Y%m%d").date()
            days_passed = (datetime.date.today() - upload_date).days
            return int(views / max(1, days_passed))
        except Exception:
            return views

    def get_transcript(self, video_id):
        # Place your transcript fetching code here
        return "Transcript text placeholder..."


def analyze_video(video_url):

    analyzer = YouTubeAnalyzer()

    info = analyzer.get_video_info(video_url)

    if not info:
        return None

    title = info.get(
        "title",
        "Unknown Title"
    )

    channel = info.get(
        "uploader",
        "Unknown Channel"
    )

    views = (
        info.get(
            "view_count",
            0
        ) or 0
    )

    likes = info.get(
        "like_count",
        0
    )

    duration = (
        info.get(
            "duration",
            0
        ) or 0
    )

    upload_date = info.get(
        "upload_date"
    )

    views_per_day = (
        analyzer.calculate_views_per_day(
            views,
            upload_date
        )
    )

    score = performance_score(
        views_per_day
    )

    video_id = extract_video_id(
        video_url
    )

    transcript = (
        analyzer.get_transcript(
            video_id
        )
    )

    title_score, details = (
        analyze_title(title)
    )

    return {

        "title": title,

        "channel": channel,

        "views": views,

        "likes": likes,

        "duration": duration,

        "upload_date": upload_date,

        "views_per_day": views_per_day,

        "transcript": transcript,

        "performance_score": score,

        "title_score": title_score,

        "title_analysis": details,

        "thumbnail": info.get(
            "thumbnail"
        ),

        "description": info.get(
            "description",
            ""
        ),

        "tags": info.get(
            "tags",
            []
        ),

        "categories": info.get(
            "categories",
            []
        ),

        "comment_count": info.get(
            "comment_count"
        ),

        "channel_followers": info.get(
            "channel_follower_count"
        )
    }


def performance_score(views_per_day):

    if views_per_day > 100000:
        return 95

    elif views_per_day > 50000:
        return 85

    elif views_per_day > 10000:
        return 70

    elif views_per_day > 1000:
        return 50

    else:
        return 20
    
    
def analyze_title(title):

    score = 0

    title_lower = title.lower()

    analysis = {}

    # --------------------------
    # Length
    # --------------------------

    length = len(title)

    if 20 <= length <= 60:
        score += 15
        analysis["optimal_length"] = True
    else:
        analysis["optimal_length"] = False

    # --------------------------
    # Question titles
    # --------------------------

    if "?" in title:
        score += 10
        analysis["question"] = True

    # --------------------------
    # Numbers
    # --------------------------

    if re.search(r"\d+", title):
        score += 10
        analysis["contains_number"] = True

    # --------------------------
    # Emotional words
    # --------------------------

    emotion_hits = [
        word
        for word in EMOTIONAL_WORDS
        if word in title_lower
    ]

    score += min(len(emotion_hits) * 5, 15)

    analysis["emotion_words"] = emotion_hits

    # --------------------------
    # Curiosity words
    # --------------------------

    curiosity_hits = [
        word
        for word in CURIOSITY_WORDS
        if word in title_lower
    ]

    score += min(len(curiosity_hits) * 5, 15)

    analysis["curiosity_words"] = curiosity_hits

    # --------------------------
    # Relatability
    # --------------------------

    relatable_hits = [
        word
        for word in RELATABLE_WORDS
        if word in title_lower
    ]

    score += min(len(relatable_hits) * 5, 10)

    analysis["relatable_words"] = relatable_hits

    # --------------------------
    # Urgency
    # --------------------------

    urgency_hits = [
        word
        for word in URGENCY_WORDS
        if word in title_lower
    ]

    score += min(len(urgency_hits) * 5, 10)

    analysis["urgency_words"] = urgency_hits

    # --------------------------
    # Emojis
    # --------------------------

    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "]+",
        flags=re.UNICODE
    )

    emojis = emoji_pattern.findall(title)

    if emojis:
        score += min(len(emojis) * 3, 12)

    analysis["emojis"] = emojis

    # --------------------------
    # Hashtags
    # --------------------------

    hashtags = re.findall(r"#(\w+)", title_lower)

    hashtag_hits = [
        tag
        for tag in hashtags
        if tag in TRENDING_HASHTAGS
    ]

    score += min(len(hashtag_hits) * 5, 15)

    analysis["hashtags"] = hashtags
    analysis["trending_hashtags"] = hashtag_hits

    # --------------------------
    # Capitalization emphasis
    # --------------------------

    words = title.split()

    capital_words = [
        word
        for word in words
        if len(word) > 2 and word.isupper()
    ]

    if capital_words:
        score += 5

    analysis["capital_words"] = capital_words

    score = min(score, 100)

    return score, analysis

import re

# Common viral / trending hashtags
TRENDING_HASHTAGS = {
    "shorts",
    "viral",
    "trending",
    "fyp",
    "motivation",
    "mindset",
    "success",
    "life",
    "business",
    "music",
    "bhajan",
    "spirituality",
    "podcast",
    "ai",
    "facts"
}

# Emotional triggers
EMOTIONAL_WORDS = {
    "secret",
    "truth",
    "mistake",
    "shocking",
    "powerful",
    "amazing",
    "unbelievable",
    "surprising",
    "warning",
    "dangerous",
    "crazy",
    "incredible"
}

# Curiosity triggers
CURIOSITY_WORDS = {
    "why",
    "how",
    "what",
    "when",
    "hidden",
    "nobody",
    "never",
    "unexpected",
    "revealed",
    "behind"
}

# Relatability triggers
RELATABLE_WORDS = {
    "you",
    "your",
    "everyone",
    "nobody",
    "people",
    "parents",
    "student",
    "students",
    "wife",
    "husband",
    "mother",
    "father",
    "friend",
    "friends"
}

# Urgency triggers
URGENCY_WORDS = {
    "now",
    "today",
    "before",
    "immediately",
    "urgent",
    "last chance",
    "don't",
    "stop"
}

if __name__ == "__main__":

    url = input(
        "Enter YouTube Video URL: "
    )

    result = analyze_video(
        url
    )

    print(result)
