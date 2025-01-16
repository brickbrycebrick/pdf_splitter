import os
import pikepdf
from PyPDF2 import PdfReader, PdfWriter

class PDFChapterSplitter:
    """A class to split PDFs into chapters based on outline/bookmarks."""
    
    def __init__(self, input_pdf, output_dir, debug=True):
        """
        Initialize and run the PDF splitter.
        
        Args:
            input_pdf (str): Path to the input PDF file
            output_dir (str): Directory where chapter PDFs will be saved
            debug (bool): Whether to print debug information
        """
        self.debug = debug
        
        # Clean file paths
        self.input_pdf = os.path.normpath(input_pdf)
        if not self.input_pdf.lower().endswith('.pdf'):
            self.input_pdf += '.pdf'
        self.output_dir = os.path.normpath(output_dir)
        
        # Run the splitting process automatically
        try:
            self.split_pdf()
            print(f"Successfully split PDF into sections in: {self.output_dir}")
        except Exception as e:
            if self.debug:
                import traceback
                print(f"Full error traceback:")
                print(traceback.format_exc())
            else:
                print(f"Error splitting PDF: {str(e)}")

    def _debug_print(self, *args):
        """Print debug information if debug mode is enabled."""
        if self.debug:
            print(*args)

    def _extract_outline(self, pdf):
        """
        Extract outline information using pikepdf.
        Returns list of (title, page_number) tuples.
        """
        def process_outlines(outlines, pdf):
            sections = []
            
            try:
                for outline in outlines:
                    # Get the title
                    if hasattr(outline, 'title'):
                        title = outline.title
                    else:
                        continue

                    # Get the page number
                    if hasattr(outline, 'destination'):
                        dest = outline.destination
                        if dest is not None and len(dest) > 0:
                            # The first item in the destination array is the page object
                            page_obj = dest[0]
                            
                            # Find the page number by matching the page object
                            for i, page in enumerate(pdf.pages):
                                if page.obj == page_obj:
                                    self._debug_print(f"Found section: {title} on page {i+1}")
                                    sections.append((title, i))
                                    break

                    # Process any children
                    if hasattr(outline, 'children'):
                        sections.extend(process_outlines(outline.children, pdf))
                        
            except Exception as e:
                self._debug_print(f"Error processing outline item: {e}")
            
            return sections

        try:
            with pikepdf.open(self.input_pdf) as pdf:
                # Get the outline (bookmarks)
                outlines = pdf.open_outline()
                if outlines.root is None:
                    self._debug_print("No outline found in PDF")
                    return []

                sections = process_outlines(outlines.root, pdf)
                return sections

        except Exception as e:
            self._debug_print(f"Error extracting outline: {e}")
            return []

    def _sanitize_filename(self, title):
        """Convert outline title to valid filename."""
        invalid_chars = '<>:"/\\|?*'
        filename = ''.join(c for c in title if c not in invalid_chars)
        filename = filename.strip()[:50].rstrip('.')
        return filename if filename else 'section'

    def split_pdf(self):
        """Split PDF into separate files based on outline."""
        if not os.path.exists(self.input_pdf):
            raise FileNotFoundError(f"Input PDF not found: {self.input_pdf}")
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Get outline using pikepdf
        sections = self._extract_outline(self.input_pdf)
        
        if not sections:
            print("No valid outline found in PDF. Cannot split.")
            return
        
        # Sort sections by page number and remove duplicates
        sections = sorted(set(sections), key=lambda x: x[1])
        self._debug_print("\nFound sections:")
        for title, page in sections:
            self._debug_print(f"- {title}: Page {page + 1}")
        
        # Now use PyPDF2 for the actual splitting
        reader = PdfReader(self.input_pdf)
        self._debug_print(f"\nPDF opened successfully. Total pages: {len(reader.pages)}")
        
        # Add the last page as the end point
        sections.append(('End', len(reader.pages)))
        
        # Split PDF into sections
        for i in range(len(sections) - 1):
            try:
                title, start_page = sections[i]
                _, end_page = sections[i + 1]
                
                writer = PdfWriter()
                
                # Add pages
                for page_num in range(start_page, end_page):
                    writer.add_page(reader.pages[page_num])
                
                # Create filename
                safe_title = self._sanitize_filename(title)
                output_filename = f"{str(i+1).zfill(2)}_{safe_title}.pdf"
                output_path = os.path.join(self.output_dir, output_filename)
                
                # Save the section
                with open(output_path, 'wb') as output_file:
                    writer.write(output_file)
                print(f'Created: {output_path} (Pages {start_page+1}-{end_page})')
                
            except Exception as e:
                self._debug_print(f"Error processing section {i}: {e}")
                if self.debug:
                    import traceback
                    traceback.print_exc()
