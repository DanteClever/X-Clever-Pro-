# Studio Pentas IRAN                             #
# Email : studiopentasiran@gmail.com   #
# ----------------------------------------------------#
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
import os
import pydub
from pydub import AudioSegment
import pandas as pd
#from docx import Document  # error libertory 
from ebooklib import epub
import json
import xml.etree.ElementTree as ET

# تنظیمات اصلی برنامه
root = tk.Tk()
root.title("X-Clever Pro")
root.resizable(False, False)
root.geometry('250x600+50+50')

p1 = tk.PhotoImage(file = f'image/icon.png') 
  
# Setting icon of master window 
root.iconphoto(False, p1)

# تنظیم تم تاریک
root.tk_setPalette(background='#2d2d2d', foreground='white', 
                  activeBackground='#3d3d3d', activeForeground='white')

style = ttk.Style()
style.configure('TFrame', background='#2d2d2d') #
style.configure('TLabelFrame', background='#2d2d2d', foreground='white') # 
style.configure('TButton', background='black', foreground='black', padding=5) # font color 
style.configure('TLabel', background='#2d2d2d', foreground='white') #




def select_input_file(filetypes):
    """انتخاب فایل ورودی"""
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=filetypes)
    return file_path

def select_output_path(default_name, filetypes):
    """انتخاب مسیر ذخیره فایل خروجی"""
    output_path = filedialog.asksaveasfilename(
        title="Save output file",
        initialfile=default_name,
        filetypes=filetypes,
        defaultextension=filetypes[0][1] if filetypes else ""
    )
    return output_path

def show_success(message):
    """نمایش پیام موفقیت"""
    messagebox.showinfo("Success", message)

def show_error(error):
    """نمایش پیام خطا"""
    messagebox.showerror("Error", f"An error occurred:\n{str(error)}")

# ==================== تبدیل اسناد و متن ====================
def pdf_to_text():
    try:
        input_path = select_input_file([("PDF Files", "*.pdf")])
        if not input_path: return
            
        output_path = select_output_path("output.txt", [("Text Files", "*.txt")])
        if not output_path: return
        
        with open(input_path, 'rb') as pdf_file:
            reader = PdfReader(pdf_file)
            text = "\n".join([page.extract_text() for page in reader.pages])
        
        with open(output_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)
            
        show_success(f"PDF converted to text and saved at:\n{output_path}")
    
    except Exception as e:
        show_error(e)

def text_to_pdf():
    try:
        input_path = select_input_file([("Text Files", "*.txt")])
        if not input_path: return
            
        output_path = select_output_path("output.pdf", [("PDF Files", "*.pdf")])
        if not output_path: return
        
        with open(input_path, 'r', encoding='utf-8') as txt_file:
            text_content = txt_file.read()
        
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter
        c.setFont("Helvetica", 12)
        
        lines = text_content.split('\n')
        y_position = height - 50
        for line in lines:
            if y_position < 50:
                c.showPage()
                y_position = height - 50
                c.setFont("Helvetica", 12)
            c.drawString(50, y_position, line)
            y_position -= 15
        
        c.save()
        show_success(f"Text converted to PDF and saved at:\n{output_path}")
    
    except Exception as e:
        show_error(e)

def docx_to_pdf():
    try:
        # نیاز به نصب python-docx و pdfkit دارد
        import pdfkit
        input_path = select_input_file([("Word Files", "*.docx")])
        if not input_path: return
            
        output_path = select_output_path("output.pdf", [("PDF Files", "*.pdf")])
        if not output_path: return
        
        pdfkit.from_file(input_path, output_path)
        show_success(f"DOCX converted to PDF and saved at:\n{output_path}")
    
    except Exception as e:
        show_error(f"{e}\nPlease install wkhtmltopdf and pdfkit")

# ==================== تبدیل تصاویر ====================
def convert_image(input_ext, output_ext, output_format, quality=95):
    try:
        input_path = select_input_file([(f"{input_ext.upper()} Files", f"*.{input_ext}")])
        if not input_path: return
            
        output_path = select_output_path(f"output.{output_ext}", [(f"{output_ext.upper()} Files", f"*.{output_ext}")])
        if not output_path: return

        img = Image.open(input_path)
        
        if output_format == "JPEG":
            img = img.convert("RGB")
        
        img.save(output_path, output_format, quality=quality)
        show_success(f"{input_ext.upper()} converted to {output_ext.upper()} and saved at:\n{output_path}")
    
    except Exception as e:
        show_error(e)

# ==================== تبدیل صوتی ==================== #
def convert_audio(input_ext, output_ext, output_format, bitrate="192k"):
    try:
        input_path = select_input_file([(f"{input_ext.upper()} Files", f"*.{input_ext}")])
        if not input_path: return
            
        output_path = select_output_path(f"output.{output_ext}", [(f"{output_ext.upper()} Files", f"*.{output_ext}")])
        if not output_path: return

        audio = AudioSegment.from_file(input_path, format=input_ext)
        audio.export(output_path, format=output_ext, bitrate=bitrate)
        show_success(f"{input_ext.upper()} converted to {output_ext.upper()} and saved at:\n{output_path}")
    
    except Exception as e:
        show_error(f"{e}\nMake sure ffmpeg is installed.")

