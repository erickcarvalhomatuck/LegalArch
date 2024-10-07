from interface import PDFViewerApp

if __name__ == "__main__":
    # List of PDFs (These should be in the same directory as the script or provide a full path)
    pdf_files = ["cp.pdf", "L8213.pdf", "CF.pdf", "CódigoCivil.pdf", "CCB.pdf", "CPP.pdf", "CPC.pdf", "CTB.pdf", "Clt.pdf"]
    
    # Initialize and run the app
    app = PDFViewerApp(pdf_files)
    app.mainloop()
