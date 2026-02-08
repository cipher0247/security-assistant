import re
import math

class PasswordStrengthChecker:
    def __init__(self):
        self.common_passwords = {"password", "123456", "qwerty", "admin", "welcome"} # Mock list

    def check_strength(self, password: str, attack_mode: str = 'offline', hardware: str = 'gpu', hash_type: str = 'md5'):
        # 1. Entropy Calculation
        pool_size = 0
        if re.search(r'[a-z]', password): pool_size += 26
        if re.search(r'[A-Z]', password): pool_size += 26
        if re.search(r'[0-9]', password): pool_size += 10
        if re.search(r'[^a-zA-Z0-9]', password): pool_size += 32
        
        entropy = 0
        if pool_size > 0:
            entropy = len(password) * math.log2(pool_size)

        # 2. Crack Time Estimate
        combinations = pool_size ** len(password) if pool_size > 0 else 0
        
        # Guerrilla math for guesses/sec based on scenario
        guesses_per_sec = 10_000_000_000 # Default fallback
        
        if attack_mode == 'online':
            guesses_per_sec = 100 # Rate limited web login (optimistic 100/sec, usually far less)
        else: # offline
            # Hardware multiplier
            hw_mult = 1
            if hardware == 'supercomputer': hw_mult = 1000
            elif hardware == 'gpu': hw_mult = 100
            elif hardware == 'cpu': hw_mult = 1
            
            # Hash difficulty (Baseline: MD5 on CPU = 10M/sec)
            base_rate = 10_000_000 
            if hash_type == 'md5': 
                # MD5 is vastly faster on GPU. 
                # RTX 4090 can do ~160GH/s (160 Billion). Let's use a "Common Hacker GPU" estimate of 10B/sec for 'gpu'
                if hardware == 'gpu': base_rate = 10_000_000_000
                elif hardware == 'supercomputer': base_rate = 1_000_000_000_000
                else: base_rate = 10_000_000 # CPU
            elif hash_type == 'bcrypt':
                # Bcrypt is designed to be slow. 
                # CPU: ~10/sec? GPU: ~5000/sec?
                if hardware == 'gpu': base_rate = 10_000
                elif hardware == 'supercomputer': base_rate = 1_000_000
                else: base_rate = 50 # CPU
            elif hash_type == 'sha256':
                # Slower than MD5, faster than Bcrypt
                 if hardware == 'gpu': base_rate = 1_000_000_000
                 else: base_rate = 5_000_000

            guesses_per_sec = base_rate

        seconds_to_crack = combinations / guesses_per_sec if guesses_per_sec > 0 else 0
        time_human = self._format_time(seconds_to_crack)

        # 3. Score & Feedback
        score = 0
        feedback = []
        
        if len(password) < 8:
            feedback.append("Password is too short (min 8 chars).")
        else:
            score += 1
            
        if pool_size > 36: # Mixed case + numbers or special
            score += 1
        if pool_size > 60: # Complex
            score += 1
        
        if entropy > 60:
            score += 1
            
        if password.lower() in self.common_passwords:
            score = 0
            feedback.append("Commonly used password detected!")
            
        # Adjust score based on survival time in the selected scenario
        # If it cracks instantly in the selected scenario, cap score
        if seconds_to_crack < 1:
            score = min(score, 1)
            feedback.append(f"In this {attack_mode} scenario, it would crack instantly.")
        elif seconds_to_crack < 60:
            score = min(score, 2)

        rating = ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"][min(score, 4)]

        return {
            "password_length": len(password),
            "entropy": round(entropy, 2),
            "crack_time_estimate": time_human,
            "guesses_per_second": guesses_per_sec,
            "rating": rating,
            "score": score, # 0-4
            "feedback": feedback
        }

    def _format_time(self, seconds):
        if seconds < 1: return "Instantly"
        if seconds < 60: return f"{int(seconds)} seconds"
        if seconds < 3600: return f"{int(seconds/60)} minutes"
        if seconds < 86400: return f"{int(seconds/3600)} hours"
        if seconds < 31536000: return f"{int(seconds/86400)} days"
        return f"{int(seconds/31536000)} years"
