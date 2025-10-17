# Troubleshooting - Backend Setup

## ❌ Lỗi: "uvicorn is not recognized"

### Nguyên nhân:
- `uvicorn` được cài vào user site-packages nhưng chưa có trong PATH
- Hoặc chưa cài đặt dependencies

### ✅ Giải pháp:

#### Option 1: Chạy qua Python module (Recommended)

```bash
cd c:\Users\tdat1\Demo_LoginResisterEvent\backend
python -m uvicorn app.main:app --reload
```

#### Option 2: Cài đặt lại dependencies

```bash
cd c:\Users\tdat1\Demo_LoginResisterEvent\backend
pip install -r requirements.txt
```

Sau đó thử lại:
```bash
python -m uvicorn app.main:app --reload
```

#### Option 3: Thêm Scripts folder vào PATH

1. Tìm Python Scripts folder:
   ```bash
   python -m site --user-site
   ```
   Output: `C:\Users\tdat1\AppData\Roaming\Python\Python313\site-packages`

2. Scripts folder sẽ là: `C:\Users\tdat1\AppData\Roaming\Python\Python313\Scripts`

3. Thêm vào PATH:
   - Windows Search → "Environment Variables"
   - System Properties → Environment Variables
   - User variables → Path → Edit
   - New → Paste: `C:\Users\tdat1\AppData\Roaming\Python\Python313\Scripts`
   - OK → OK

4. Restart terminal và thử:
   ```bash
   uvicorn app.main:app --reload
   ```

---

## ✅ Backend đang chạy thành công

Khi thấy output:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process [xxxxx]
INFO:     Application startup complete.
```

**Backend đã sẵn sàng!** ✅

### Kiểm tra:

Mở browser và truy cập:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Health check**: [http://localhost:8000/](http://localhost:8000/)

---

## ⚠️ Warning: "orm_mode has been renamed to from_attributes"

Đây chỉ là warning, không ảnh hưởng. Backend vẫn hoạt động bình thường.

Để fix (optional):

1. Mở `backend/app/schemas.py`
2. Tìm:
   ```python
   class Config:
       orm_mode = True
   ```
3. Thay bằng:
   ```python
   class Config:
       from_attributes = True
   ```

---

## 🚀 Commands thường dùng

### Start backend:
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### Start backend với host khác (cho physical device):
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0
```

### Start backend với port khác:
```bash
python -m uvicorn app.main:app --reload --port 8001
```

### Stop backend:
```
Ctrl + C
```

---

## 📝 Lưu vào Script

Tạo file `start_backend.bat` trong folder `backend`:

```batch
@echo off
cd /d %~dp0
python -m uvicorn app.main:app --reload
pause
```

Sau đó chỉ cần double-click file này để start backend!

---

## 🔍 Check PostgreSQL connection

Nếu backend không kết nối được database:

1. **Kiểm tra PostgreSQL đang chạy:**
   ```bash
   # Windows
   Get-Service -Name postgresql*
   ```

2. **Kiểm tra credentials trong `.env`:**
   ```
   DATABASE_URL=postgresql://demo_user:demouser01@localhost:5432/demo_app
   ```

3. **Test connection:**
   ```bash
   psql -U demo_user -d demo_app -h localhost
   # Password: demouser01
   ```

---

## ✅ Workflow hoàn chỉnh

```bash
# Terminal 1: Backend
cd c:\Users\tdat1\Demo_LoginResisterEvent\backend
python -m uvicorn app.main:app --reload

# Terminal 2: Emulator
flutter emulators --launch Pixel_7

# Terminal 3: Flutter App
cd c:\Users\tdat1\Demo_LoginResisterEvent\frontend\mobile
flutter run
```

---

**Backend đã sẵn sàng để test! 🎉**

Từ emulator hoặc web, truy cập:
- Android Emulator: `http://10.0.2.2:8000/docs`
- iOS Simulator / Web: `http://localhost:8000/docs`
- Physical Device: `http://192.168.x.x:8000/docs` (thay bằng IP máy bạn)
