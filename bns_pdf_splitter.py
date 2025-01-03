# %%
import argparse
import fitz  # PyMuPDF
import re
import sys

# %%

DEFAULT_ISSN = "1411-6499"
# pdf_path = "BNS Vol 20 No 1 Februari 2021 Rev17-02-23-2.pdf"


# %%
def extract_first_page_text(pdf_path):
    """Extracts text from the first page of a PDF using PyMuPDF.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        The text content of the first page, or None if there's an error or the file is empty.
    """
    try:
        doc = fitz.open(pdf_path)
        if not doc.page_count:  # Handle empty PDFs
            return None
        page = doc[0]
        text = page.get_text()
        return text
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None


def get_page_number_range(first_page_text, issn):
    # Regular expression to match digit-hyphen-digit sequences
    pattern = r"\d+-\d+"

    matches = re.findall(pattern, first_page_text)

    # remove ISSN from matches list
    matches.remove(issn)
    return matches


def remove_punctuation_all(text):
    """Removes all punctuation from a string using regular expressions.

    Args:
        text: The input string.

    Returns:
        The string with all punctuation removed.
    """
    return re.sub(r"[^\w\s]", "", text)


def extract_vol_no_regex(text):
    """Extracts lines using a regular expression."""
    match = re.search(
        r"Vol\.\s*\d+,?\s*No\.\s*\d+", text, re.IGNORECASE
    )  # re.IGNORECASE handles case insensitive search
    if match:
        # Finds the entire line containing the match using the line break as a delimiter
        lines = text.splitlines()
        for line in lines:
            if match.group(0) in line:
                return line
    return ""


def get_outfile_prefix(first_page_text):
    vol_no = extract_vol_no_regex(first_page_text)
    output_prefix = remove_punctuation_all(vol_no)
    output_prefix = "BNS " + output_prefix
    return output_prefix


def extract_first_line_of_each_page(pdf_path):
    """Extracts the first line of text from each page of a PDF using PyMuPDF."""
    try:
        doc = fitz.open(pdf_path)
        if not doc.page_count:
            return []
        first_lines = []
        for page in doc:
            text = page.get_text()
            if text:
                lines = text.splitlines()
                if lines:
                    first_lines.append(lines[0])
                else:
                    first_lines.append("")
            else:
                first_lines.append("")

        return first_lines
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return []


def map_page_number(pdf_path):
    # Get the page numbers from text
    first_lines = extract_first_line_of_each_page(pdf_path)

    # Create a mapping of extracted page numbers to actual PDF page indices
    page_number_mapping = {}
    for idx, line in enumerate(first_lines):
        if line.strip().isdigit():  # Check if the line contains only digits
            page_number_mapping[int(line)] = idx
    return page_number_mapping


def split_pdf(pdf_path, page_ranges, output_prefix):
    page_number_mapping = map_page_number(pdf_path)

    # Open the PDF
    pdf_document = fitz.open(pdf_path)

    # Process each range
    for page_range in page_ranges:
        # Get start and end page numbers
        start, end = map(int, page_range.split("-"))

        # Create a new PDF document
        output_pdf = fitz.open()

        # Get the actual PDF page indices for this range
        start_idx = page_number_mapping.get(start)
        end_idx = page_number_mapping.get(end)

        if start_idx is not None and end_idx is not None:
            # Copy the specified pages
            output_pdf.insert_pdf(pdf_document, from_page=start_idx, to_page=end_idx)

            # Save the output PDF
            output_filename = f"{output_prefix}_{start}-{end}.pdf"
            output_pdf.save(output_filename)
            output_pdf.close()

            print(f"Created: {output_filename}")
        else:
            print(f"Warning: Could not find page indices for range {start}-{end}")

    # Close the input PDF
    pdf_document.close()


# %%


def main():
    parser = argparse.ArgumentParser(
        description="Split a PDF based on page ranges extracted from its content."
    )
    parser.add_argument("pdf_path", help="Path to the input PDF file")
    parser.add_argument(
        "ISSN",
        nargs="?",
        default=DEFAULT_ISSN,
        help="ISSN of the publication (required for page range extraction)",
    )
    args = parser.parse_args()

    pdf_path = args.pdf_path
    ISSN = args.ISSN

    try:
        first_page_text = extract_first_page_text(pdf_path)
        output_prefix = get_outfile_prefix(first_page_text)
        page_ranges = get_page_number_range(first_page_text, ISSN)
        # page_number = extract_first_line_of_each_page(pdf_path)

        split_pdf(pdf_path, page_ranges, output_prefix)
    except FileNotFoundError:
        print(f"Error: PDF file not found at '{pdf_path}'", file=sys.stderr)
        sys.exit(1)  # Exit with an error code
    except Exception as e:  # Catch other potential errors
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
