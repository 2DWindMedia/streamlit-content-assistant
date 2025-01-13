import openai
import streamlit as st
from pytrends.request import TrendReq

# Cấu hình API Key của bạn
openai.api_key = "YOUR_API_KEY_HERE"  # Thay bằng API Key thực tế của bạn

# Hàm lấy xu hướng từ Google Trends
def get_google_trends():
    pytrends = TrendReq(hl="en-US", tz=360)
    trending_searches = pytrends.trending_searches(pn="vietnam")
    return trending_searches[0].tolist()

# Hàm tạo ý tưởng video
def generate_idea(trend, target_audience, platform):
    prompt = f"""
    Bạn là trợ lý sáng tạo nội dung. Tôi cần tạo ý tưởng video ngắn:
    - Xu hướng: {trend}
    - Đối tượng mục tiêu: {target_audience}
    - Nền tảng: {platform}

    Hãy đề xuất:
    1. Một ý tưởng chính.
    2. Tiêu đề hấp dẫn.
    3. Nội dung kịch bản chi tiết.
    4. Hashtag phù hợp.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# Giao diện chính
def main():
    st.title("Trợ Lý Sáng Tạo Nội Dung")
    st.subheader("Tạo ý tưởng video từ xu hướng")

    # Lựa chọn nguồn xu hướng
    source = st.radio("Chọn nguồn xu hướng:", ("Nhập tay", "Google Trends"))

    # Nhập xu hướng
    if source == "Nhập tay":
        tiktok_trends = st.text_area("Nhập các xu hướng TikTok (mỗi dòng một xu hướng):")
        trends = [trend.strip() for trend in tiktok_trends.splitlines() if trend.strip()]
    elif source == "Google Trends":
        if st.button("Lấy xu hướng từ Google Trends"):
            trends = get_google_trends()
            st.write("Xu hướng từ Google Trends:")
            for trend in trends:
                st.write(f"- {trend}")
        else:
            trends = []

    # Tạo ý tưởng video
    if st.button("Tạo ý tưởng video"):
        if trends:
            for trend in trends:
                st.write(f"### Xu hướng: {trend}")
                idea = generate_idea(trend, "Người trẻ từ 18-25 tại Việt Nam", "TikTok")
                st.text_area("Ý tưởng video:", idea, height=300)
        else:
            st.warning("Hãy nhập hoặc chọn ít nhất một xu hướng để tạo ý tưởng!")

if __name__ == "__main__":
    main()
