import pytesseract

def extract_text(frame):
    # Preprocess the image for OCR
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text.strip()