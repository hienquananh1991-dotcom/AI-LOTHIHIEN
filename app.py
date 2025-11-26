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
    
    if api_key:
        try:
            genai.configure(api_key=api_key)
            # Kiểm tra thử kết nối ngay lập tức
            model_test = genai.GenerativeModel('gemini-1.5-flash')
            st.success("Kết nối thành công! ✅")
        except Exception as e:
            st.error(f"API Key chưa đúng hoặc lỗi mạng: {e}")

    st.markdown("---")
    st.header("👤 HỌC SINH")
    ten_hs = st.text_input("Họ tên:", "Lò Văn Páo")
    lop = st.selectbox("Lớp:", ["Lớp 1", "Lớp 2", "Lớp 3", "Lớp 4", "Lớp 5"])

# --- HÀM XỬ LÝ ---
def ai_soan_bai(mon, lop, chu_de, nang_luc):
    # Prompt chi tiết
    prompt = f"""
    Đóng vai giáo viên tiểu học soạn phiếu bài tập môn {mon} lớp {lop}.
    Chủ đề: {chu_de} (Sách Kết nối tri thức).
    Học sinh: {nang_luc}. Địa phương: Điện Biên.
    
    Yêu cầu đầu ra (Format văn bản thuần túy, không Markdown đậm nghiêng):
    1. MỤC TIÊU: (Trích SGK)
    2. BÀI TẬP: (3 câu hỏi tự luận/trắc nghiệm phù hợp năng lực. Dùng hình ảnh nương rẫy, bản làng làm ví dụ).
    3. GỢI Ý: (Hướng dẫn giải).
    """
    try:
        # Sử dụng model chuẩn quốc tế mới nhất
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # QUAN TRỌNG: Trả về lỗi chi tiết để debug
        return f"LỖI AI: {str(e)}"

def ai_cham_bai(image, mon, lop):
    prompt = f"Chấm bài {mon} lớp {lop}. Đọc chữ viết tay, kiểm tra đúng sai, chấm điểm trên 10 và nhận xét khích lệ học sinh."
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"LỖI VISION: {str(e)}"

def tao_file_word(ten, noi_dung):
    doc = Document()
    doc.add_heading(f'PHIẾU BÀI TẬP: {ten.upper()}', 0)
    doc.add_paragraph(noi_dung)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- GIAO DIỆN CHÍNH ---
st.title("🏫 Smart-Print AI: Kết Nối Tri Thức (Fix Lỗi)")

tab1, tab2 = st.tabs(["📝 SOẠN BÀI", "📷 CHẤM BÀI"])

with tab1:
    mon_hoc = st.selectbox("Môn học", ["Toán", "Tiếng Việt", "Tự nhiên Xã hội", "Khoa học", "Lịch sử & Địa lý", "Tin học", "Công nghệ", "Tiếng Anh", "Đạo đức", "Âm nhạc", "Mĩ thuật", "Thể dục"])
    bai_hoc = st.text_input("Tên bài học:", "Bài ôn tập cuối tuần")
    hoc_luc = st.radio("Mức độ:", ["Cơ bản", "Nâng cao"])
    
    if st.button("🚀 SOẠN BÀI"):
        if not api_key:
            st.warning("⚠️ Vui lòng nhập API Key trước!")
        else:
            with st.spinner("Đang kết nối AI..."):
                ket_qua = ai_soan_bai(mon_hoc, lop, bai_hoc, hoc_luc)
                
                # Kiểm tra xem có bị lỗi 404 không
                if "LỖI AI" in ket_qua:
                    st.error("⚠️ Hệ thống gặp lỗi kết nối AI:")
                    st.code(ket_qua)
                    st.info("Cách sửa: Hãy thực hiện BƯỚC 3 (Xóa App và tạo lại) trong hướng dẫn.")
                else:
                    st.success("Đã xong!")
                    st.text_area("Kết quả:", ket_qua, height=300)
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
                ket_qua = ai_cham_bai(img, mon_hoc, lop)
                st.write(ket_qua)
