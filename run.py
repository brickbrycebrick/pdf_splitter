from split_by_section import PDFChapterSplitter

splitter = PDFChapterSplitter(
    input_pdf=r"books\book_dynamic_systems_lynch.pdf",
    output_dir=r"output",
    debug=True  # Set to False to suppress detailed output
)