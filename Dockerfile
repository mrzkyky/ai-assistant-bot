# Gunakan image python ringan 
FROM python:3.12-slim

# Mengatur direktori kerja
WORKDIR /app

# Copy file yang dibutuhkan 
COPY . .

# Install dependensi
RUN pip install --no-cache-dir -r requirements.txt

# Jalankan bot
CMD ["python3", "-m", "app.bot"]
