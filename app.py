import streamlit as st
import time
import random

# 1. CẤU HÌNH TRANG WEB
st.set_page_config(page_title="Smart-Print AI Điện Biên", page_icon="📚")

# 2. GIAO DIỆN TIÊU ĐỀ
st.title("📚 Smart-Print AI: Trợ Lý Soạn Bài")
st.write("Dành cho giáo viên vùng cao - Tỉnh Điện Biên")
st.markdown("---")

# 3. CỘT NHẬP LIỆU (BÊN TRÁI)
with st.sidebar:
    st.header("1. Nhập thông tin học sinh")
    ten_hs = st.text_input("Tên học sinh", "Vàng A Súa")
    lop = st.selectbox("Lớp", ["Lớp 1", "Lớp 2", "Lớp 3", "Lớp 4", "Lớp 5"])
    hoc_luc = st.radio("Mức độ", ["Yếu (Cần bổ trợ)", "Khá", "Giỏi (Nâng cao)"])
    van_de = st.text_area("Ghi chú đặc điểm/Lỗi sai", "Hay quên nhớ khi cộng. Thích đá bóng.")
    
    st.markdown("---")
    btn_tao = st.button("🚀 TẠO PHIẾU BÀI TẬP", type="primary")

# 4. PHẦN XỬ LÝ VÀ HIỂN THỊ (BÊN PHẢI)
if btn_tao:
    with st.spinner(f'AI đang soạn bài riêng cho em {ten_hs}...'):
        time.sleep(2) # Giả lập thời gian AI suy nghĩ
        
        # Tạo nội dung giả lập (Demo)
        if "Yếu" in hoc_luc:
            loi_chao = f"Thầy/Cô chào {ten_hs}! Cố lên nhé!"
            bai_tap = f"Bài 1: {ten_hs} có 5 quả cam, mẹ cho thêm 3 quả. Hỏi có tất cả bao nhiêu?\n\nBài 2: Đặt tính rồi tính: 15 + 4 = ?"
            loi_khuyen = "Gợi ý: Em nhớ dùng que tính để đếm nhé."
        else:
            loi_chao = f"Chào {ten_hs}! Hôm nay thử sức với bài toán khó nhé!"
            bai_tap = "Bài 1: Tìm quy luật dãy số: 2, 4, 8, 16, ...\n\nBài 2: Một đàn trâu có số chân là 16. Hỏi có bao nhiêu con trâu?"
            loi_khuyen = "Gợi ý: Hãy dùng phép nhân hoặc chia."

        # Hiển thị ra màn hình
        st.success("✅ Đã soạn xong!")
        st.header(f"📄 PHIẾU BÀI TẬP: {ten_hs.upper()}")
        
        st.info(f"💌 **Lời nhắn:** {loi_chao}")
        
        container = st.container(border=True)
        container.write("**Nội dung bài tập:**")
        container.code(bai_tap, language=None)
        container.warning(loi_khuyen)
        
        st.button("🖨️ Tải xuống PDF (Bản Demo)")

else:
    st.info("👈 Mời thầy cô nhập thông tin bên tay trái để bắt đầu.")
    st.image("https://media.istockphoto.com/id/1356366363/vector/school-children-in-classroom.jpg?s=612x612&w=0&k=20&c=XUuYkK1bMvOaN9TjQyJc7iYxKz8h5qWnE2_f1Q4Zl8=", caption="Lớp học vùng cao")
