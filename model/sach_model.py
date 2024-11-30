from csdl import get_connection

def getsach():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT * FROM Sach
        """
        
        cursor.execute(query)
        sachs = cursor.fetchall()
        return sachs

    except Exception as e:
        print("Lỗi khi truy vấn dữ liệu từ cơ sở dữ liệu:", e)
        return None

    finally:
        if conn:
            conn.close()


def them_sach_new(txtmaSach, txttenSach, txttacGia, txtnhaXuatBan, txtloaiSach, txtsoTrang, txtgiaBan, txtsoLuong, txthinhAnh):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Kiểm tra mã sách đã tồn tại
        check_query = "SELECT COUNT(*) FROM Sach WHERE MaSach = ?"
        cursor.execute(check_query, (txtmaSach,))
        if cursor.fetchone()[0] > 0:
            return "Mã sách đã tồn tại"

        # Thêm sách mới
        query = """
            INSERT INTO Sach (MaSach,TenSach, MaTacGia, MaNXB, MaLoai, SoTrang, GiaBan, SoLuong, HinhAnh)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (txtmaSach, txttenSach, txttacGia, txtnhaXuatBan, txtloaiSach, txtsoTrang, txtgiaBan, txtsoLuong, txthinhAnh))
        conn.commit()
        return "Thêm sách thành công!"
    except Exception as e:
        print("Lỗi khi thêm sách vào cơ sở dữ liệu:", e)
        return "Lỗi khi thêm sách"
    finally:
        if conn:
            conn.close()

def sua_sach_new(txtmaSach, txttenSach, txttacGia, txtnhaXuatBan, txtloaiSach, txtsoTrang, txtgiaBan, txtsoLuong, txthinhAnh):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        UPDATE Sach
        SET TenSach = ?, MaTacGia = ?, MaNXB = ?, MaLoai = ?, SoTrang = ?, GiaBan = ?, SoLuong = ?, HinhAnh = ?
        WHERE MaSach = ?
        """

        cursor.execute(query, (txttenSach, txttacGia, txtnhaXuatBan, txtloaiSach, txtsoTrang, txtgiaBan, txtsoLuong, txthinhAnh, txtmaSach))
        conn.commit()
        print("Cập nhật sách thành công!")

    except Exception as e:
        print("Lỗi khi cập nhật dữ liệu trong cơ sở dữ liệu:", e)

    finally:
        if conn:
            conn.close()

def xoa_sach_new(txtmaSach):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "DELETE FROM Sach WHERE MaSach = ?"
        cursor.execute(query, (txtmaSach,))

        conn.commit()  # Commit the transaction
        return "Xóa sach thành công!"

    except Exception as e:
        # Kiểm tra lỗi liên quan đến ràng buộc khóa ngoại
        if "foreign key constraint" in str(e).lower():
            return "Loại sách hiện đang được sử dụng trong bảng Sách, không thể xóa."
        else:
            print("Lỗi khi xóa dữ liệu từ cơ sở dữ liệu:", e)
            return "Xóa không thành công do tồn tại tác giả trong bảng sách."

    finally:
        if conn:
            conn.close()