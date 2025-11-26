import streamlit as st
import google.generativeai as genai
from docx import Document
from io import BytesIO
from PIL import Image

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(page_title="Smart-Print AI (Real)", page_icon="🧠", layout="wide")

# --- SIDEBAR: CÀI ĐẶT API KEY ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Google_Gemini_logo.svg/2560px-Google_Gemini_logo.svg.png", width=150)
    st.header("🔑 KẾT NỐI BỘ NÃO AI")
    # Thêm type='password' để ẩn key đi cho bảo mật
    api_key = st.text_input("Nhập Google API Key của bạn:", type="password", help="Lấy key tại aistudio.google.com")
    
    if api_key:
        genai.configure(api_key=api_key)
        st.success("Đã kết nối Google Gemini! 🟢")
    else:
        st.warning("Vui lòng nhập API Key để AI hoạt động.")

    st.markdown("---")
    st.header("👤 Hồ sơ học sinh")
    ten_hs = st.text_input("Họ tên", "Lò Văn Páo")
    lop = st.selectbox("Khối lớp", ["Lớp 1", "Lớp 2", "Lớp 3", "Lớp 4", "Lớp 5"])

# --- HÀM 1: AI SOẠN BÀI (Dùng gemini-pro cho ổn định) ---
def ai_soan_bai(mon, lop, chu_de, nang_luc):
    prompt = f"""
    Bạn là một chuyên gia giáo dục tiểu học Việt Nam, am hiểu tường tận bộ sách giáo khoa 'Kết nối tri thức với cuộc sống'.
    Nhiệm vụ: Soạn phiếu bài tập môn {mon} cho học sinh {lop}.
    
    Thông tin đầu vào:
    - Chủ đề/Bài học: {chu_de} (Thuộc sách Kết nối tri thức).
    - Năng lực học sinh: {nang_luc}.
    - Địa phương: Tỉnh Điện Biên (Học sinh dân tộc thiểu số).
    
    Yêu cầu đầu ra:
    1. Trích xuất Mục tiêu bài học (Yêu cầu cần đạt) chính xác theo sách giáo khoa.
    2. Nội dung bài tập:
       - Nếu học sinh Yếu: Bài tập cơ bản, nhiều ví dụ, ngôn ngữ đơn giản, gần gũi (ví dụ về nương rẫy, hoa ban, con trâu...).
       - Nếu học sinh Giỏi: Có câu hỏi vận dụng cao.
    3. Trình bày rõ ràng: Phần A (Kiến thức nhớ), Phần B (Bài tập), Phần C (Gợi ý).
    4. Không dùng các ký tự markdown phức tạp (*, #), hãy viết dạng văn bản thuần để dễ đưa vào Word.
    """
    
    try:
        # SỬA Ở ĐÂY: Dùng 'gemini-pro' thay vì '1.5-flash' để tránh lỗi
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Lỗi kết nối AI: {str(e)}"

# --- HÀM 2: AI CHẤM BÀI (VISION) ---
def ai_cham_bai(image, mon, lop):
    prompt = f"""
    Hãy đóng vai giáo viên chấm bài môn {mon} lớp {lop}.
    Nhiệm vụ:
    1. Nhìn vào hình ảnh bài làm của học sinh.
    2. Đọc nội dung chữ viết tay (OCR).
    3. Kiểm tra đúng/sai so với kiến thức chuẩn.
    4. Chấm điểm trên thang 10.
    5. Viết lời nhận xét chi tiết, ân cần, khích lệ.
    """
    
    try:
        # Với hình ảnh, chúng ta vẫn cần model 1.5 Flash.
        # Nhờ bước cập nhật requirements.txt, cái này sẽ chạy được.
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        # Nếu Flash vẫn lỗi, thử fallback về gemini-pro-vision (bản cũ)
        try:
             model_old = genai.GenerativeModel('gemini-pro-vision')
             response = model_old.generate_content([prompt, image])
             return response.text
        except:
             return f"Lỗi xử lý hình ảnh: {str(e)}"

# --- HÀM 3: TẠO FILE WORD ---
def tao_file_word(ten, lop, mon, noi_dung_ai):
    doc = Document()
    doc.add_heading(f'PHIẾU BÀI TẬP: {ten.upper()}', 0)
    doc.add_paragraph(f'Môn: {mon} - {lop}')
    doc.add_paragraph('Bộ sách: Kết nối tri thức với cuộc sống')
    doc.add_paragraph('-'*50)
    doc.add_paragraph(noi_dung_ai)
    doc.add_paragraph('\n')
    doc.add_paragraph('--- Smart-Print AI: Ứng dụng trí tuệ nhân tạo Điện Biên ---')
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- GIAO DIỆN CHÍNH ---
st.title("🏫 Smart-Print AI: Kết Nối Tri Thức")
st.caption("Phiên bản ổn định (Stable) - Tích hợp Google Gemini")

tab1, tab2 = st.tabs(["📝 TẠO PHIẾU BÀI TẬP", "📷 CHẤM BÀI (AI VISION)"])

# --- TAB 1: SOẠN BÀI ---
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        mon_hoc = st.selectbox("Môn học", 
            ["Toán", "Tiếng Việt", "Tiếng Anh", "Tin học", "Công nghệ", 
             "Khoa học", "Lịch sử & Địa lý", "Đạo đức", "Tự nhiên & Xã hội"])
        bai_hoc = st.text_input("Tên bài học (Ví dụ: Bài 5 - Phép cộng có nhớ)", "Bài 10: Làm quen với máy tính")
    
    with col2:
        hoc_luc = st.radio("Mức độ đề bài", ["Cơ bản (Dành cho HS yếu)", "Trung bình", "Nâng cao (Dành cho HS giỏi)"])
        st.write("")
        btn_soan = st.button("🚀 AI SOẠN BÀI NGAY", type="primary")

    if btn_soan:
        if not api_key:
            st.error("⚠️ Vui lòng nhập API Key ở cột bên trái trước!")
        else:
            with st.spinner("AI đang đọc sách và soạn bài..."):
                noi_dung_ai = ai_soan_bai(mon_hoc, lop, bai_hoc, hoc_luc)
                st.success("✅ Đã soạn xong!")
                with st.expander("👀 Xem trước nội dung"):
                    st.write(noi_dung_ai)
                
                file_word = tao_file_word(ten_hs, lop, mon_hoc, noi_dung_ai)
                st.download_button("📥 TẢI PHIẾU WORD (.docx)", file_word, f"{ten_hs}_{mon_hoc}.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")

# --- TAB 2: CHẤM BÀI ---
with tab2:
    st.info("Chụp ảnh bài làm của học sinh và tải lên. AI sẽ chấm điểm.")
    uploaded_file = st.file_uploader("Tải ảnh bài làm...", type=['jpg', 'png', 'jpeg'])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption='Bài làm học sinh', width=400)
        
        if st.button("✨ AI CHẤM BÀI"):
            if not api_key:
                st.error("⚠️ Chưa có API Key!")
            else:
                with st.spinner("AI đang chấm điểm..."):
                    ket_qua_cham = ai_cham_bai(image, mon_hoc, lop)
                    st.markdown("### 📝 KẾT QUẢ")
                    st.write(ket_qua_cham)
                    st.balloons()

st.markdown("---")
st.caption("Powered by Google Gemini Pro")
