import streamlit as st
from gtts import gTTS
import os
from googletrans import Translator

# =====================================================
# CẤU HÌNH HỆ THỐNG
# =====================================================
HOSPITAL_NAME = "Trung tâm tiêm chủng VNVB"

# =====================================================
# CÀI ĐẶT GIAO DIỆN
# =====================================================
st.set_page_config(
    page_title="Hệ thống gọi khách hàng",
    page_icon="📢",
    layout="centered"
)

st.title("📢 Hệ thống gọi khách hàng - " + HOSPITAL_NAME)

st.markdown("""
Ứng dụng hỗ trợ phát thanh tự động cho bệnh viện. Đây là một công cụ giúp giảm tải cho nhân viên y tế trong việc gọi khách hàng. Ứng dụng sử dụng **Streamlit** để tạo giao diện trực quan, **gTTS** để tạo giọng nói và **googletrans** để dịch tự động.
""")

# =====================================================
# NHẬP DỮ LIỆU NGƯỜI DÙNG
# =====================================================
name = st.text_input("🧑 Nhập tên khách hàng:")
location = st.text_input("📍 Nhập địa điểm:")
closing = st.selectbox(
    "🙏 Chọn lời kết:",
    [
        "Xin cảm ơn!",
        "Trân trọng cảm ơn!",
        "Cảm ơn!",
        "Vui lòng đến ngay!",
        "Chúc sức khỏe!",
        "Rất mong quý khách hợp tác!",
        ""
    ]
)

# =====================================================
# LỰA CHỌN NGÔN NGỮ
# =====================================================
lang_option = st.radio(
    "🌐 Chọn ngôn ngữ phát thanh:",
    [
        "Chỉ tiếng Việt",
        "Tiếng Việt + Tiếng Anh"
    ],
    horizontal=True
)

# =====================================================
# HÀM HỖ TRỢ
# =====================================================
def generate_tts(text: str, lang: str, filename: str):
    """
    Tạo file âm thanh từ văn bản sử dụng gTTS.

    Args:
        text (str): Chuỗi văn bản cần chuyển đổi.
        lang (str): Mã ngôn ngữ (vi, en, ...).
        filename (str): Tên file mp3 xuất ra.

    Returns:
        str | None: Trả về đường dẫn file nếu thành công, None nếu thất bại.
    """
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
        return filename
    except Exception as e:
        st.error(f"❌ Lỗi tạo giọng nói: {e}")
        return None


def build_vietnamese_announcement(name: str, location: str, closing: str) -> str:
    """Ghép câu thông báo tiếng Việt."""
    return f"Xin mời khách hàng {name} đến {location}. {closing} ."


def translate_text_to_english(text: str) -> str:
    """Dịch văn bản từ tiếng Việt sang tiếng Anh."""
    translator = Translator()
    return translator.translate(text, src='vi', dest='en').text

# =====================================================
# XỬ LÝ KHI NGƯỜI DÙNG NHẤN NÚT
# =====================================================
if st.button("▶️ Tạo & Phát thông báo"):
    if name.strip() == "" or location.strip() == "":
        st.warning("⚠️ Vui lòng nhập đủ tên khách hàng và địa điểm!")
    else:
        # --- Thông báo tiếng Việt ---
        text_vi = build_vietnamese_announcement(name, location, closing)
        st.subheader("📌 Thông báo Tiếng Việt")
        st.success(text_vi)

        vi_path = generate_tts(text_vi, 'vi', "output_vi.mp3")
        if vi_path:
            st.audio(vi_path, format="audio/mp3")

        # --- Thông báo tiếng Anh nếu chọn ---
        if lang_option == "Tiếng Việt + Tiếng Anh":
            try:
                text_en = translate_text_to_english(text_vi)
                st.subheader("📌 Announcement in English")
                st.info(text_en)

                en_path = generate_tts(text_en, 'en', "output_en.mp3")
                if en_path:
                    st.audio(en_path, format="audio/mp3")
            except Exception as e:
                st.error(f"❌ Lỗi dịch sang tiếng Anh: {e}")

        st.success("✅ Hoàn tất phát thanh!")
