import os
import cv2
import numpy as np
from PIL import Image, ImageChops, ImageEnhance
import io
import base64
import tempfile

class DeepfakeDetector:
    @staticmethod
    def run_ela(image_bytes, quality=90):
        """
        Performs Error Level Analysis (ELA) on an image.
        Returns:
            - ela_image_base64: The ELA visualization as a base64 string.
            - score: A suspicion score (0-100) based on the ELA variance.
        """
        try:
            original = Image.open(io.BytesIO(image_bytes)).convert('RGB')
            
            # 1. Save at a known quality level
            buffer = io.BytesIO()
            original.save(buffer, 'JPEG', quality=quality)
            buffer.seek(0)
            resaved = Image.open(buffer)
            
            # 2. Calculate pixel difference
            ela_image = ImageChops.difference(original, resaved)
            
            # 3. Calculate Extrema (max difference) to scale contrast
            extrema = ela_image.getextrema()
            max_diff = max([ex[1] for ex in extrema])
            if max_diff == 0:
                max_diff = 1
            scale = 255.0 / max_diff
            
            # 4. Enhance brightness to make artifacts visible
            ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
            
            # 5. Calculate Suspicion Score
            # Convert to numpy for stats
            ela_np = np.array(ela_image)
            # Calculate brightness mean and variance of the difference
            # Higher variance/mean often implies inconsistent compression levels (manipulation)
            # This is a heuristic approximation.
            gray_ela = cv2.cvtColor(ela_np, cv2.COLOR_RGB2GRAY)
            # Threshold to remove background noise (uniform compression artifacts)
            _, thresh = cv2.threshold(gray_ela, 15, 255, cv2.THRESH_BINARY)
            non_zero_count = cv2.countNonZero(thresh)
            total_pixels = gray_ela.size
            
            # Score based on percentage of "high error" pixels
            # Normal images have uniform noise. Edited ones have patches of high noise.
            # However, simpler logic: if extremely high noise everywhere -> might just be high res/complex
            # If low noise -> likely original or consistent.
            # We'll map the ratio to a 0-100 score.
            ratio = (non_zero_count / total_pixels) * 100
            score = min(100, int(ratio * 3)) # Amplify a bit
            
            # 6. Convert ELA image to base64 for frontend
            buffered = io.BytesIO()
            ela_image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            
            return {
                "ela_image": f"data:image/jpeg;base64,{img_str}",
                "score": score
            }
            
        except Exception as e:
            print(f"ELA Error: {e}")
            return None

    @staticmethod
    def process_video(video_path):
        """
        Extracts key frames from a video and runs ELA on them.
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return None
            
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        duration = frame_count / fps if fps > 0 else 0
        
        # Extract 3 key frames: Start, Middle, End (avoiding very first/last to prevent black screens)
        points = [0.1, 0.5, 0.9]
        frames_analysis = []
        total_score = 0
        
        for p in points:
            target_frame = int(frame_count * p)
            cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
            ret, frame = cap.read()
            if ret:
                # Convert OpenCV BGR to Pillow RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(rgb_frame)
                
                # Save to bytes
                buf = io.BytesIO()
                pil_image.save(buf, format='JPEG')
                image_bytes = buf.getvalue()
                
                # Run ELA
                result = DeepfakeDetector.run_ela(image_bytes)
                if result:
                    frames_analysis.append(result)
                    total_score += result['score']
        
        cap.release()
        
        avg_score = int(total_score / len(frames_analysis)) if frames_analysis else 0
        return {
            "score": avg_score,
            "frames": frames_analysis,
            "duration": f"{duration:.1f}s"
        }
