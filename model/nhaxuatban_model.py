from csdl import get_connection

# Lấy danh sách Nhà Xuất Bản
def getnxb():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT * FROM NhaXuatBan
        """

        cursor.execute(query)
        nxbs = cursor.fetchall()
        return nxbs

    except Exception as e:
        print("Lỗi khi truy vấn dữ liệu từ cơ sở dữ liệu:", e)
        return None

    finally:
        if conn:
            conn.close()


# Thêm Nhà Xuất Bản
def them_nxb_new(txtmaNXB, txttenNXB, txtghiChu):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Kiểm tra mã loại sách đã tồn tại
        check_query = "SELECT COUNT(*) FROM NhaXuatBan WHERE MaNXB = ?"
        cursor.execute(check_query, (txtmaNXB,))
        if cursor.fetchone()[0] > 0:
            return "Mã nxb đã tồn tại"

        # Nếu không tồn tại, thực hiện thêm mới
        query = """
        INSERT INTO NhaXuatBan (MaNXB, TenNXB, GhiChu)
        VALUES (?, ?, ?)
        """
        cursor.execute(query, (txtmaNXB, txttenNXB, txtghiChu))

        conn.commit()
        return "Thêm nxb thành công!"

    except Exception as e:
        print("Lỗi khi thêm dữ liệu vào cơ sở dữ liệu:", e)
        return "Lỗi khi thêm loại sách"

    finally:
        if conn:
            conn.close()

# Sửa Nhà Xuất Bản
def sua_nxb_new(txtmaNXB, txttenNXB, txtghiChu):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        UPDATE NhaXuatBan
        SET TenNXB = ?, GhiChu = ?
        WHERE MaNXB = ?
        """

        cursor.execute(query, (txttenNXB, txtghiChu, txtmaNXB))
        conn.commit()
        print("Cập nhật nxb thành công!")

    except Exception as e:
        print("Lỗi khi cập nhật dữ liệu trong cơ sở dữ liệu:", e)

    finally:
        if conn:
            conn.close()

# Xóa Nhà Xuất Bản
def xoa_nxb_new(txtmaNXB):

    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "DELETE FROM NhaXuatBan WHERE MaNXB = ?"
        cursor.execute(query, (txtmaNXB,))

        conn.commit()  # Commit the transaction
        return "Xóa nxb thành công!"

    except Exception as e:
        # Kiểm tra lỗi liên quan đến ràng buộc khóa ngoại
        if "foreign key constraint" in str(e).lower():
            return "Loại sách hiện đang được sử dụng trong bảng Sách, không thể xóa."
        else:
            print("Lỗi khi xóa dữ liệu từ cơ sở dữ liệu:", e)
            return "Xóa không thành công do tồn tại nha xuat ban trong bảng sách."

    finally:
        if conn:
            conn.close()

