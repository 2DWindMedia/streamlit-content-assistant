import openai
import requests
from bs4 import BeautifulSoup
from pytrends.request import TrendReq
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Cấu hình API Key của bạn
openai.api_key = "YOUR_API_KEY_HERE"  # Thay bằng API key thực tế của bạn

# Hàm 1: Tạo ý tưởng video ngắn
def generate_idea(trend, target_audience, platform):
    """
    Tạo ý tưởng video ngắn dựa trên xu hướng và đối tượng mục tiêu.
    """
    prompt = f"""
Bạn là trợ lý sáng tạo nội dung trên TikTok. Tôi cần tạo ý tưởng video:
- Xu hướng: {trend}
- Đối tượng mục tiêu: {target_audience}
- Nền tảng: {platform}

Hãy đề xuất chi tiết:
1. Một ý tưởng chính, phù hợp với giới trẻ và dễ lan truyền.
2. Tiêu đề hấp dẫn, không quá 50 ký tự.
3. Nội dung kịch bản từng bước, giới hạn 100 giây video.
4. Danh sách hashtag liên quan.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# Hàm 2: Lưu ý tưởng vào file
def save_to_file(content, filename="ideas.txt"):
    """
    Lưu nội dung vào file.
    """
    with open(filename, "a", encoding="utf-8") as file:
        file.write(content + "\n\n")
    print(f"Ý tưởng đã được lưu vào file: {filename}")

# Hàm 3: Lấy xu hướng từ Google Trends
def get_google_trends():
    """
    Lấy danh sách từ khóa xu hướng từ Google Trends.
    """
    pytrends = TrendReq(hl="en-US", tz=360)
    trending_searches = pytrends.trending_searches(pn="vietnam")  # Khu vực Việt Nam
    trends = trending_searches[0].tolist()
    return trends

# Hàm 4: Nhập xu hướng TikTok bằng tay
def input_tiktok_trends():
    """
    Cho phép người dùng nhập danh sách trend TikTok bằng tay.
    """
    print("Nhập các trend TikTok (gõ 'done' để kết thúc):")
    trends = []
    while True:
        trend = input("Nhập trend: ")
        if trend.lower() == 'done':
            break
        trends.append(trend.strip())
    return trends

# Hàm 5: Lưu danh sách trend vào file
def save_trends_to_file(trends, filename="tiktok_trends.txt"):
    """
    Lưu danh sách trend vào file.
    """
    with open(filename, "w", encoding="utf-8") as file:
        for trend in trends:
            file.write(trend + "\n")
    print(f"Danh sách trend đã được lưu vào file: {filename}")

# Hàm 6: Đọc danh sách trend từ file
def load_trends_from_file(filename="tiktok_trends.txt"):
    """
    Đọc danh sách trend từ file.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            trends = [line.strip() for line in file.readlines()]
        return trends
    except FileNotFoundError:
        print(f"File {filename} không tồn tại. Vui lòng nhập tay.")
        return []

# Main: Sử dụng các hàm đã xây dựng
if __name__ == "__main__":
    # Hỏi người dùng muốn nhập tay hay đọc từ file
    print("\nBạn muốn nhập trend TikTok bằng tay hay đọc từ file?")
    choice = input("Nhập '1' để nhập tay, '2' để đọc từ file: ").strip()

    if choice == '1':
        # Nhập trend TikTok bằng tay
        tiktok_trends = input_tiktok_trends()
        save_trends_to_file(tiktok_trends)
    elif choice == '2':
        # Đọc trend TikTok từ file
        tiktok_trends = load_trends_from_file()
    else:
        print("Lựa chọn không hợp lệ.")
        tiktok_trends = []

    if not tiktok_trends:
        print("Không tìm thấy xu hướng TikTok nào.")
    else:
        print("Xu hướng TikTok:")
        for trend in tiktok_trends:
            print(f"- {trend}")
            try:
                # Tạo ý tưởng video từ xu hướng
                idea = generate_idea(trend, "Người trẻ từ 18-25 tại Việt Nam", "TikTok")
                print("\nÝ tưởng video:")
                print(idea)

                # Lưu ý tưởng vào file
                save_to_file(idea)
            except Exception as e:
                print(f"Lỗi khi tạo ý tưởng: {e}")
