import streamlit as st
import tweepy
import os

CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET")
ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

if not all([CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
    st.error("Twitter API keys are not set. Please set TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, and TWITTER_ACCESS_TOKEN_SECRET environment variables.")
    st.stop()

try:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    api.verify_credentials()
    st.success("Successfully authenticated with Twitter!")
except tweepy.TweepyException as e:
    st.error(f"Error authenticating with Twitter. Please check your API keys and internet connection: {e}")
    st.stop()

st.title("Twitter Post Sender")
st.write("Enter your message below and click 'Send Tweet' to post it on Twitter.")

if 'tweet_message_input' not in st.session_state:
    st.session_state.tweet_message_input = ""

tweet_message = st.text_area(
    "Your Tweet Message:",
    max_chars=280,
    height=150,
    help="Tweets are limited to 280 characters.",
    key="tweet_input_area",
    value=st.session_state.tweet_message_input
)

if st.button("Send Tweet"):
    if tweet_message:
        try:
            api.update_status(tweet_message)
            st.success("Tweet sent successfully!")
            st.balloons()
            st.write(f"You tweeted: \"{tweet_message}\"")
            st.session_state.tweet_message_input = ""
            st.experimental_rerun()
        except tweepy.TweepyException as e:
            st.error(f"Error sending tweet: {e}")
    else:
        st.warning("Please enter a message before sending your tweet.")

st.markdown("---")
st.markdown("Developed with using Streamlit and Tweepy")