# ==================== تبدیل ویدیو ====================
def convert_video(input_ext, output_ext):
    try:
        # نیاز به نصب ffmpeg دارد
        input_path = select_input_file([(f"{input_ext.upper()} Files", f"*.{input_ext}")])
        if not input_path: return
            
        output_path = select_output_path(f"output.{output_ext}", [(f"{output_ext.upper()} Files", f"*.{output_ext}")])
        if not output_path: return

        os.system(f'ffmpeg -i "{input_path}" "{output_path}"')
        show_success(f"{input_ext.upper()} converted to {output_ext.upper()} and saved at:\n{output_path}")
    
    except Exception as e:
        show_error(f"{e}\nMake sure ffmpeg is installed.")

# ==================== تبدیل داده‌ها ====================
def csv_to_excel():
    try:
        input_path = select_input_file([("CSV Files", "*.csv")])
        if not input_path: return
            
        output_path = select_output_path("output.xlsx", [("Excel Files", "*.xlsx")])
        if not output_path: return

        df = pd.read_csv(input_path)
        df.to_excel(output_path, index=False)
        show_success(f"CSV converted to Excel and saved at:\n{output_path}")
    
    except Exception as e:
        show_error(e)

def excel_to_csv():
    try:
        input_path = select_input_file([("Excel Files", "*.xlsx;*.xls")])
        if not input_path: return
            
        output_path = select_output_path("output.csv", [("CSV Files", "*.csv")])
        if not output_path: return

        df = pd.read_excel(input_path)
        df.to_csv(output_path, index=False)
        show_success(f"Excel converted to CSV and saved at:\n{output_path}")
    
    except Exception as e:
        show_error(e)

def json_to_xml():
    try:
        input_path = select_input_file([("JSON Files", "*.json")])
        if not input_path: return
            
        output_path = select_output_path("output.xml", [("XML Files", "*.xml")])
        if not output_path: return

        with open(input_path, 'r') as f:
            data = json.load(f)
        
        def dict_to_xml(d, root):
            for k, v in d.items():
                if isinstance(v, dict):
                    child = ET.SubElement(root, k)
                    dict_to_xml(v, child)
                else:
                    ET.SubElement(root, k).text = str(v)
        
        root = ET.Element("root")
        dict_to_xml(data, root)
        tree = ET.ElementTree(root)
        #tree.write(output_path, encoding='utf-8', xml_declaration=True)
        
        show_success(f"JSON converted to XML and saved at:\n{output_path}")
    
    except Exception as e:
        show_error(e)

# ==================== رابط کاربری ====================
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True, padx=10, pady=10)

# تب تبدیل اسناد
doc_frame = ttk.Frame(notebook)
notebook.add(doc_frame, text='Documents')

ttk.Button(doc_frame, text="PDF to Text",command=pdf_to_text ,  width=25).pack(pady=5)
ttk.Button(doc_frame, text="Text to PDF", command=text_to_pdf, width=25).pack(pady=5)
#ttk.Button(doc_frame, text="DOCX to PDF", command=docx_to_pdf, width=25).pack(pady=5)

# تب تبدیل تصاویر
img_frame = ttk.Frame(notebook)
notebook.add(img_frame, text='Images')

image_conversions = [
    ("PNG to JPG", "png", "jpg", "JPEG"),
    ("JPG to PNG", "jpg", "png", "PNG"),
    ("WEBP to PNG", "webp", "png", "PNG"),
    ("BMP to JPG", "bmp", "jpg", "JPEG"),
    ("TIFF to PNG", "tiff", "png", "PNG")
]

for text, inp, out, fmt in image_conversions:
    ttk.Button(img_frame, text=text, 
              command=lambda i=inp, o=out, f=fmt: convert_image(i, o, f), 
              width=25).pack(pady=5)

# تب تبدیل صوتی
audio_frame = ttk.Frame(notebook)
notebook.add(audio_frame, text='Audio')

audio_conversions = [
    ("MP3 to WAV", "mp3", "wav", "wav"),
    ("WAV to MP3", "wav", "mp3", "mp3"),
    ("OGG to MP3", "ogg", "mp3", "mp3"),
    ("FLAC to WAV", "flac", "wav", "wav"),
    ("AAC to MP3", "aac", "mp3", "mp3")
]

for text, inp, out, fmt in audio_conversions:
    ttk.Button(audio_frame, text=text, 
              command=lambda i=inp, o=out, f=fmt: convert_audio(i, o, f), 
              width=25).pack(pady=5)

# تب تبدیل ویدیو
video_frame = ttk.Frame(notebook)
notebook.add(video_frame, text='Video')

video_conversions = [
    ("MP4 to AVI", "mp4", "avi"),
    ("AVI to MP4", "avi", "mp4"),
    ("MKV to MP4", "mkv", "mp4"),
    ("MOV to MP4", "mov", "mp4"),
    ("WEBM to MP4", "webm", "mp4")
]

for text, inp, out in video_conversions:
    ttk.Button(video_frame, text=text, 
              command=lambda i=inp, o=out: convert_video(i, o), 
              width=25).pack(pady=5)

# تب تبدیل داده‌ها
data_frame = ttk.Frame(notebook)
notebook.add(data_frame, text='Data')

ttk.Button(data_frame, text="CSV to Excel", command=csv_to_excel, width=25).pack(pady=5)
ttk.Button(data_frame, text="Excel to CSV", command=excel_to_csv, width=25).pack(pady=5)
ttk.Button(data_frame, text="JSON to XML", command=json_to_xml, width=25).pack(pady=5)

# نکته نصب پیش‌نیازها
note_frame = ttk.Frame(root)
note_frame.pack(fill='x', padx=10, pady=5)

ttk.Label(note_frame, 
         text=" Gmail: StudioPentasIran@gmail.com",
         style='TLabel').pack()

root.mainloop()

