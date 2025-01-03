import streamlit as st
import os
import zipfile
from bns_pdf_splitter import (
    extract_first_page_text,
    get_outfile_prefix,
    get_page_number_range,
    # extract_first_line_of_each_page,
    split_pdf,
    DEFAULT_ISSN,
)
import tempfile


def process_pdf(pdf_file):
    # Create a temporary directory to store files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save uploaded file temporarily
        temp_pdf_path = os.path.join(temp_dir, "input.pdf")
        with open(temp_pdf_path, "wb") as f:
            f.write(pdf_file.getvalue())

        # Process the PDF
        first_page_text = extract_first_page_text(temp_pdf_path)
        output_prefix = get_outfile_prefix(first_page_text)
        page_ranges = get_page_number_range(first_page_text, DEFAULT_ISSN)
        # page_number = extract_first_line_of_each_page(temp_pdf_path)

        # Split the PDF
        # Assuming split_pdf creates files in the current directory
        # Get the current working directory
        current_dir = os.getcwd()
        split_pdf(temp_pdf_path, page_ranges, output_prefix)

        # Create a ZIP file containing all split PDFs
        zip_filename = f"{output_prefix}.zip"
        zip_path = os.path.join(temp_dir, zip_filename)

        # Create ZIP file with split PDFs
        with zipfile.ZipFile(zip_path, "w") as zipf:
            # Look for split PDFs in the current directory
            for file in os.listdir(current_dir):
                if file.startswith(output_prefix) and file.endswith(".pdf"):
                    file_path = os.path.join(current_dir, file)
                    # Add file to zip
                    zipf.write(file_path, file)
                    # Optional: remove the split PDF after adding to zip
                    os.remove(file_path)

        # Read the ZIP file
        with open(zip_path, "rb") as f:
            return f.read(), zip_filename


def main():
    st.set_page_config(
        page_title="BNS PDF Splitter",
    )

    st.image(
        "assets/bns_header.jpg", width=None
    )  # Use width=None to let the image determine its width

    st.title("BNS PDF Splitter App")
    st.write("Upload a BNS PDF file to split it into multiple PDFs")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        st.write("File uploaded successfully!")

        if st.button("Process PDF"):
            with st.spinner("Processing PDF..."):
                try:
                    zip_content, zip_filename = process_pdf(uploaded_file)

                    # Offer the ZIP file for download
                    st.download_button(
                        label="Download Split PDFs",
                        data=zip_content,
                        file_name=zip_filename,
                        mime="application/zip",
                    )

                    st.success(
                        "PDF processing completed! Click the button above to download the split PDFs."
                    )
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
