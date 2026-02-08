import hashlib

class HashCalculator:
    @staticmethod
    def calculate_hashes(text: str):
        return {
            "md5": hashlib.md5(text.encode()).hexdigest(),
            "sha1": hashlib.sha1(text.encode()).hexdigest(),
            "sha256": hashlib.sha256(text.encode()).hexdigest(),
            "sha512": hashlib.sha512(text.encode()).hexdigest()
        }
