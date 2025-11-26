import streamlit as st
import google.generativeai as genai
from docx import Document
from io import BytesIO
from PIL import Image

# --- CẤU HÌNH ---
st.set_page_config(page_title="Smart-Print AI Điện Biên", page_icon="🇻🇳", layout="wide")

# --- SIDEBAR ---
with st.sidebar:
    st.header("🔑 CÀI ĐẶT")
    api_key = st.text_input("Nhập Google API Key:", type="password")
    
    # Nút kiểm tra hệ thống (Mới)
    if st.button("Kiểm tra kết nối AI"):
        if not api_key:
            st.error("Chưa nhập Key!")
        else:
            try:
                genai.configure(api_key=api_key)
                # Lấy danh sách các model mà máy chủ hỗ trợ
                models = [m.name for m in genai.list_models()]
                st.success(f"Kết nối thành công! Các model hiện có: {models}")
            except Exception as e:
                st.error(f"Lỗi kết nối: {e}")

    st.markdown("---")
    st.header("👤 HỌC SINH")
    ten_hs = st.text_input("Họ tên:", "Lò Văn Páo")
    lop = st.selectbox("Lớp:", ["Lớp 1", "Lớp 2", "Lớp 3", "Lớp 4", "Lớp 5"])

# --- HÀM XỬ LÝ (DÙNG GEMINI-PRO ỔN ĐỊNH) ---
def ai_soan_bai(api_key, mon, lop, chu_de, nang_luc):
    # Cấu hình lại key trong hàm để đảm bảo nhận key mới nhất
    genai.configure(api_key=api_key)
    
    prompt = f"""
    Bạn là giáo viên tiểu học. Soạn phiếu bài tập môn {mon} lớp {lop}.
    Chủ đề: {chu_de} (Sách Kết nối tri thức).
    Học sinh: {nang_luc}. Địa phương: Điện Biên.
    Viết dạng văn bản thuần, không dùng Markdown (không dùng dấu #, dấu *).
    Gồm: 1. Mục tiêu. 2. Bài tập (2 câu). 3. Gợi ý.
    """
    try:
        # DÙNG GEMINI-PRO (BẢN CHUẨN) - KHÔNG DÙNG FLASH NỮA
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Lỗi AI: {str(e)}"

def ai_cham_bai(api_key, image, mon, lop):
    genai.configure(api_key=api_key)
    prompt = f"Chấm bài {mon} lớp {lop}. Đọc chữ viết tay, chấm điểm và nhận xét ngắn gọn."
    try:
        # DÙNG GEMINI-PRO-VISION (BẢN CHUẨN CHO ẢNH)
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"Lỗi Vision: {str(e)}"

def tao_file_word(ten, noi_dung):
    doc = Document()
    doc.add_heading(f'PHIẾU BÀI TẬP: {ten.upper()}', 0)
    doc.add_paragraph(noi_dung)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- GIAO DIỆN CHÍNH ---
st.title("🏫 Smart-Print AI: Phiên bản Ổn định")

tab1, tab2 = st.tabs(["📝 SOẠN BÀI", "📷 CHẤM BÀI"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        mon_hoc = st.selectbox("Môn học", ["Toán", "Tiếng Việt", "Tự nhiên Xã hội", "Khoa học", "Lịch sử & Địa lý", "Tin học", "Công nghệ", "Tiếng Anh", "Đạo đức", "Âm nhạc", "Mĩ thuật", "Thể dục"])
        bai_hoc = st.text_input("Tên bài học:", "Bài ôn tập")
    with col2:
        hoc_luc = st.radio("Mức độ:", ["Cơ bản", "Nâng cao"])
        st.write("")
        btn_soan = st.button("🚀 SOẠN BÀI")
    
    if btn_soan:
        if not api_key:
            st.warning("⚠️ Vui lòng nhập API Key!")
        else:
            with st.spinner("Đang soạn thảo..."):
                ket_qua = ai_soan_bai(api_key, mon_hoc, lop, bai_hoc, hoc_luc)
                
                if "Lỗi AI" in ket_qua:
                    st.error(ket_qua)
                    st.info("Hãy bấm nút 'Kiểm tra kết nối AI' bên trái để xem lỗi chi tiết.")
                else:
                    st.success("Xong!")
                    st.text_area("Nội dung:", ket_qua, height=300)
                    file_doc = tao_file_word(ten_hs, ket_qua)
                    st.download_button("📥 Tải Word", file_doc, "Phieu_Bai_Tap.docx")

with tab2:
    uploaded_file = st.file_uploader("Tải ảnh bài làm", type=['jpg', 'png', 'jpeg'])
    if uploaded_file and st.button("✨ CHẤM BÀI"):
        if not api_key:
            st.warning("Chưa có Key!")
        else:
            with st.spinner("Đang chấm..."):
                img = Image.open(uploaded_file)
                st.image(img, width=300)
                ket_qua = ai_cham_bai(api_key, img, mon_hoc, lop)
                st.write(ket_qua)
