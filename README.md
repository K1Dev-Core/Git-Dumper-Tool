# Git Dumper Tool

เครื่องมือสำหรับดึงข้อมูลจาก Git repository ที่เปิดเผยผ่านเว็บไซต์

## การติดตั้ง

### 1. ติดตั้ง Python
- ดาวน์โหลด Python จาก [python.org](https://www.python.org/downloads/)
- เลือกเวอร์ชัน 3.6 หรือใหม่กว่า
- ติดตั้งโดยทำตามขั้นตอนในตัวติดตั้ง

### 2. ติดตั้งไลบรารีที่จำเป็น
เปิด Command Prompt หรือ PowerShell แล้วรันคำสั่ง:

```bash
pip install requests
```

## วิธีการใช้งาน

### 1. เปลี่ยน URL เป้าหมาย
เปิดไฟล์ `app.py` และแก้ไขบรรทัดที่ 4:

```python
BASE = "http://0.0.0.0/.git/"   # เปลี่ยนเป็น URL ที่ต้องการ
```

### 2. รันโปรแกรม
เปิด Command Prompt หรือ PowerShell ในโฟลเดอร์ที่มีไฟล์ `app.py` แล้วรัน:

```bash
python app.py
```

### 3. ดูผลลัพธ์
- โปรแกรมจะสร้างโฟลเดอร์ `git_dump` 
- ไฟล์ทั้งหมดจะถูกบันทึกใน `git_dump/blobs/`
- ดูข้อความในหน้าจอเพื่อติดตามความคืบหน้า

## ตัวอย่างการใช้งาน

```bash
# เปลี่ยน URL ในไฟล์ app.py ก่อน
# จาก: BASE = "http://0.0.0.0/.git/"
# เป็น: BASE = "http://example.com/.git/"

# รันโปรแกรม
python app.py

# ดูไฟล์ที่ดึงมา
dir git_dump\blobs
```

