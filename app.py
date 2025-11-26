import streamlit as st
import time
import random
from docx import Document # Thư viện tạo file Word
from io import BytesIO    # Thư viện xử lý file trong bộ nhớ

# --- 1. CẤU HÌNH TRANG WEB ---
st.set_page_config(page_title="Smart-Print AI Điện Biên", page_icon="📚", layout="wide")

# --- HÀM TẠO FILE WORD (MỚI) ---
def tao_file_word(ten_hs, mon_hoc, lop, noi_dung, loi_khuyen):
    doc = Document()
    
    # Tiêu đề
    doc.add_heading(f'PHIẾU BÀI TẬP: {ten_hs.upper()}', 0)
    doc.add_paragraph(f'Môn: {mon_hoc} - {lop}')
    doc.add_paragraph('Bộ sách: Kết nối tri thức với cuộc sống')
    doc.add_paragraph('-'*50)
    
    # Nội dung
    doc.add_heading('A. NỘI DUNG BÀI TẬP', level=1)
    doc.add_paragraph(noi_dung)
    
    # Lời khuyên
    doc.add_heading('B. GÓC SƯ PHẠM (Gợi ý)', level=1)
    doc.add_paragraph(f"Lời khuyên cho {ten_hs}: {loi_khuyen}")
    
    # Footer
    doc.add_paragraph('\n')
    doc.add_paragraph('--- Sản phẩm hỗ trợ giáo dục vùng cao ---')

    # Lưu file vào bộ nhớ đệm (RAM) thay vì ổ cứng
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- 2. GIAO DIỆN ---
st.title("📚 Smart-Print AI: Trợ Lý Soạn Bài & Xuất File Word")
st.markdown("**Địa phương:** Tỉnh Điện Biên | **Tính năng:** Tải phiếu bài tập .docx")
st.markdown("---")

# --- 3. CỘT NHẬP LIỆU ---
with st.sidebar:
    st.header("🛠️ Thiết lập")
    ten_hs = st.text_input("Họ tên học sinh", "Lò Thị Mai")
    lop = st.selectbox("Khối lớp", ["Lớp 3", "Lớp 4", "Lớp 5"])
    
    mon_hoc = st.selectbox("Môn học", 
        ["Toán", "Tiếng Việt", "Tiếng Anh", "Tin học", "Công nghệ", "Tự nhiên & Xã hội"])
    
    hoc_luc = st.radio("Năng lực", ["Cần cố gắng", "Đạt", "Tốt"])
    btn_tao = st.button("🚀 TẠO PHIẾU BÀI TẬP", type="primary")

# --- 4. XỬ LÝ ---
if btn_tao:
    with st.spinner(f'Đang soạn thảo văn bản môn {mon_hoc}...'):
        time.sleep(1) # Giả lập chờ
        
        # --- NỘI DUNG GIẢ LẬP (Bạn có thể sửa lại nội dung này) ---
        if mon_hoc == "Toán":
            noi_dung_bai = "Bài 1: Đặt tính rồi tính:\n   3524 + 215 = ?\n   5620 - 140 = ?\n\nBài 2: Giải toán có lời văn..."
            loi_khuyen = "Hãy cẩn thận khi đặt tính hàng dọc."
        elif mon_hoc == "Tiếng Việt":
            noi_dung_bai = "Bài 1: Tìm từ ngữ chỉ sự vật trong câu sau...\n\nBài 2: Viết đoạn văn ngắn tả ngôi trường của em."
            loi_khuyen = "Chú ý lỗi chính tả dấu hỏi/ngã."
        elif mon_hoc == "Tin học":
            noi_dung_bai = "Câu 1: Kể tên các bộ phận của máy tính?\nCâu 2: Tư thế ngồi máy tính đúng là gì?"
            loi_khuyen = "Nhớ giữ khoảng cách mắt với màn hình."
        elif mon_hoc == "Công nghệ":
            noi_dung_bai = "Câu 1: Em hãy dùng lá cây làm một chiếc thuyền.\nCâu 2: Vẽ lại ý tưởng của em."
            loi_khuyen = "Cẩn thận khi dùng kéo."
        else:
            noi_dung_bai = "Câu hỏi ôn tập kiến thức đã học trong tuần.\nHãy ghi chép lại những điều em quan sát được."
            loi_khuyen = "Hãy quan sát kỹ thực tế."

    # --- HIỂN THỊ KẾT QUẢ ---
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.success("✅ Đã tạo xong! Xem trước bên dưới:")
        st.code(noi_dung_bai, language=None) # Xem trước nội dung
        
    with col2:
        st.info("⬇️ **Tải về máy tính**")
        st.write("File Word (.docx) giúp thầy cô dễ dàng chỉnh sửa và in ấn.")
        
        # TẠO FILE WORD ĐỂ TẢI
        file_word = tao_file_word(ten_hs, mon_hoc, lop, noi_dung_bai, loi_khuyen)
        
        # NÚT TẢI VỀ (DOWNLOAD BUTTON)
        st.download_button(
            label="📥 TẢI PHIẾU BÀI TẬP (.docx)",
            data=file_word,
            file_name=f"Phieu_Bai_Tap_{ten_hs}_{mon_hoc}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

else:
    st.info("👈 Mời thầy cô nhập thông tin và bấm nút TẠO để xuất file.")
