from csdl import get_connection

def getsinhvien():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT * FROM SinhVien
        """
        
        cursor.execute(query)
        sinhviens = cursor.fetchall()
        return sinhviens

    except Exception as e:
        print("Lỗi khi truy vấn dữ liệu từ cơ sở dữ liệu:", e)
        return None

    finally:
        if conn:
            conn.close()


def them_quan_lysinhvien(txtMaSV, txtTenSV, txtNganhHoc, txtKhoaHoc, txtSoDienThoai):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Kiểm tra mã loại sách đã tồn tại
        check_query = "SELECT COUNT(*) FROM SinhVien WHERE MaSV = ?"
        cursor.execute(check_query, (txtMaSV,))
        if cursor.fetchone()[0] > 0:
            return "Mã sinh vien đã tồn tại"

        check_query_sdt = "SELECT COUNT(*) FROM SinhVien WHERE SoDienThoai = ?"
        cursor.execute(check_query_sdt, (txtSoDienThoai,))
        if cursor.fetchone()[0] > 0:
            return "Số điện thoại đã được sử dụng"

        # Nếu không tồn tại, thực hiện thêm mới
        query = """
            INSERT INTO SinhVien (MaSV, TenSV, NganhHoc, KhoaHoc, SoDienThoai)
            VALUES (?, ?, ?, ?, ?)
            """
        cursor.execute(query, (txtMaSV, txtTenSV, txtNganhHoc, txtKhoaHoc, txtSoDienThoai))

        conn.commit()
        return "Thêm sinh vien thành công!"

    except Exception as e:
        print("Lỗi khi thêm dữ liệu vào cơ sở dữ liệu:", e)
        return "Lỗi khi thêm sinh vien"

    finally:
        if conn:
            conn.close()

def sua_quan_lysinhvien(txtMaSV, txtTenSV, txtNganhHoc, txtKhoaHoc, txtSoDienThoai):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        UPDATE SinhVien
        SET TenSV = ?, NganhHoc = ?, KhoaHoc = ?, SoDienThoai = ?
        WHERE MaSV = ?
        """

        cursor.execute(query, (txtTenSV, txtNganhHoc, txtKhoaHoc,txtSoDienThoai,txtMaSV))
        conn.commit()
        print("Cập nhật sinh vien thành công!")

    except Exception as e:
        print("Lỗi khi cập nhật dữ liệu trong cơ sở dữ liệu:", e)

    finally:
        if conn:
            conn.close()


def xoa_quan_lysinhvien(maSinhVien):

    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "DELETE FROM SinhVien WHERE MaSV = ?"
        cursor.execute(query, (maSinhVien,))

        conn.commit()  # Commit the transaction
        return "Xóa sinh vien thành công!"

    except Exception as e:
        # Kiểm tra lỗi liên quan đến ràng buộc khóa ngoại
        if "foreign key constraint" in str(e).lower():
            return "Sinh vien van dang muon sach, không thể xóa."
        else:
            print("Lỗi khi xóa dữ liệu từ cơ sở dữ liệu:", e)
            return "Xóa không thành công do tồn tại sinh vien trong bảng sách."

    finally:
        if conn:
            conn.close()
