import streamlit as st
import time
from utils import text_to_speech

def home_page():
    """Hiển thị trang chủ giới thiệu hệ thống"""
    # ======= CSS TÙY CHỈNH =======
    st.markdown("""
    <style>
        /* Tiêu đề chính */
        .main-header {
            text-align: center;
            padding: 2rem;
            background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
            color: white;
            border-radius: 15px;
            margin: 1rem 0;
            box-shadow: 0 4px 15px rgba(76,175,80,0.3);
        }

        /* Card giới thiệu */
        .feature-card {
            background: white;
            border-radius: 15px;
            padding: 2rem;
            margin: 1.5rem 0;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            border: 1px solid #e0e0e0;
            transition: transform 0.3s, box-shadow 0.3s;
        }

        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }

        /* Nút lớp học */
        .class-card {
            padding: 2rem;
            border-radius: 15px;
            background: linear-gradient(145deg, #f5f5f5 0%, #ffffff 100%);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            text-align: center;
            min-height: 180px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .class-card:hover {
            transform: scale(1.03);
            box-shadow: 0 8px 25px rgba(76,175,80,0.2);
            background: linear-gradient(145deg, #e8f5e9 0%, #ffffff 100%);
        }

        /* Hướng dẫn sử dụng */
        .guide-step {
            padding: 1.5rem;
            background: #f8f9fa;
            border-left: 4px solid #4CAF50;
            margin: 1rem 0;
            border-radius: 8px;
        }

        /* Thông tin liên hệ */
        .contact-card {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 2rem;
            margin-top: 2rem;
            text-align: center;
        }

        .badge {
            display: inline-block;
            padding: 0.5rem 1rem;
            background: #4CAF50;
            color: white;
            border-radius: 20px;
            margin: 0.5rem;
            font-size: 0.9rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # ======= PHẦN NỘI DUNG =======
    # Header chính
    st.markdown("""
    <div class="main-header">
        <h1 style="margin:0; font-size:2.5rem">📚 Hệ thống kích thích tư duy học tập và hỗ trợ điều chỉnh tư thế ngồi thông minh dành cho người khiếm thị</h1>
    </div>
    """, unsafe_allow_html=True)
    text_to_speech("Hệ thống kích thích tư duy học tập và hỗ trợ điều chỉnh tư thế ngồi thông minh cho người khiếm thị")
    time.sleep(1)

    # Giới thiệu hệ thống
    with st.container():
        st.markdown("""
        <div class="feature-card">
            <h3 style="color:#2E7D32; margin-top:0">🌐 Giới Thiệu Hệ Thống</h3>
            <p style="font-size:1.05rem; line-height:1.6">
            Hệ thống tích hợp công nghệ AI tiên tiến hỗ trợ học tập đa phương thức với:
            </p>
            <div style="display: flex; gap:1rem; flex-wrap:wrap;">
                <span class="badge">🎤 Nhận diện giọng nói</span>
                <span class="badge">📖 Học liệu đa dạng</span>
                <span class="badge">🤖 Trợ lý ảo thông minh</span>
                <span class="badge">📊 Báo cáo học tập</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔊 Nghe giới thiệu hệ thống", use_container_width=True):
            intro_text = """
                        Hệ thống được thiết kế để hỗ trợ học sinh, 
                        đặc biệt là học sinh khiếm thị, tiếp cận kiến thức dễ dàng thông qua 
                        đa dạng hình thức: văn bản, âm thanh, hình ảnh và tương tác.
                        """
            text_to_speech(intro_text)

    # Lớp học
    st.markdown("### 📚 Chọn Lớp Học")
    cols = st.columns(3)
    class_info = {
        1: {"color": "#4CAF50", "icon": "🧮"},
        2: {"color": "#2196F3", "icon": "📚"},
        3: {"color": "#9C27B0", "icon": "🌍"},
        4: {"color": "#FF9800", "icon": "⚛️"},
        5: {"color": "#E91E63", "icon": "🎨"}
    }

    for i in range(1, 6):
        with cols[(i - 1) % 3]:
            info = class_info[i]
            html = f"""
            <div class="class-card" onclick="window.location.href='?class={i}'">
                <div style="font-size:2.5rem; margin-bottom:1rem">{info['icon']}</div>
                <h3 style="margin:0; color:{info['color']}">Lớp {i}</h3>
            </div>
            """
            st.markdown(html, unsafe_allow_html=True)
    intro_text = """
                            Hệ thống được thiết kế để hỗ trợ học sinh, 
                            đặc biệt là học sinh khiếm thị, tiếp cận kiến thức dễ dàng thông qua 
                            đa dạng hình thức: văn bản, âm thanh, hình ảnh và tương tác.
                            """
    text_to_speech(intro_text)
    time.sleep(3)
    # text_to_speech("Bạn muốn vào lớp mấy?")
    # # speech = recognize_speech().lower()
    # time.sleep(2)
    # speech = "lớp 4"
    # # Nhận diện lớp học
    # for i in range(1, 6):
    #     if f"lớp {i}" in speech:
    #         text_to_speech(f"Bạn đã chọn lớp {i}")
    #         st.session_state.selected_class = i
    #         break

    if "guide_read" not in st.session_state:
        st.session_state.guide_read = False

    # Hướng dẫn sử dụng (theo các phím tắt ALT)
    with st.expander("📘 Hướng Dẫn Sử Dụng Nhanh Bằng Bàn Phím", expanded=False):
        st.markdown("""
        <div class="guide-step">
            <h4>🎯 Điều hướng nhanh</h4>
            <ul>
                <li><b>Alt + 1</b>: Về trang chủ</li>
                <li><b>Alt + 2</b>: Mở trang bài học</li>
                <li><b>Alt + 3</b>: Mở trang kiểm tra kiến thức</li>
                <li><b>Alt + 4</b>: Mở trang hỗ trợ học tập</li>
            </ul>
        </div>

        <div class="guide-step">
            <h4>🃏 Flashcard</h4>
            <ul>
                <li><b>Alt + M</b>: Chuyển sang flashcard tiếp theo</li>
                <li><b>Alt + B</b>: Phát tiếng Anh của flashcard</li>
                <li><b>Alt + V</b>: Phát tiếng Việt của flashcard</li>
                <li><b>Alt + N</b>: Phát tiếng Nhật của flashcard</li>
            </ul>
        </div>

        <div class="guide-step">
            <h4>🎤 Giọng nói</h4>
            <ul>
                <li><b>Alt + 5</b>: Bật chế độ điều khiển bằng giọng nói</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Tự động đọc hướng dẫn nếu chưa đọc
        if not st.session_state.guide_read:
            huong_dan = """
            Hướng dẫn sử dụng bằng phím tắt:
            Alt + 1 để về trang chủ.
            Alt + 2 để mở trang bài học.
            Alt + 3 để mở trang kiểm tra kiến thức.
            Alt + 4 để mở trang hỗ trợ học tập.
            Alt + M để chuyển sang flashcard tiếp theo.
            Alt + B để nghe phát âm tiếng Anh.
            Alt + V để nghe phát âm tiếng Việt.
            Alt + N để nghe phát âm tiếng Nhật.
            Alt + 5 để bật điều khiển bằng giọng nói.
            """
            text_to_speech(huong_dan)
            st.session_state.guide_read = True

    # Thông tin liên hệ
    st.markdown("""
    <div class="contact-card">
        <h3 style="margin-top:0">📬 Liên Hệ Hỗ Trợ</h3>
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap:1rem;">
            <div style="padding:1rem; background:#fff; border-radius:10px;">
                <h4 style="margin:0 0 0.5rem 0">💌 Email</h4>
                <p style="margin:0">support@hocsinhthongminh.vn</p>
            </div>
            <div style="padding:1rem; background:#fff; border-radius:10px;">
                <h4 style="margin:0 0 0.5rem 0">📞 Hotline</h4>
                <p style="margin:0">1900 1234 (24/7)</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    # text_to_speech(intro_text)
    time.sleep(1)
    text_to_speech("Bạn học lớp mấy?")
    # speech = recognize_speech().lower()
    time.sleep(2)
    speech = "lớp 4"
    # Nhận diện lớp học
    for i in range(1, 6):
        if f"lớp {i}" in speech:
            text_to_speech(f"Bạn đã chọn lớp {i}")
            st.session_state.selected_class = i
            break
