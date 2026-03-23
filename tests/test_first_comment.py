import os
from rmrbot.publisher.facebook_publisher import post_first_comment

# Set this to a real post ID on your page for testing
TEST_POST_ID = os.getenv("FB_TEST_POST_ID")
COMMENT_TEXT = "✅ Test comment to verify first-comment feature."

if not TEST_POST_ID:
    raise ValueError("Please set the FB_TEST_POST_ID environment variable for testing")

result = post_first_comment(TEST_POST_ID, COMMENT_TEXT)

if result:
    print("✅ Comment posted successfully:", result)
else:
    print("❌ Comment posting failed. Check logs for details.")