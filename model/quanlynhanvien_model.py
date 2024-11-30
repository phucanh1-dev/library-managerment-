from csdl import get_connection


def getnhanvien():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT * FROM NhanVien
        """

        cursor.execute(query)
        nhanviens = cursor.fetchall()
        return nhanviens

    except Exception as e:
        print("Lỗi khi truy vấn dữ liệu từ cơ sở dữ liệu:", e)
        return None

    finally:
        if conn:
            conn.close()


def them_quan_lynhanien(txtMaNhanVien, txtTenNhanVien, txtSoDienThoai, txtGioiTinh, txtDiaChi, txtMatkhau, txtVaiTro):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Kiểm tra mã loại sách đã tồn tại
        check_query = "SELECT COUNT(*) FROM NhanVien WHERE MaNhanVien = ?"
        cursor.execute(check_query, (txtMaNhanVien))
        if cursor.fetchone()[0] > 0:
            return "Mã nhan vien đã tồn tại"


        check_query_sdt = "SELECT COUNT(*) FROM NhanVien WHERE SoDienThoai = ?"
        cursor.execute(check_query_sdt, (txtSoDienThoai,))
        if cursor.fetchone()[0] > 0:
            return "Số điện thoại đã được sử dụng"


        # Nếu không tồn tại, thực hiện thêm mới
        query = """
            INSERT INTO NhanVien (MaNhanVien, TenNhanVien, SoDienThoai, GioiTinh, DiaChi, MatKhau, VaiTro)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
        cursor.execute(query, (txtMaNhanVien, txtTenNhanVien, txtSoDienThoai, txtGioiTinh, txtDiaChi, txtMatkhau, txtVaiTro))

        conn.commit()
        return "Thêm nhan vien thành công!"

    except Exception as e:
        print("Lỗi khi thêm dữ liệu vào cơ sở dữ liệu:", e)
        return "Lỗi khi thêm nhan vien"

    finally:
        if conn:
            conn.close()

def sua_quan_lynhanvien(txtMaNhanVien, txtTenNhanVien, txtSoDienThoai, txtGioiTinh, txtDiaChi, txtMatkhau, txtVaiTro):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        UPDATE NhanVien
        SET TenNhanVien = ?, SoDienThoai = ?, GioiTinh = ?, DiaChi = ?, MatKhau = ?, VaiTro = ?
        WHERE MaNhanVien = ?
        """

        cursor.execute(query, (txtTenNhanVien, txtSoDienThoai, txtGioiTinh, txtDiaChi, txtMatkhau, txtVaiTro, txtMaNhanVien))
        conn.commit()
        print("Cập nhật nhan vien thành công!")

    except Exception as e:
        print("Lỗi khi cập nhật dữ liệu trong cơ sở dữ liệu:", e)

    finally:
        if conn:
            conn.close()


def xoa_quan_lynhanvien(maNhanVien):

    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "DELETE FROM NhanVien WHERE MaNhanVien = ?"
        cursor.execute(query, (maNhanVien,))

        conn.commit()  # Commit the transaction
        return "Xóa nhan vien thành công!"

    except Exception as e:
        # Kiểm tra lỗi liên quan đến ràng buộc khóa ngoại
        if "foreign key constraint" in str(e).lower():
            return "nhan vien van dang di lam, không thể xóa."
        else:
            print("Lỗi khi xóa dữ liệu từ cơ sở dữ liệu:", e)
            return "Xóa không thành công do tồn tại sinh vien trong bảng sách."

    finally:
        if conn:
            conn.close()



def check_login(phone, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MaNhanVien, TenNhanVien, VaiTro FROM NhanVien WHERE SoDienThoai = ? AND MatKhau = ?", (phone, password))
    user = cursor.fetchone()
    return user
