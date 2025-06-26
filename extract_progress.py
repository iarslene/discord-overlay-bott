from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import re
import os

# Path to Tesseract executable on Linux (Railway)
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# Folder containing slides (use relative path)
slides_folder = "./slides"

# Regex to match progress patterns like 6/10, 0/5, 10/10, etc.
progress_pattern = re.compile(r'\b\d{1,2}/\d{1,2}\b')

# Store all matches
all_matches = []

print("\n🔍 OCR Output:\n")

# Loop over slides 4 to 12
for i in range(4, 13):
    slide_path = os.path.join(slides_folder, f"slide{i}.png")
    if not os.path.exists(slide_path):
        print(f"⚠️ Slide {i} missing: {slide_path}")
        continue

    # Load and preprocess image
    image = Image.open(slide_path)
    image = image.resize((image.width * 2, image.height * 2))      # upscale
    image = image.convert("L")                                     # grayscale
    image = ImageEnhance.Contrast(image).enhance(3)                # increase contrast
    image = image.filter(ImageFilter.SHARPEN)                      # sharpen

    # OCR
    raw_text = pytesseract.image_to_string(image)
    print(f"🔍 OCR Output from slide{i}.png:\n{raw_text.strip()}\n")

    # Fix common OCR issues
    cleaned_text = (
        raw_text.replace("W", "1")
                .replace("l", "1")
                .replace("I", "1")
                .replace("O", "0")
    )

    # Extract progress matches
    matches = progress_pattern.findall(cleaned_text)
    all_matches.extend(matches)

# Remove duplicates and sort
unique_matches = sorted(set(all_matches))

# Final output
print("📊 All Progress Detected:")
for match in unique_matches:
    print(f"• {match}")

print(f"\n✅ Total Unique Progress Bars Detected: {len(unique_matches)}")
