import random
import string
import feedparser
from PIL import Image, ExifTags
from io import BytesIO

class PasswordGenerator:
    @staticmethod
    def generate(length=16, use_symbols=True, use_numbers=True, use_upper=True):
        chars = string.ascii_lowercase
        if use_upper: chars += string.ascii_uppercase
        if use_numbers: chars += string.digits
        if use_symbols: chars += "!@#$%^&*()-_=+"
        
        # Ensure at least one of each selected type
        password = []
        if use_upper: password.append(random.choice(string.ascii_uppercase))
        if use_numbers: password.append(random.choice(string.digits))
        if use_symbols: password.append(random.choice("!@#$%^&*()-_=+"))
        
        # Fill rest
        while len(password) < length:
            password.append(random.choice(chars))
            
        random.shuffle(password)
        return "".join(password)

class SteganographyTool:
    @staticmethod
    def hide_text(image_bytes, text):
        img = Image.open(BytesIO(image_bytes)).convert('RGB')
        encoded = img.copy()
        width, height = img.size
        
        # Convert text to binary
        binary_text = ''.join(format(ord(i), '08b') for i in text)
        binary_text += '00000000' # Null Delimiter
        
        data_index = 0
        data_len = len(binary_text)
        
        pixels = encoded.load()
        
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                
                if data_index < data_len:
                    # Modify LSB of Red channel
                    r = (r & ~1) | int(binary_text[data_index])
                    data_index += 1
                
                pixels[x, y] = (r, g, b)
                
                if data_index >= data_len:
                    break
            if data_index >= data_len:
                break
                
        output = BytesIO()
        encoded.save(output, format='PNG')
        return output.getvalue()

    @staticmethod
    def extract_text(image_bytes):
        img = Image.open(BytesIO(image_bytes)).convert('RGB')
        binary_data = ""
        pixels = img.load()
        width, height = img.size
        
        for y in range(height):
            for x in range(width):
                r, _, _ = pixels[x, y]
                binary_data += str(r & 1)

        # Split by 8 bits
        all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
        
        decoded_text = ""
        for byte in all_bytes:
            if byte == "00000000": # Null delimiter
                break
            decoded_text += chr(int(byte, 2))
            
            # Safety break for huge images or noise
            if len(decoded_text) > 5000: 
                break
                
        # Filter non-printable logic if it's just noise
        if len(decoded_text) > 0 and not decoded_text[0].isprintable():
            return "No hidden message found (or encrypted)."
            
        return decoded_text

class ExifViewer:
    @staticmethod
    def get_metadata(image_bytes):
        try:
            img = Image.open(BytesIO(image_bytes))
            exif_data = {}
            
            info = img.getexif()
            if not info:
                print("ExifViewer: No info returned from getexif()")
                return {"status": "No EXIF data found"}
                
            for tag, value in info.items():
                decoded = ExifTags.TAGS.get(tag, tag)
                # Handle bytes (decode or repr)
                if isinstance(value, bytes):
                    try:
                        value = value.decode()
                    except:
                        value = f"<binary data len={len(value)}>"
                
                # Handle IFDRational and other non-JSON types from Pillow
                if not isinstance(value, (str, int, float, bool, list, dict, type(None))):
                    value = str(value)
                    
                exif_data[decoded] = value
                
            return exif_data
        except Exception as e:
            print(f"ExifViewer Error: {e}")
            return {"status": f"Error extracting Exif: {str(e)}"}

class NewsFetcher:
    FEED_URLS = [
        "https://feeds.feedburner.com/TheHackersNews",
        "https://www.bleepingcomputer.com/feed/"
    ]
    
    @staticmethod
    def get_latest_news(limit=5):
        articles = []
        for url in NewsFetcher.FEED_URLS:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:3]:
                    articles.append({
                        "title": entry.title,
                        "link": entry.link,
                        "source": feed.feed.get('title', 'Security News'),
                        "published": entry.get('published', '')[:16] 
                    })
            except Exception as e:
                print(f"Error fetching feed {url}: {e}")
                
        # Shuffle and limit
        random.shuffle(articles)
        return articles[:limit]
