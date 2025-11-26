import streamlit as st
import google.generativeai as genai
from docx import Document
from io import BytesIO
from PIL import Image

# --- CẤU HÌNH ---
st.set_page_config(page_title="Smart-Print AI Điện Biên", page_icon="🇻🇳", layout="wide")

# --- SIDEBAR ---
with st.sidebar:
    st.header("🔑 CÀI ĐẶT HỆ THỐNG")
    api_key = st.text_input("1. Nhập Google API Key:", type="password")
    
    selected_model = None
    
    if api_key:
        try:
            genai.configure(api_key=api_key)
            # Tự động lấy danh sách model từ Google (như trong video của bạn)
            model_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            # Ưu tiên chọn model tốt nhất
            index_uu_tien = 0
            if 'models/gemini-1.5-flash' in model_list:
                index_uu_tien = model_list.index('models/gemini-1.5-flash')
            
            st.success(f"✅ Kết nối tốt! Tìm thấy {len(model_list)} bộ não AI.")
            
            # Cho phép bạn chọn Model (để không bao giờ bị lỗi 'Not Found')
            selected_model = st.selectbox("2. Chọn bộ não AI (Khuyên dùng 1.5-flash):", model_list, index=index_uu_tien)
            
        except Exception as e:
            st.error(f"Lỗi Key: {e}")

    st.markdown("---")
    st.header("👤 HỌC SINH")
    ten_hs = st.text_input("Họ tên:", "Lò Văn Páo")
    lop = st.selectbox("Lớp:", ["Lớp 1", "Lớp 2", "Lớp 3", "Lớp 4", "Lớp 5"])

# --- HÀM XỬ LÝ ---
def ai_soan_bai(model_name, mon, lop, chu_de, nang_luc):
    prompt = f"""
    Bạn là giáo viên tiểu học tại Điện Biên. Soạn phiếu bài tập môn {mon} lớp {lop}.
    Chủ đề: {chu_de} (Sách Kết nối tri thức).
    Học sinh: {nang_luc}. 
    Yêu cầu: Viết văn bản thuần (không Markdown). Gồm: 1. Mục tiêu. 2. Bài tập (2 câu ví dụ bản làng/nương rẫy). 3. Gợi ý.
    """
    try:
        # Sử dụng đúng cái tên bạn đã chọn trong danh sách
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Lỗi AI: {str(e)}"

def ai_cham_bai(model_name, image, mon, lop):
    prompt = f"Chấm bài {mon} lớp {lop}. Đọc chữ viết tay, chấm điểm và nhận xét khích lệ."
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"Lỗi Vision: {str(e)}"

def tao_file_word(ten, noi_dung):
    doc = Document()
    doc.add_heading(f'PHIẾU BÀI TẬP: {ten.upper()}', 0)
    doc.add_paragraph(noi_dung)
    doc.add_paragraph('\n--- Smart-Print AI Điện Biên ---')
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- GIAO DIỆN CHÍNH ---
st.title("🏫 Smart-Print AI: Phiên bản Tự Động")

if not api_key:
    st.info("👈 Vui lòng nhập API Key ở cột bên trái để bắt đầu.")
    st.stop()

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
        with st.spinner("Đang soạn thảo..."):
            if selected_model:
                ket_qua = ai_soan_bai(selected_model, mon_hoc, lop, bai_hoc, hoc_luc)
                st.success("Xong!")
                st.text_area("Nội dung:", ket_qua, height=300)
                file_doc = tao_file_word(ten_hs, ket_qua)
                st.download_button("📥 Tải Word", file_doc, "Phieu_Bai_Tap.docx")
            else:
                st.error("Chưa chọn được Model AI.")

with tab2:
    uploaded_file = st.file_uploader("Tải ảnh bài làm", type=['jpg', 'png', 'jpeg'])
    if uploaded_file and st.button("✨ CHẤM BÀI"):
        with st.spinner("Đang chấm..."):
             image = Image.open(uploaded_file)
             st.image(image, width=300)
             if selected_model:
                ket_qua = ai_cham_bai(selected_model, image, mon_hoc, lop)
                st.write(ket_qua)
