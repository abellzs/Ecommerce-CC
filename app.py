from flask import Flask, render_template_string, request, redirect, url_for
import pymysql
import sys
from datetime import datetime
import boto3
import uuid
import requests  # Tambahkan import untuk library requests
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os

app = Flask(__name__)


# Load environment variables from .env file
load_dotenv()

# Konfigurasi AWS S3
AWS_REGION = os.getenv('AWS_REGION')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

s3 = boto3.client(
    's3',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# Fungsi untuk koneksi ke database
def get_db_connection():
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")

# Route untuk halaman utama
@app.route('/')
def home():
    try:
        # Dapatkan koneksi database
        db = get_db_connection()
        if not db:
            return "<h1>Error koneksi database</h1>"
            
        cursor = db.cursor()
        # Ambil data produk (termasuk ID untuk delete)
        cursor.execute("SELECT id, name, price, image_url FROM products")
        products = cursor.fetchall()
        cursor.close()
        db.close()
        
        # Developer info
        developer_name = "Mochamad Abel Avriyana Savero"
        developer_nrp = "152022141"
        
        html = '''
        <!DOCTYPE html>
        <html lang="id">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>ECOMMERCE ABENG</title>
            <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
            <style>
                :root {
                    --primary: #4f46e5;
                    --primary-dark: #3730a3;
                    --secondary: #6366f1;
                    --accent: #ec4899;
                    --dark: #111827;
                    --light: #f9fafb;
                    --gray: #6b7280;
                    --success: #10b981;
                    --danger: #ef4444;
                    --warning: #f59e0b;
                    --info: #3b82f6;
                    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
                    --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
                }
                
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                
                body {
                    font-family: 'Poppins', sans-serif;
                    background-color: #f3f4f6;
                    color: var(--dark);
                    line-height: 1.6;
                }
                
                /* Navbar */
                .navbar {
                    background-color: white;
                    padding: 1rem 0;
                    box-shadow: var(--shadow);
                    position: sticky;
                    top: 0;
                    z-index: 100;
                }
                
                .container {
                    width: 90%;
                    max-width: 1200px;
                    margin: 0 auto;
                }
                
                .navbar-container {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                
                .brand {
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                }
                
                .logo {
                    font-size: 1.5rem;
                    font-weight: 700;
                    color: var(--primary);
                    text-decoration: none;
                }
                
                .nav-menu {
                    display: flex;
                    gap: 1.5rem;
                }
                
                .nav-link {
                    color: var(--dark);
                    text-decoration: none;
                    font-weight: 500;
                    transition: color 0.2s;
                    display: flex;
                    align-items: center;
                    gap: 0.3rem;
                }
                
                .nav-link:hover {
                    color: var(--primary);
                }
                
                .user-actions {
                    display: flex;
                    align-items: center;
                    gap: 1rem;
                }
                
                .action-btn {
                    background: none;
                    border: none;
                    color: var(--dark);
                    font-size: 1.25rem;
                    cursor: pointer;
                    transition: color 0.2s;
                }
                
                .action-btn:hover {
                    color: var(--primary);
                }
                
                .add-btn {
                    background-color: var(--primary);
                    color: white;
                    border: none;
                    padding: 0.5rem 1rem;
                    border-radius: 0.375rem;
                    font-weight: 500;
                    text-decoration: none;
                    display: inline-flex;
                    align-items: center;
                    gap: 0.5rem;
                    transition: background-color 0.2s;
                    font-size: 0.875rem;
                }
                
                .add-btn:hover {
                    background-color: var(--primary-dark);
                }
                
                /* Hero Banner */
                .hero {
                    background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('https://images.unsplash.com/photo-1607082350899-7e105aa886ae?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80') no-repeat center/cover;
                    padding: 5rem 0;
                    text-align: center;
                    color: white;
                    margin-bottom: 3rem;
                }
                
                .hero-content {
                    max-width: 800px;
                    margin: 0 auto;
                }
                
                .hero h1 {
                    font-size: 2.5rem;
                    font-weight: 700;
                    margin-bottom: 1rem;
                    line-height: 1.2;
                }
                
                .hero p {
                    font-size: 1.125rem;
                    margin-bottom: 2rem;
                    opacity: 0.9;
                }
                
                .developer-info {
                    background-color: rgba(255, 255, 255, 0.1);
                    padding: 0.5rem 1rem;
                    border-radius: 0.375rem;
                    display: inline-block;
                    margin-bottom: 1rem;
                    font-size: 0.875rem;
                }
                
                /* Section Heading */
                .section-heading {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 2rem;
                }
                
                .section-title {
                    font-size: 1.5rem;
                    font-weight: 600;
                    color: var(--dark);
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                }
                
                /* Product Grid */
                .product-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
                    gap: 2rem;
                    margin-bottom: 4rem;
                }
                
                .product-card {
                    background-color: white;
                    border-radius: 0.5rem;
                    overflow: hidden;
                    box-shadow: var(--shadow);
                    transition: transform 0.3s, box-shadow 0.3s;
                    position: relative;
                }
                
                .product-card:hover {
                    transform: translateY(-5px);
                    box-shadow: var(--shadow-lg);
                }
                
                .product-badge {
                    position: absolute;
                    top: 1rem;
                    left: 1rem;
                    background-color: var(--primary);
                    color: white;
                    padding: 0.25rem 0.75rem;
                    border-radius: 2rem;
                    font-size: 0.75rem;
                    font-weight: 500;
                    text-transform: uppercase;
                    z-index: 10;
                }
                
                .product-img-wrapper {
                    position: relative;
                    height: 200px;
                    overflow: hidden;
                }
                
                .product-img {
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                    transition: transform 0.5s;
                }
                
                .product-card:hover .product-img {
                    transform: scale(1.05);
                }
                
                .product-overlay {
                    position: absolute;
                    inset: 0;
                    background-color: rgba(0, 0, 0, 0.2);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 0.5rem;
                    opacity: 0;
                    transition: opacity 0.3s;
                }
                
                .product-card:hover .product-overlay {
                    opacity: 1;
                }
                
                .overlay-btn {
                    width: 2.5rem;
                    height: 2.5rem;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    background-color: white;
                    color: var(--dark);
                    border-radius: 50%;
                    border: none;
                    cursor: pointer;
                    transition: background-color 0.2s, color 0.2s, transform 0.2s;
                }
                
                .overlay-btn:hover {
                    background-color: var(--primary);
                    color: white;
                    transform: scale(1.1);
                }
                
                .product-content {
                    padding: 1.25rem;
                }
                
                .product-name {
                    font-size: 1.125rem;
                    font-weight: 600;
                    color: var(--dark);
                    margin-bottom: 0.5rem;
                }
                
                .product-meta {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    margin-top: 1rem;
                }
                
                .product-price {
                    font-size: 1.25rem;
                    font-weight: 700;
                    color: var(--primary);
                }
                
                .action-buttons {
                    display: flex;
                    gap: 0.5rem;
                }
                
                .action-buttons a {
                    text-decoration: none;
                }
                
                .cart-btn, .delete-btn {
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    width: 2rem;
                    height: 2rem;
                    border-radius: 0.375rem;
                    border: none;
                    cursor: pointer;
                    transition: background-color 0.2s;
                }
                
                .cart-btn {
                    background-color: var(--success);
                    color: white;
                }
                
                .cart-btn:hover {
                    background-color: #0e9f6e;
                }
                
                .delete-btn {
                    background-color: var(--danger);
                    color: white;
                }
                
                .delete-btn:hover {
                    background-color: #dc2626;
                }
                
                /* Features Section */
                .features {
                    background-color: white;
                    padding: 4rem 0;
                    margin-bottom: 3rem;
                }
                
                .features-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 2rem;
                }
                
                .feature-card {
                    text-align: center;
                    padding: 2rem;
                    border-radius: 0.5rem;
                    background-color: var(--light);
                    transition: transform 0.3s;
                }
                
                .feature-card:hover {
                    transform: translateY(-5px);
                }
                
                .feature-icon {
                    width: 4rem;
                    height: 4rem;
                    background-color: var(--primary);
                    color: white;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin: 0 auto 1.5rem;
                    font-size: 1.5rem;
                }
                
                .feature-title {
                    font-size: 1.25rem;
                    font-weight: 600;
                    margin-bottom: 0.75rem;
                }
                
                .feature-desc {
                    color: var(--gray);
                    font-size: 0.875rem;
                }
                
                /* Footer */
                footer {
                    background-color: var(--dark);
                    color: white;
                    padding: 3rem 0 1.5rem;
                }
                
                .footer-content {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 2rem;
                    margin-bottom: 2rem;
                }
                
                .footer-column h3 {
                    font-size: 1.25rem;
                    font-weight: 600;
                    margin-bottom: 1.5rem;
                    color: white;
                }
                
                .footer-links {
                    list-style: none;
                }
                
                .footer-links li {
                    margin-bottom: 0.75rem;
                }
                
                .footer-links a {
                    color: #e5e7eb;
                    text-decoration: none;
                    transition: color 0.2s;
                }
                
                .footer-links a:hover {
                    color: white;
                }
                
                .footer-text {
                    color: #e5e7eb;
                    margin-bottom: 1.5rem;
                    font-size: 0.875rem;
                }
                
                .social-links {
                    display: flex;
                    gap: 0.75rem;
                }
                
                .social-link {
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    width: 2.5rem;
                    height: 2.5rem;
                    border-radius: 50%;
                    background-color: rgba(255, 255, 255, 0.1);
                    color: white;
                    transition: background-color 0.2s;
                    text-decoration: none;
                }
                
                .social-link:hover {
                    background-color: var(--primary);
                }
                
                .footer-bottom {
                    text-align: center;
                    padding-top: 1.5rem;
                    border-top: 1px solid rgba(255, 255, 255, 0.1);
                    color: #9ca3af;
                    font-size: 0.875rem;
                }
                
                .developer {
                    font-weight: 600;
                    color: white;
                }
                
                /* Responsive */
                @media (max-width: 768px) {
                    .nav-menu, .developer-info span {
                        display: none;
                    }
                    
                    .hero h1 {
                        font-size: 2rem;
                    }
                    
                    .product-grid {
                        grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
                        gap: 1rem;
                    }
                    
                    .features-grid {
                        grid-template-columns: 1fr;
                    }
                }
            </style>
        </head>
        <body>
            <!-- Navbar -->
            <nav class="navbar">
                <div class="container navbar-container">
                    <div class="brand">
                        <a href="/" class="logo">ABENGSHOP</a>
                    </div>
                    
                    <ul class="nav-menu">
                        <li><a href="/" class="nav-link"><i class="fas fa-home"></i> Beranda</a></li>
                        <li><a href="#products" class="nav-link"><i class="fas fa-shopping-bag"></i> Produk</a></li>
                        <li><a href="#features" class="nav-link"><i class="fas fa-star"></i> Fitur</a></li>
                        <li><a href="#footer" class="nav-link"><i class="fas fa-envelope"></i> Kontak</a></li>
                    </ul>
                    
                    <div class="user-actions">
                        <button class="action-btn"><i class="fas fa-search"></i></button>
                        <button class="action-btn"><i class="fas fa-shopping-cart"></i></button>
                        <button class="action-btn"><i class="fas fa-user"></i></button>
                    </div>
                </div>
            </nav>
            
            <!-- Hero Banner -->
            <section class="hero">
                <div class="hero-content">
                    <div class="developer-info">
                        <span>Dibuat oleh: {{ developer_name }} ({{ developer_nrp }})</span>
                    </div>
                    <h1>Selamat Datang di Ecommerce Seada ada nya</h1>
                    <p>Produk Terbaru</p>
                </div>
            </section>
            
            <!-- Product Section -->
            <section id="products" class="container">
                <div class="section-heading">
                    <h2 class="section-title"><i class="fas fa-shopping-bag"></i> Produk Terbaru</h2>
                    <a href="/add" class="add-btn"><i class="fas fa-plus"></i> Tambah Produk</a>
                </div>
                
                <div class="product-grid">
                    {% for id, nama, harga, url in products %}
                    <div class="product-card">
                        {% if loop.index % 3 == 0 %}
                        <div class="product-badge">New</div>
                        {% endif %}
                        
                        <div class="product-img-wrapper">
                            <img src="{{ url }}" alt="{{ nama }}" class="product-img">
                            <div class="product-overlay">
                                <button class="overlay-btn"><i class="fas fa-eye"></i></button>
                                <button class="overlay-btn"><i class="fas fa-heart"></i></button>
                            </div>
                        </div>
                        
                        <div class="product-content">
                            <h3 class="product-name">{{ nama }}</h3>
                            <div class="product-meta">
                                <div class="product-price">Rp {{ "{:,.0f}".format(harga) }}</div>
                                <div class="action-buttons">
                                    <a href="/delete/{{ id }}" onclick="return confirm('Apakah Anda yakin ingin menghapus produk ini?')">
                                        <button class="delete-btn"><i class="fas fa-trash"></i></button>
                                    </a>
                                    <button class="cart-btn"><i class="fas fa-shopping-cart"></i></button>
                                </div>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </section>
            
            <!-- Features Section -->
            <section id="features" class="features">
                <div class="container">
                    <h2 class="section-title" style="text-align: center; margin-bottom: 3rem;"><i class="fas fa-star"></i> Harus banget Beli di sini ?</h2>
                    
                    <div class="features-grid">
                        <div class="feature-card">
                            <div class="feature-icon">
                                <i class="fas fa-truck"></i>
                            </div>
                            <h3 class="feature-title">Pengiriman Cepat</h3>
                            <p class="feature-desc">Pengiriman cepat ke seluruh Indonesia dengan berbagai pilihan layanan ekspedisi terpercaya.</p>
                        </div>
                        
                        <div class="feature-card">
                            <div class="feature-icon">
                                <i class="fas fa-shield-alt"></i>
                            </div>
                            <h3 class="feature-title">Pembayaran Aman</h3>
                            <p class="feature-desc">Transaksi aman dengan berbagai metode pembayaran yang terjamin keamanannya.</p>
                        </div>
                        
                        <div class="feature-card">
                            <div class="feature-icon">
                                <i class="fas fa-undo"></i>
                            </div>
                            <h3 class="feature-title">Garansi 30 Hari</h3>
                            <p class="feature-desc">Garansi pengembalian produk dalam 30 hari jika ada kerusakan atau ketidaksesuaian.</p>
                        </div>
                        
                        <div class="feature-card">
                            <div class="feature-icon">
                                <i class="fas fa-headset"></i>
                            </div>
                            <h3 class="feature-title">Layanan 24/7</h3>
                            <p class="feature-desc">Tim customer service kami siap membantu Anda selama 24 jam setiap hari.</p>
                        </div>
                    </div>
                </div>
            </section>
            
            <!-- Footer -->
            <footer id="footer">
                <div class="container">
                    <div class="footer-content">
                        <div class="footer-column">
                            <h3>SHAP</h3>
                            <p class="footer-text">Toko online terpercaya yang menyediakan berbagai produk berkualitas dengan harga terbaik.</p>
                            <div class="social-links">
                                <a href="#" class="social-link"><i class="fab fa-facebook-f"></i></a>
                                <a href="#" class="social-link"><i class="fab fa-twitter"></i></a>
                                <a href="#" class="social-link"><i class="fab fa-instagram"></i></a>
                                <a href="#" class="social-link"><i class="fab fa-linkedin-in"></i></a>
                            </div>
                        </div>
                        
                        <div class="footer-column">
                            <h3>Link Cepat</h3>
                            <ul class="footer-links">
                                <li><a href="/">Beranda</a></li>
                                <li><a href="#products">Produk</a></li>
                                <li><a href="#features">Fitur</a></li>
                                <li><a href="#">Tentang Kami</a></li>
                                <li><a href="#">Kontak</a></li>
                            </ul>
                        </div>
                        
                        <div class="footer-column">
                            <h3>Kategori</h3>
                            <ul class="footer-links">
                                <li><a href="#">Elektronik</a></li>
                                <li><a href="#">Fashion</a></li>
                                <li><a href="#">Kesehatan</a></li>
                                <li><a href="#">Peralatan Rumah</a></li>
                                <li><a href="#">Olahraga</a></li>
                            </ul>
                        </div>
                        
                        <div class="footer-column">
                            <h3>Kontak</h3>
                            <ul class="footer-links">
                                <li><i class="fas fa-map-marker-alt"></i> Jl. sekepanjang 3</li>
                                <li><i class="fas fa-phone"></i> +62 812-3456-7890</li>
                                <li><i class="fas fa-envelope"></i> info@shop.com</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="footer-bottom">
                        <p>&copy; {{ current_year }} Abeng | Dibuat oleh <span class="developer">{{ developer_name }} ({{ developer_nrp }})</span></p>
                    </div>
                </div>
            </footer>
        </body>
        </html>
        '''
        
        current_year = datetime.now().year
        return render_template_string(html, 
                                    products=products, 
                                    current_year=current_year,
                                    developer_name=developer_name,
                                    developer_nrp=developer_nrp)
    
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>"

# Route untuk halaman form tambah produk
@app.route('/add')
def add_product_form():
    # Developer info
    developer_name = "Mochamad Abel Avriyana S"
    developer_nrp = "152022141"
    
    html = '''
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Tambah Produk Baru - Abeng</title>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            :root {
                --primary: #4f46e5;
                --primary-dark: #3730a3;
                --secondary: #6366f1;
                --dark: #111827;
                --light: #f9fafb;
                --gray: #6b7280;
                --danger: #ef4444;
                --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
                --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            }
            
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Poppins', sans-serif;
                background-color: #f3f4f6;
                color: var(--dark);
                line-height: 1.6;
            }
            
            /* Navbar */
            .navbar {
                background-color: white;
                padding: 1rem 0;
                box-shadow: var(--shadow);
            }
            
            .container {
                width: 90%;
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .navbar-container {
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .logo {
                font-size: 1.5rem;
                font-weight: 700;
                color: var(--primary);
                text-decoration: none;
            }
            
            .back-link {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                color: var(--dark);
                text-decoration: none;
                font-weight: 500;
                transition: color 0.2s;
            }
            
            .back-link:hover {
                color: var(--primary);
            }
            
            /* Form Container */
            .form-container {
                max-width: 800px;
                margin: 2rem auto;
                background-color: white;
                border-radius: 0.5rem;
                box-shadow: var(--shadow);
                overflow: hidden;
            }
            
            .form-header {
                background-color: var(--primary);
                color: white;
                padding: 1.5rem;
                text-align: center;
            }
            
            .form-title {
                font-size: 1.5rem;
                font-weight: 600;
                margin-bottom: 0.5rem;
            }
            
            .form-subtitle {
                font-size: 0.875rem;
                opacity: 0.9;
            }
            
            .form-content {
                padding: 2rem;
            }
            
            .form-group {
                margin-bottom: 1.5rem;
            }
            
            .form-label {
                display: block;
                font-weight: 500;
                margin-bottom: 0.5rem;
                color: var(--dark);
            }
            
            .form-control {
                width: 100%;
                padding: 0.75rem 1rem;
                border: 1px solid #d1d5db;
                border-radius: 0.375rem;
                font-family: 'Poppins', sans-serif;
                font-size: 1rem;
                transition: border-color 0.2s;
            }
            
            .form-control:focus {
                outline: none;
                border-color: var(--primary);
                box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
            }
            
            .form-hint {
                font-size: 0.75rem;
                color: var(--gray);
                margin-top: 0.5rem;
            }
            
            .form-buttons {
                display: flex;
                gap: 1rem;
                margin-top: 2rem;
            }
            
            .btn {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
                padding: 0.75rem 1.5rem;
                border-radius: 0.375rem;
                font-weight: 500;
                text-decoration: none;
                transition: all 0.2s;
                cursor: pointer;
                border: none;
                font-family: 'Poppins', sans-serif;
                font-size: 1rem;
            }
            
            .btn-primary {
                background-color: var(--primary);
                color: white;
            }
            
            .btn-primary:hover {
                background-color: var(--primary-dark);
            }
            
            .btn-danger {
                background-color: var(--danger);
                color: white;
            }
            
            .btn-danger:hover {
                background-color: #dc2626;
            }
            
            /* Footer */
            .footer {
                text-align: center;
                padding: 1rem 0;
                color: var(--gray);
                font-size: 0.875rem;
                margin-top: 2rem;
            }
            
            .developer {
                font-weight: 600;
                color: var(--dark);
            }
            
            @media (max-width: 768px) {
                .form-content {
                    padding: 1.5rem;
                }
                
                .form-buttons {
                    flex-direction: column;
                }
            }
        </style>
    </head>
    <body>
        <!-- Navbar -->
        <nav class="navbar">
            <div class="container navbar-container">
                <a href="/" class="logo">ABENGSHOP</a>
                <a href="/" class="back-link"><i class="fas fa-arrow-left"></i> Kembali ke Beranda</a>
            </div>
        </nav>
        
        <!-- Form Container -->
        <div class="container">
            <div class="form-container">
                <div class="form-header">
                    <h1 class="form-title">Tambah Produk Baru</h1>
                    <p class="form-subtitle">Lengkapi formulir di bawah ini untuk menambahkan produk baru</p>
                </div>
                
                <div class="form-content">
                    <form action="/add" method="post">
                        <div class="form-group">
                            <label for="name" class="form-label">Nama Produk</label>
                            <input type="text" id="name" name="name" class="form-control" required>
                            <p class="form-hint">Masukkan nama produk yang deskriptif (maksimal 100 karakter)</p>
                        </div>
                        
                        <div class="form-group">
                            <label for="price" class="form-label">Harga (Rp)</label>
                            <input type="number" id="price" name="price" class="form-control" min="1000" required>
                            <p class="form-hint">Masukkan harga produk dalam Rupiah (minimal Rp 1.000)</p>
                        </div>
                        
                        <div class="form-group">
                            <label for="image_url" class="form-label">URL Gambar</label>
                            <input type="url" id="image_url" name="image_url" class="form-control" required>
                            <p class="form-hint">Masukkan URL gambar produk (direkomendasikan rasio 1:1)</p>
                        </div>
                        
                        <div class="form-buttons">
                            <a href="/" class="btn btn-danger"><i class="fas fa-times"></i> Batal</a>
                            <button type="submit" class="btn btn-primary"><i class="fas fa-save"></i> Simpan Produk</button>
                        </div>
                    </form>
                </div>
            </div>
            
            <div class="footer">
                <p>&copy; {{ current_year }} ABENG | Dibuat oleh <span class="developer">{{ developer_name }} ({{ developer_nrp }})</span></p>
            </div>
        </div>
    </body>
    </html>
    '''
    
    current_year = datetime.now().year
    return render_template_string(html, 
                                current_year=current_year,
                                developer_name=developer_name,
                                developer_nrp=developer_nrp)

# Route untuk memproses form tambah produk
@app.route('/add', methods=['POST'])
def add_product():
    if request.method == 'POST':
        try:
            # Ambil data dari form
            name = request.form.get('name')
            price_str = request.form.get('price')
            image_url = request.form.get('image_url')

            # Validasi form
            if not name or not image_url or not price_str:
                return "<h1>Error</h1><p>Semua field harus diisi</p>"

            # Validasi harga
            try:
                price = float(price_str)
                if price <= 0:
                    return "<h1>Error</h1><p>Harga harus lebih dari 0</p>"
            except ValueError:
                return "<h1>Error</h1><p>Harga harus berupa angka yang valid</p>"

            # Upload gambar ke S3
            s3_image_url = None
            try:
                response = requests.get(image_url, stream=True)
                response.raise_for_status()

                file_extension = ""
                if '.' in image_url:
                    file_extension = image_url.split('.')[-1].lower()
                s3_file_name = f"{uuid.uuid4()}.{file_extension}"

                s3.upload_fileobj(response.raw, S3_BUCKET_NAME, s3_file_name)
                s3_image_url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_file_name}"

            except requests.exceptions.RequestException as e:
                return f"<h1>Error</h1><p>Gagal mengunduh gambar dari URL: {e}</p>"
            except Exception as e:
                return f"<h1>Error</h1><p>Gagal mengupload gambar ke S3: {e}</p>"

            # Simpan produk ke database
            db = get_db_connection()
            if not db:
                return "<h1>Error koneksi database</h1>"

            cursor = db.cursor()
            sql = "INSERT INTO products (name, price, image_url) VALUES (%s, %s, %s)"
            cursor.execute(sql, (name, price, s3_image_url))  # gunakan URL dari S3!
            db.commit()
            cursor.close()
            db.close()

            # Redirect ke halaman utama
            return redirect(url_for('home'))
            
        except Exception as e:
            return f"<h1>Error</h1><p>{str(e)}</p>"

# Route untuk menghapus produk
@app.route('/delete/<int:id>')
def delete_product(id):
    try:
        # Koneksi ke database
        db = get_db_connection()
        if not db:
            return "<h1>Error koneksi database</h1>"
            
        # Hapus data dari database
        cursor = db.cursor()
        sql = "DELETE FROM products WHERE id = %s"
        cursor.execute(sql, (id,))
        db.commit()
        cursor.close()
        db.close()
        
        # Redirect ke halaman utama
        return redirect(url_for('home'))
        
    except Exception as e:
        #ke,balikan
        return f"<h1>Error</h1><p>{str(e)}</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)