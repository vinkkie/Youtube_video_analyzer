import streamlit as st
import pandas as pd

from bcknd2 import analyze_video


# ----------------------------------------
# Page Configuration
# ----------------------------------------

st.set_page_config(
    page_title="YouTube Video Intelligence",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 YouTube Video Intelligence")

st.caption(
    "Analyze any public YouTube video using metadata, title intelligence, and performance metrics."
)


# ----------------------------------------
# URL INPUT
# ----------------------------------------

video_url = st.text_input(
    "Enter YouTube Video URL"
)


# ----------------------------------------
# ANALYZE BUTTON
# ----------------------------------------

if st.button("Analyze Video"):

    if not video_url.strip():

        st.error("Please enter a valid YouTube URL")

    else:

        try:

            with st.spinner("Analyzing video..."):

                result = analyze_video(video_url)
                if result is None:
                    st.error("Could not fetch video information.")
                    st.stop()

            st.success("Analysis Complete")

            st.divider()

            # ----------------------------------------
            # THUMBNAIL
            # ----------------------------------------

            thumbnail = result.get("thumbnail")

            if thumbnail:

                st.image(
                    thumbnail,
                    caption="Video Thumbnail",
                    width=600
                )

            # ----------------------------------------
            # METRICS
            # ----------------------------------------

            st.subheader("📊 Performance Metrics")

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.metric(
                    "Views",
                    f"{result['views']:,}"
                )

            with col2:

                likes = result.get("likes")

                st.metric(
                    "Likes",
                    f"{likes:,}" if likes else "N/A"
                )

            with col3:

                st.metric(
                    "Views / Day",
                    f"{result['views_per_day']:,}"
                )

            with col4:

                comments = result.get(
                    "comment_count"
                )

                st.metric(
                    "Comments",
                    f"{comments:,}" if comments else "N/A"
                )

            st.divider()

            # ----------------------------------------
            # VIDEO DETAILS
            # ----------------------------------------

            st.subheader("🎥 Video Details")

            st.write(
                f"**Title:** {result['title']}"
            )

            st.write(
                f"**Channel:** {result['channel']}"
            )

            st.write(
                f"**Upload Date:** {result['upload_date']}"
            )

            st.write(
                f"**Duration:** {result['duration']} seconds"
            )

            followers = result.get(
                "channel_followers"
            )

            if followers:

                st.write(
                    f"**Channel Followers:** {followers:,}"
                )

            st.divider()

            # ----------------------------------------
            # SCORES
            # ----------------------------------------

            st.subheader("🏆 Scores")

            score_col1, score_col2 = st.columns(2)

            with score_col1:

                st.write(
                    f"### Performance Score: {result['performance_score']}/100"
                )

                st.progress(
                    result['performance_score'] / 100
                )

            with score_col2:

                st.write(
                    f"### Title Score: {result['title_score']}/100"
                )

                st.progress(
                    result['title_score'] / 100
                )

            st.divider()

            # ----------------------------------------
            # TITLE ANALYSIS
            # ----------------------------------------

            st.subheader("📝 Title Analysis")

            title_analysis = result.get(
                "title_analysis",
                {}
            )

            if title_analysis:

                analysis_df = pd.DataFrame(
                    list(title_analysis.items()),
                    columns=[
                        "Factor",
                        "Value"
                    ]
                )

                st.dataframe(
                    analysis_df,
                    use_container_width=True
                )

            else:

                st.info(
                    "No title analysis available."
                )

            st.divider()

            # ----------------------------------------
            # TAGS
            # ----------------------------------------

            st.subheader("🏷️ Tags")

            tags = result.get("tags")

            if tags:

                st.write(tags)

            else:

                st.info(
                    "No tags available."
                )

            st.divider()

            # ----------------------------------------
            # CATEGORIES
            # ----------------------------------------

            st.subheader("📂 Categories")

            categories = result.get(
                "categories"
            )

            if categories:

                st.write(categories)

            else:

                st.info(
                    "No category information."
                )

            st.divider()

            # ----------------------------------------
            # DESCRIPTION
            # ----------------------------------------

            st.subheader("📖 Description")

            description = result.get(
                "description"
            )

            if description:

                st.text_area(
                    "",
                    description,
                    height=250
                )

            else:

                st.info(
                    "Description unavailable."
                )

            st.divider()

            # ----------------------------------------
            # TRANSCRIPT
            # ----------------------------------------

            st.subheader(
                "🎤 Transcript Preview"
            )

            transcript = result.get(
                "transcript",
                ""
            )

            st.text_area(
                "",
                transcript[:5000],
                height=350
            )

        except Exception as e:

            st.error(
                f"Analysis failed: {str(e)}"
            )
