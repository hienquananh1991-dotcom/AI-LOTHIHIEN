import streamlit as st
import time
import random

# --- 1. CẤU HÌNH TRANG WEB ---
st.set_page_config(page_title="Smart-Print AI Điện Biên", page_icon="📚", layout="wide")

# --- 2. GIAO DIỆN TIÊU ĐỀ ---
st.title("📚 Smart-Print AI: Trợ Lý Soạn Bài")
st.markdown("**Bộ sách:** Kết nối tri thức với cuộc sống | **Địa phương:** Tỉnh Điện Biên")
st.markdown("---")

# --- 3. CỘT NHẬP LIỆU (BÊN TRÁI) ---
with st.sidebar:
    st.header("🛠️ Thiết lập bài tập")
    
    # Nhập thông tin học sinh
    ten_hs = st.text_input("Họ và tên học sinh", "Lò Thị Mai")
    lop = st.selectbox("Khối lớp", ["Lớp 1", "Lớp 2", "Lớp 3", "Lớp 4", "Lớp 5"])
    
    # CHỌN MÔN HỌC (MỚI)
    mon_hoc = st.selectbox(
        "Chọn môn học", 
        ["Toán", "Tiếng Việt", "Tiếng Anh", "Tự nhiên & Xã hội", "Khoa học", "Lịch sử & Địa lý", "Đạo đức"]
    )
    
    hoc_luc = st.radio("Năng lực hiện tại", ["Cần cố gắng (Yếu)", "Đạt (Trung bình)", "Tốt (Giỏi)"])
    
    van_de = st.text_area("Ghi chú/Vấn đề cần hỗ trợ", 
                          "Em đọc còn ngọng vần 'anh' và 'ăn'. Thích tìm hiểu về cây cối.")
    
    st.markdown("---")
    btn_tao = st.button("🚀 TẠO PHIẾU BÀI TẬP", type="primary")

# --- 4. PHẦN XỬ LÝ VÀ HIỂN THỊ (BÊN PHẢI) ---
if btn_tao:
    # Hiệu ứng chờ AI xử lý
    with st.spinner(f'AI đang tham khảo sách "Kết nối tri thức" môn {mon_hoc} cho em {ten_hs}...'):
        time.sleep(1.5) 
    
    # --- LOGIC GIẢ LẬP NỘI DUNG THEO MÔN (DEMO) ---
    # Phần này mô phỏng cách AI tạo nội dung dựa trên môn học và học lực
    
    loi_chao = f"Chào {ten_hs}! Cùng thầy cô khám phá bài học thú vị hôm nay nhé."
    noi_dung_bai = ""
    loi_khuyen = ""

    # 1. MÔN TOÁN
    if mon_hoc == "Toán":
        if "Yếu" in hoc_luc:
            noi_dung_bai = """**Bài 1:** Đặt tính rồi tính (Làm cẩn thận nhé):
   15 + 4 = ?      28 - 5 = ?
   
**Bài 2:** Mẹ đi chợ phiên mua 10 quả trứng, mua thêm 5 quả nữa. Hỏi mẹ có tất cả bao nhiêu quả?"""
            loi_khuyen = "Gợi ý: 'Thêm' là làm phép cộng. Em dùng que tính để đếm nhé."
        else: # Giỏi
            noi_dung_bai = """**Bài 1:** Tính nhanh: 15 + 27 + 5 + 3 = ?
            
**Bài 2 (Tư duy):** Bố trồng cây quế. Hàng thứ nhất trồng 5 cây, hàng thứ hai trồng gấp đôi hàng thứ nhất. Hỏi cả hai hàng có bao nhiêu cây?"""
            loi_khuyen = "Gợi ý: Gấp đôi là nhân 2. Sau đó cộng tổng hai hàng lại."

    # 2. MÔN TIẾNG VIỆT
    elif mon_hoc == "Tiếng Việt":
        noi_dung_bai = f"""**Bài 1: Luyện đọc và sửa lỗi chính tả**
Đọc đoạn văn sau và gạch chân dưới từ chứa vần 'anh' hoặc 'ăn':
"Cánh đồng Mường Thanh lúa chín vàng óng. Các bạn nhỏ rủ nhau ra ngắm cảnh đẹp quê hương."

**Bài 2: Tập làm văn**
{ten_hs} hãy viết 2-3 câu kể về một loài hoa ở bản mình (Ví dụ: Hoa Ban, Hoa Đào)."""
        loi_khuyen = "Lưu ý: Nhớ viết hoa chữ cái đầu câu và tên riêng (Mường Thanh) nhé."

    # 3. MÔN TIẾNG ANH
    elif mon_hoc == "Tiếng Anh":
        noi_dung_bai = """**Task 1: Vocabulary (Từ vựng)**
Nối từ tiếng Anh với nghĩa tiếng Việt tương ứng:
1. Hello          a. Quả táo
2. Apple          b. Xin chào
3. School         c. Trường học

**Task 2: Sentence (Mẫu câu)**
Hoàn thành câu sau: "My name is _______." (Tên tôi là...)"""
        loi_khuyen = "Hãy đọc to từ tiếng Anh lên khi làm bài nhé!"

    # 4. TỰ NHIÊN XÃ HỘI / KHOA HỌC
    elif mon_hoc in ["Tự nhiên & Xã hội", "Khoa học"]:
        noi_dung_bai = """**Câu 1:** Em hãy quan sát xung quanh nhà hoặc trường học.
Kể tên 3 con vật hoặc cây cối mà em nhìn thấy.

**Câu 2:** Để giữ gìn vệ sinh bản làng, chúng ta CẦN làm gì và KHÔNG NÊN làm gì?"""
        loi_khuyen = "Gợi ý: Không vứt rác bừa bãi, trồng thêm cây xanh..."

    # 5. CÁC MÔN KHÁC
    else:
        noi_dung_bai = """**Câu hỏi:** Em hãy kể về một việc làm tốt mà em đã làm trong tuần qua để giúp đỡ bố mẹ hoặc bạn bè.
        
**Hoạt động:** Hãy vẽ một bức tranh về chủ đề này vào mặt sau giấy nhé!"""
        loi_khuyen = "Hãy trung thực và chia sẻ thật lòng nhé."

    # --- HIỂN THỊ KẾT QUẢ RA MÀN HÌNH ---
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.success(f"✅ Đã soạn xong phiếu môn **{mon_hoc}**!")
        st.subheader(f"📄 PHIẾU BÀI TẬP: {ten_hs.upper()}")
        st.markdown(f"*Chủ đề: Bám sát SGK Kết nối tri thức - Tuần hiện tại*")
        
        container = st.container(border=True)
        container.write(f"**Lời nhắn:** {loi_chao}")
        container.markdown("---")
        container.code(noi_dung_bai, language=None)
        
    with col2:
        st.info("💡 **Góc Sư Phạm (AI Phân tích)**")
        st.write(f"**Học sinh:** {ten_hs}")
        st.write(f"**Điểm cần lưu ý:** {van_de}")
        st.warning(f"**Hướng dẫn riêng:** {loi_khuyen}")
        st.markdown("---")
        st.button("🖨️ Tải PDF để in", type="primary")

else:
    # Màn hình chờ
    st.info("👈 Mời thầy cô chọn Môn học và nhập thông tin học sinh ở cột bên trái.")
    st.write("---")
    st.caption("© 2024 Dự án Chuyển đổi số Giáo dục Điện Biên - Ứng dụng AI hỗ trợ dạy học.")
