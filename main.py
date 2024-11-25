import time
from screen_capture import capture_screen
from ocr_processor import extract_text
from gpt_analyzer import analyze_text
from gui_overlay import display_feedback

def main():
    print("Starting AI assistant...")
    while True:
        # Step 1: Capture screen
        frame = capture_screen()
        
        # Step 2: Extract text from the frame
        extracted_text = extract_text(frame)
        if not extracted_text:
            continue

        # Step 3: Analyze text with GPT
        feedback = analyze_text(extracted_text)
        
        # Step 4: Display feedback
        display_feedback(feedback)
        
        # Small delay to prevent overwhelming the system
        time.sleep(2)

if __name__ == "__main__":
    main()