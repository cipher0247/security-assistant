import hashlib
import os

class FileScanner:
    def __init__(self):
        # Common malware extensions (just for metadata, not static blocking)
        self.suspicious_extensions = ['.exe', '.dll', '.bat', '.cmd', '.sh', '.vbs', '.js', '.scr']

    async def scan_file(self, content: bytes, filename: str):
        size = len(content)
        sha256_hash = hashlib.sha256(content).hexdigest()
        
        # Simple entropy calculation (Shannon entropy)
        entropy = self.calculate_entropy(content)
        
        # Extension check
        ext = os.path.splitext(filename)[1].lower()
        is_suspicious_ext = ext in self.suspicious_extensions
        
        return {
            "filename": filename,
            "size": size,
            "hash": sha256_hash,
            "entropy": entropy,
            "suspicious_extension": is_suspicious_ext,
            "risk_factors": self.assess_risk(entropy, is_suspicious_ext)
        }

    def calculate_entropy(self, data: bytes) -> float:
        import math
        if not data:
            return 0
        entropy = 0
        for x in range(256):
            p_x = float(data.count(x)) / len(data)
            if p_x > 0:
                entropy += - p_x * math.log(p_x, 2)
        return entropy

    def assess_risk(self, entropy: float, suspicious_ext: bool):
        factors = []
        if entropy > 7.0:
            factors.append("High entropy (possible packed/encrypted code)")
        if suspicious_ext:
            factors.append("Suspicious file extension typically used for executables")
        if not factors:
            factors.append("No static anomalies detected")
        return factors
