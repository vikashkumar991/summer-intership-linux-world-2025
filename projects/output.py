```python
import streamlit as st
import tweepy
import os

# Get Twitter API keys from environment variables
# It's highly recommended to store these securely, e.g., in environment variables or a secrets management system.
# Example:
# CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY")
# CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET")
# ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
# ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

# **IMPORTANT: Replace these placeholders with your actual Twitter API keys or environment variable calls.**
# For local development, you can set these directly, but for deployment, use environment variables.
CONSUMER_KEY = "YOUR_CONSUMER_KEY"
CONSUMER_SECRET = "YOUR_CONSUMER_SECRET"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
ACCESS_TOKEN_SECRET = "YOUR_ACCESS_TOKEN_SECRET"

# Authenticate with Twitter
try:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    api.verify_credentials() # Verify that the credentials are valid
    st.success("Successfully authenticated with Twitter!")
except tweepy.TweepyException as e:
    st.error(f"Error authenticating with Twitter. Please check your API keys and internet connection: {e}")
    st.stop() # Stop the app if authentication fails

st.title("Twitter Post Sender")
st.write("Enter your message below and click 'Send Tweet' to post it on Twitter.")

tweet_message = st.text_area("Your Tweet Message:", max_chars=280, height=150, help="Tweets are limited to 280 characters.")

if st.button("Send Tweet"):
    if tweet_message:
        try:
            # Send the tweet
            api.update_status(tweet_message)
            st.success("Tweet sent successfully!")
            st.balloons() # Show a celebratory animation
            st.write(f"You tweeted: \"{tweet_message}\"")
            # Note: Streamlit widgets don't directly update their values in this way
            # For clearing, you'd typically use session state or rerun the app.
            # tweet_message = "" # This line won't clear the text_area directly in Streamlit's execution model
        except tweepy.TweepyException as e:
            st.error(f"Error sending tweet: {e}")
    else:
        st.warning("Please enter a message before sending your tweet.")

st.markdown("---")
st.markdown("Developed with using Streamlit and Tweepy")
```