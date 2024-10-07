import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import fitz  # PyMuPDF to render PDF previews
import webbrowser
import os

class PDFViewerApp(tk.Tk):
    def __init__(self, pdf_files):
        super().__init__()
        self.title("Law Reference Files")
        self.geometry("900x700")
        self.configure(bg="#288490")  # Cor de fundo da janela

        self.create_widgets(pdf_files)

    def create_widgets(self, pdf_files):
        # Frame para o cabeçalho
        header_frame = tk.Frame(self, bg="#005965", relief="raised", bd=2)  # Cabeçalho em #005965
        header_frame.pack(fill=tk.X)

        # Carregar e redimensionar a logo
        logo = self.load_logo("LogoSLe.png")
        if logo:
            logo_label = tk.Label(header_frame, image=logo, bg="#005965")
            logo_label.image = logo
            logo_label.pack(side=tk.LEFT, padx=10, pady=5)

        header_label = tk.Label(header_frame, text="Law Reference Files", font=("Arial", 24, "bold"), fg="white", bg="#005965")
        header_label.pack(side=tk.LEFT, padx=20, pady=10)

        # Frame principal para os PDFs
        content_frame = tk.Frame(self, bg="#288490")  # Cor de fundo da interface
        content_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)


        # Criando uma grade para os arquivos PDF
        for idx, pdf_file in enumerate(pdf_files):
            self.create_pdf_widget(content_frame, pdf_file, idx)

    def create_pdf_widget(self, parent, pdf_file, idx):
        # Frame para cada entrada de PDF
        pdf_frame = tk.Frame(parent, bg="#2B6D7C", bd=2, relief="groove")  # Cor dos frames dos PDFs
        pdf_frame.grid(row=idx // 3, column=idx % 3, padx=20, pady=20)

        # Renderizar pré-visualização do PDF
        preview_image = self.render_pdf_preview(pdf_file)

        # Adicionar imagem (pré-visualização da primeira página do PDF)
        if preview_image:
            img_label = tk.Label(pdf_frame, image=preview_image, bg="#2B6D7C", bd=0)
            img_label.image = preview_image
            img_label.pack(pady=5)

        # Nome do PDF
        pdf_label = tk.Label(pdf_frame, text=pdf_file, font=("Arial", 14, "bold"), fg="white", bg="#2B6D7C")
        pdf_label.pack(pady=10)

        # Botão "Ler" com design melhorado
        read_button = ttk.Button(pdf_frame, text="Read", command=lambda: self.read_pdf(pdf_file))
        read_button.pack(pady=10)

        # Estilizar o botão
        style = ttk.Style()
        style.configure("TButton", background="white", foreground="black")  # Cor do botão
        style.map("TButton", background=[("active", "#E0E0E0")])  # Cor do botão ao passar o mouse


    def render_pdf_preview(self, pdf_file):
        try:
            pdf_document = fitz.open(pdf_file)
            page = pdf_document.load_page(0)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img = img.resize((150, 200))  # Redimensionar imagem para caber na interface
            img = img.convert("RGB")
            img_with_border = Image.new("RGB", (160, 210), (255, 255, 255))  # Adicionando borda à imagem
            img_with_border.paste(img, (5, 5))  # Colocar imagem com borda de 5px
            return ImageTk.PhotoImage(img_with_border)
        except Exception as e:
            messagebox.showerror("Error", f"Could not render PDF: {str(e)}")
            return None

    def read_pdf(self, pdf_file):
        # Abrir o arquivo PDF no navegador padrão
        file_path = os.path.abspath(pdf_file)
        if os.path.exists(file_path):
            webbrowser.open(f"file://{file_path}")
        else:
            messagebox.showerror("Error", f"PDF file not found: {pdf_file}")

    def load_logo(self, logo_file):
        try:
            logo = Image.open(logo_file)
            logo = logo.resize((50, 50), Image.Resampling.LANCZOS)  # Tamanho reduzido da logo
            return ImageTk.PhotoImage(logo)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load logo: {str(e)}")
            return None

if __name__ == "__main__":
    pdf_files = ["cp.pdf", "L8213.pdf", "CF.pdf", "CódigoCivil.pdf", "CCB.pdf", "CPP.pdf", "CPC.pdf", "CTB.pdf", "Clt.pdf"]
    app = PDFViewerApp(pdf_files)
    app.mainloop()
