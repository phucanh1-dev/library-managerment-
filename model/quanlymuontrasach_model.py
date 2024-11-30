from csdl import get_connection
from datetime import datetime

def getmuontrasach():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT MS.MaPhieuMuon, SV.MaSV, SV.TenSV, S.MaSach, S.TenSach, 
               FORMAT(MS.NgayMuon, 'dd/MM/yyyy') AS NgayMuon, 
               FORMAT(MS.NgayTra, 'dd/MM/yyyy') AS NgayTra, 
               MS.GhiChu
        FROM MuonTraSach MS
        JOIN Sach S ON S.MaSach = MS.MaSach
        JOIN SinhVien SV ON SV.MaSV = MS.MaSV
        """
        cursor.execute(query)
        muontrasachs = cursor.fetchall()
        print("Dữ liệu mượn trả sách đã được truy xuất với định dạng ngày.")
        return muontrasachs
    except Exception as e:
        print(f"Lỗi khi lấy dữ liệu mượn trả sách: {e}")
        return []
    finally:
        if conn:
            conn.close()


def muonsach(txtMaSV, txtMaSach, txtNgayMuon, txtNgayTra, txtGhiChu):
    try:
        conn = get_connection()
        if conn is None:
            print("Không thể kết nối đến cơ sở dữ liệu.")
            return "error: database connection failed"
        
        cursor = conn.cursor()

        # Kiểm tra số lượng phiếu mượn hiện tại của sinh viên
        print("Kiểm tra tổng số sách sinh viên đã mượn chưa trả...")
        query_check_borrowed = """
        SELECT COUNT(*) 
        FROM MuonTraSach 
        WHERE MaSV = ? 
        """
        cursor.execute(query_check_borrowed, (txtMaSV,))
        borrowed_count = cursor.fetchone()[0]

        # Nếu số lượng phiếu mượn chưa trả >= 3, từ chối mượn thêm
        if borrowed_count >= 3:
            print("Sinh viên đã mượn quá 3 cuốn sách chưa trả.")
            return "error: Sinh viên đã mượn quá 3 quyển sách chưa trả"

        # Kiểm tra số lượng sách còn trong thư viện
        print("Kiểm tra số lượng sách có sẵn...")
        query_check_book = """
        SELECT SoLuong 
        FROM Sach 
        WHERE MaSach = ?
        """
        cursor.execute(query_check_book, (txtMaSach,))
        result = cursor.fetchone()
        if not result or result[0] <= 0:
            print("Sách không còn sẵn để mượn.")
            return ":Lỗi: Sách không còn sẵn"

        # Thêm phiếu mượn vào bảng MuonTraSach
        print("Thêm phiếu mượn sách...")
        query_insert_loan = """
        INSERT INTO MuonTraSach (MaSV, MaSach, NgayMuon, NgayTra, GhiChu)
        VALUES (?, ?, ?, ?, ?)
        """ 
        ngay_muon_formatted = datetime.strptime(txtNgayMuon, "%d/%m/%Y").strftime("%Y-%m-%d")
        ngay_tra_formatted = datetime.strptime(txtNgayTra, "%d/%m/%Y").strftime("%Y-%m-%d") if txtNgayTra else None

        cursor.execute(query_insert_loan, (txtMaSV, txtMaSach, ngay_muon_formatted, ngay_tra_formatted, txtGhiChu))
        conn.commit()

        # Cập nhật số lượng sách
        print("Cập nhật số lượng sách còn lại...")
        query_update_books = """
        UPDATE Sach 
        SET SoLuong = SoLuong - 1 
        WHERE MaSach = ?
        """
        cursor.execute(query_update_books, (txtMaSach,))
        conn.commit()

        print("Mượn sách thành công.")
        return "thành công: cho mượn thành công"
    except Exception as e:
        print(f"Lỗi khi mượn sách: {e}")
        if conn:
            conn.rollback()
        return f"error: {e}"
    finally:
        if conn:
            conn.close()

def trasach(maPhieuMuon):
    try:
        conn = get_connection()
        if conn is None:
            print("Không thể kết nối đến cơ sở dữ liệu.")
            return "error: database connection failed"
        
        cursor = conn.cursor()

        # Lấy mã sách từ phiếu mượn
        query_get_book = "SELECT MaSach FROM MuonTraSach WHERE MaPhieuMuon = ?"
        cursor.execute(query_get_book, (maPhieuMuon,))
        result = cursor.fetchone()
        if not result:
            return "error: loan record not found"
        maSach = result[0]

        # Xóa phiếu mượn
        query_delete_loan = "DELETE FROM MuonTraSach WHERE MaPhieuMuon = ?"
        cursor.execute(query_delete_loan, (maPhieuMuon,))
        conn.commit()

        # Tăng số lượng sách
        query_update_book = "UPDATE Sach SET SoLuong = SoLuong + 1 WHERE MaSach = ?"
        cursor.execute(query_update_book, (maSach,))
        conn.commit()

        return "success: book returned"
    except Exception as e:
        conn.rollback()
        return f"error: {e}"
    finally:
        if conn:
            conn.close()

def giahan_ngaytra(maPhieuMuon, ngayTraMoi):
    try:
        conn = get_connection()
        if conn is None:
            return "error: database connection failed"
        
        cursor = conn.cursor()

        # Định dạng lại ngày từ DD/MM/YYYY sang định dạng chuẩn SQL
        ngayTraMoi_formatted = datetime.strptime(ngayTraMoi, "%d/%m/%Y").strftime("%Y-%m-%d")

        # Kiểm tra ngày mới phải lớn hơn ngày hiện tại
        today = datetime.now().strftime("%Y-%m-%d")
        if ngayTraMoi_formatted <= today:
            return "error: Ngày trả mới phải lớn hơn ngày hiện tại"

        # Cập nhật ngày trả trong bảng MuonTraSach
        query_update_date = """
        UPDATE MuonTraSach 
        SET NgayTra = ? 
        WHERE MaPhieuMuon = ?
        """
        cursor.execute(query_update_date, (ngayTraMoi_formatted, maPhieuMuon))
        conn.commit()

        return "success: gia hạn ngày trả thành công"
    except Exception as e:
        conn.rollback()
        return f"error: {e}"
    finally:
        if conn:
            conn.close()
