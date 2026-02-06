import csv
import qrcode
import os
from PIL import Image, ImageDraw, ImageFont

# Cấu hình
csv_file = '10c8.csv'
output_folder = 'DS_QR_CODE'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Đọc file CSV (Thay thế Pandas)
try:
    with open(csv_file, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f) # Đọc dạng từ điển
        print("Đang tạo mã QR...")
        
        for row in reader:
            # Sửa tên cột khớp với file CSV của bạn
            ho_ten = row['Họ và Tên'] 
            ma_hs = row['Mã Học Sinh']
            
            qr_content = f"{ma_hs} - {ho_ten}"
            
            # --- Đoạn dưới này giữ nguyên như code cũ ---
            qr = qrcode.QRCode(box_size=10, border=4)
            qr.add_data(qr_content)
            qr.make(fit=True)
            
            img_qr = qr.make_image(fill_color="black", back_color="white").convert('RGB')
            
            # Vẽ tên (Code cũ)
            canvas_height = img_qr.height + 50
            new_image = Image.new('RGB', (img_qr.width, canvas_height), 'white')
            new_image.paste(img_qr, (0, 0))
            draw = ImageDraw.Draw(new_image)
            
            # Load font mặc định nếu lỗi
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except:
                font = ImageFont.load_default()

            text_bbox = draw.textbbox((0, 0), ho_ten, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_x = (new_image.width - text_width) / 2
            
            draw.text((text_x, img_qr.height + 10), ho_ten, fill="black", font=font)
            
            new_image.save(f"{output_folder}/{ma_hs}.png")
            print(f"Xong: {ma_hs}")
            
except Exception as e:
    print(f"Lỗi: {e}")
    print("Gợi ý: Hãy kiểm tra xem file .csv có nằm cùng thư mục code chưa?")