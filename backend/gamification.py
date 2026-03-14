"""
Gamification System - Security Scoring & Leveling
Tracks user progress, awards points, and manages game mechanics
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

class UserLevel(Enum):
    """User security awareness levels"""
    BEGINNER = (0, "Beginner", "Just starting your security journey")
    EXPLORER = (50, "Security Explorer", "Learning the basics")
    HUNTER = (150, "Threat Hunter", "Detecting threats effectively")
    DEFENDER = (350, "Cyber Defender", "Advanced security knowledge")
    EXPERT = (600, "Security Expert", "Master of cybersecurity")
    
    def __init__(self, min_points, display_name, description):
        self.min_points = min_points
        self.display_name = display_name
        self.description = description


@dataclass
class Badge:
    """Achievement badge"""
    id: str
    name: str
    description: str
    icon: str
    points_earned: int
    unlock_condition: str


@dataclass
class UserSecurityScore:
    """User's security awareness and performance score"""
    user_id: str
    total_points: int
    level: UserLevel
    points_to_next_level: int
    
    # Stats
    threats_detected: int
    correct_detections: int
    accuracy: float
    
    quizzes_completed: int
    quiz_average: float
    
    labs_completed: int
    
    # Streaks
    daily_login_streak: int
    longest_streak: int
    
    # Badges
    badges: List[Badge]
    
    # Leaderboard
    global_rank: Optional[int]
    regional_rank: Optional[int]


class GameificationEngine:
    """Handles all gamification mechanics"""
    
    # Points system
    POINTS = {
        'quiz_complete': 10,
        'quiz_perfect_score': 20,
        'lab_complete': 25,
        'lab_with_high_score': 35,
        'threat_detection_correct': 5,
        'threat_detection_high_confidence': 8,
        'daily_login': 2,
        'streak_bonus_7days': 50,
        'streak_bonus_30days': 200,
        'assistant_interaction': 1,
    }
    
    # Badges
    BADGES = {
        'first_quiz': Badge(
            id='first_quiz',
            name='Quiz Master Initiate',
            description='Completed your first quiz',
            icon='🎓',
            points_earned=10,
            unlock_condition='complete_1_quiz'
        ),
        'quiz_perfectionist': Badge(
            id='quiz_perfectionist',
            name='Quiz Perfectionist',
            description='Scored 100% on a quiz',
            icon='⭐',
            points_earned=30,
            unlock_condition='perfect_quiz_score'
        ),
        'phishing_detective': Badge(
            id='phishing_detective',
            name='Phishing Detective',
            description='Correctly identified 10 phishing attempts',
            icon='🔍',
            points_earned=50,
            unlock_condition='detect_10_phishing'
        ),
        'file_inspector': Badge(
            id='file_inspector',
            name='File Inspector',
            description='Scanned 25 files for threats',
            icon='📁',
            points_earned=40,
            unlock_condition='scan_25_files'
        ),
        'lab_master': Badge(
            id='lab_master',
            name='Lab Master',
            description='Completed 5 security labs',
            icon='🔬',
            points_earned=75,
            unlock_condition='complete_5_labs'
        ),
        'daily_guardian': Badge(
            id='daily_guardian',
            name='Daily Guardian',
            description='7-day login streak',
            icon='🛡️',
            points_earned=100,
            unlock_condition='7_day_streak'
        ),
        'security_scholar': Badge(
            id='security_scholar',
            name='Security Scholar',
            description='Learned 20+ security terms',
            icon='📚',
            points_earned=35,
            unlock_condition='learn_20_terms'
        ),
        'password_guardian': Badge(
            id='password_guardian',
            name='Password Guardian',
            description='Analyzed 15 passwords',
            icon='🔐',
            points_earned=25,
            unlock_condition='analyze_15_passwords'
        ),
        'url_analyst': Badge(
            id='url_analyst',
            name='URL Analyst',
            description='Checked 20 URLs for safety',
            icon='🌐',
            points_earned=30,
            unlock_condition='check_20_urls'
        ),
        'expert_analyst': Badge(
            id='expert_analyst',
            name='Expert Analyst',
            description='Reached Security Expert level',
            icon='👑',
            points_earned=500,
            unlock_condition='reach_expert_level'
        ),
        'streak_champion': Badge(
            id='streak_champion',
            name='Streak Champion',
            description='30-day login streak',
            icon='🔥',
            points_earned=200,
            unlock_condition='30_day_streak'
        ),
        'threat_warrior': Badge(
            id='threat_warrior',
            name='Threat Warrior',
            description='Detected 50 threats correctly',
            icon='⚔️',
            points_earned=100,
            unlock_condition='detect_50_threats'
        ),
    }
    
    def __init__(self):
        self.user_scores: Dict[str, UserSecurityScore] = {}
        self.leaderboard = []
    
    def initialize_user(self, user_id: str) -> UserSecurityScore:
        """Create new user score"""
        score = UserSecurityScore(
            user_id=user_id,
            total_points=0,
            level=UserLevel.BEGINNER,
            points_to_next_level=50,
            threats_detected=0,
            correct_detections=0,
            accuracy=0.0,
            quizzes_completed=0,
            quiz_average=0.0,
            labs_completed=0,
            daily_login_streak=0,
            longest_streak=0,
            badges=[],
            global_rank=None,
            regional_rank=None
        )
        self.user_scores[user_id] = score
        return score
    
    def add_points(self, user_id: str, action: str, amount: Optional[int] = None) -> int:
        """Add points for an action"""
        if user_id not in self.user_scores:
            self.initialize_user(user_id)
        
        # Use predefined points or custom amount
        points = amount or self.POINTS.get(action, 0)
        
        score = self.user_scores[user_id]
        score.total_points += points
        
        # Check level up
        old_level = score.level
        new_level = self._get_level_from_points(score.total_points)
        
        if old_level != new_level:
            score.level = new_level
            # Award level-up bonus
            score.total_points += 50
            self._trigger_level_up_event(user_id, new_level)
        
        # Update points to next level
        next_level = self._get_next_level(new_level)
        score.points_to_next_level = next_level.min_points - score.total_points
        
        # Check badges
        self._check_badge_conditions(user_id, action)
        
        return points
    
    def record_quiz_completion(self, user_id: str, score: int, max_score: int = 100) -> Dict:
        """Record quiz completion and award points"""
        if user_id not in self.user_scores:
            self.initialize_user(user_id)
        
        user_score = self.user_scores[user_id]
        user_score.quizzes_completed += 1
        
        # Update average
        old_total = user_score.quiz_average * (user_score.quizzes_completed - 1)
        user_score.quiz_average = (old_total + score) / user_score.quizzes_completed
        
        # Award points
        points = self.POINTS['quiz_complete']
        if score == max_score:
            points = self.POINTS['quiz_perfect_score']
        
        self.add_points(user_id, 'quiz_complete', points)
        
        return {
            'points_earned': points,
            'new_total': user_score.total_points,
            'average': user_score.quiz_average
        }
    
    def record_lab_completion(self, user_id: str, lab_score: int, max_score: int = 100) -> Dict:
        """Record lab completion"""
        if user_id not in self.user_scores:
            self.initialize_user(user_id)
        
        user_score = self.user_scores[user_id]
        user_score.labs_completed += 1
        
        # Award points based on score
        points = self.POINTS['lab_complete']
        if lab_score >= 80:
            points = self.POINTS['lab_with_high_score']
        
        self.add_points(user_id, 'lab_complete', points)
        
        return {
            'points_earned': points,
            'new_total': user_score.total_points,
            'labs_completed': user_score.labs_completed
        }
    
    def record_threat_detection(self, user_id: str, was_correct: bool, confidence: float = 0.5) -> Dict:
        """Record threat detection attempt"""
        if user_id not in self.user_scores:
            self.initialize_user(user_id)
        
        user_score = self.user_scores[user_id]
        user_score.threats_detected += 1
        
        if was_correct:
            user_score.correct_detections += 1
        
        # Update accuracy
        user_score.accuracy = (user_score.correct_detections / user_score.threats_detected) * 100
        
        # Award points
        points = 0
        if was_correct:
            points = self.POINTS['threat_detection_correct']
            if confidence >= 0.8:
                points = self.POINTS['threat_detection_high_confidence']
        
        if points > 0:
            self.add_points(user_id, 'threat_detection_correct', points)
        
        return {
            'was_correct': was_correct,
            'points_earned': points,
            'current_accuracy': user_score.accuracy,
            'total_threats_detected': user_score.threats_detected
        }
    
    def record_daily_login(self, user_id: str) -> Dict:
        """Record user daily login and update streak"""
        if user_id not in self.user_scores:
            self.initialize_user(user_id)
        
        user_score = self.user_scores[user_id]
        user_score.daily_login_streak += 1
        
        # Update longest streak
        if user_score.daily_login_streak > user_score.longest_streak:
            user_score.longest_streak = user_score.daily_login_streak
        
        # Award points
        self.add_points(user_id, 'daily_login', self.POINTS['daily_login'])
        
        # Streak bonuses
        if user_score.daily_login_streak == 7:
            self.add_points(user_id, 'streak_bonus_7days', self.POINTS['streak_bonus_7days'])
        elif user_score.daily_login_streak == 30:
            self.add_points(user_id, 'streak_bonus_30days', self.POINTS['streak_bonus_30days'])
        
        return {
            'streak': user_score.daily_login_streak,
            'longest_streak': user_score.longest_streak,
            'points_earned': self.POINTS['daily_login']
        }
    
    def _get_level_from_points(self, total_points: int) -> UserLevel:
        """Get user level based on points"""
        for level in sorted(UserLevel, key=lambda x: x.min_points, reverse=True):
            if total_points >= level.min_points:
                return level
        return UserLevel.BEGINNER
    
    def _get_next_level(self, current_level: UserLevel) -> UserLevel:
        """Get next level promotion"""
        levels = [UserLevel.BEGINNER, UserLevel.EXPLORER, UserLevel.HUNTER, 
                 UserLevel.DEFENDER, UserLevel.EXPERT]
        
        current_idx = levels.index(current_level)
        if current_idx < len(levels) - 1:
            return levels[current_idx + 1]
        return UserLevel.EXPERT
    
    def _trigger_level_up_event(self, user_id: str, new_level: UserLevel):
        """Handle level up event"""
        print(f"🎉 User {user_id} advanced to {new_level.display_name}!")
        print(f"   {new_level.description}")
    
    def _check_badge_conditions(self, user_id: str, action: str):
        """Check if badge conditions are met"""
        user_score = self.user_scores[user_id]
        
        badges_to_check = {
            'first_quiz': user_score.quizzes_completed >= 1,
            'quiz_perfectionist': user_score.quiz_average == 100,
            'phishing_detective': user_score.correct_detections >= 10,
            'file_inspector': False,  # Would need file scan tracking
            'lab_master': user_score.labs_completed >= 5,
            'daily_guardian': user_score.daily_login_streak >= 7,
            'security_scholar': False,  # Would need glossary tracking
            'password_guardian': False,  # Would need password tracking
            'url_analyst': False,  # Would need URL tracking
            'expert_analyst': user_score.level == UserLevel.EXPERT,
            'streak_champion': user_score.daily_login_streak >= 30,
            'threat_warrior': user_score.correct_detections >= 50,
        }
        
        for badge_id, condition in badges_to_check.items():
            if condition and badge_id in self.BADGES:
                self._award_badge(user_id, badge_id)
    
    def _award_badge(self, user_id: str, badge_id: str):
        """Award badge to user"""
        user_score = self.user_scores[user_id]
        badge = self.BADGES[badge_id]
        
        # Check if already earned
        if badge_id not in [b.id for b in user_score.badges]:
            user_score.badges.append(badge)
            self.add_points(user_id, 'badge_earned', badge.points_earned)
            print(f"🏆 {user_id} earned badge: {badge.name}")
    
    def get_user_stats(self, user_id: str) -> UserSecurityScore:
        """Get user statistics"""
        if user_id not in self.user_scores:
            return self.initialize_user(user_id)
        return self.user_scores[user_id]
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get top users by points"""
        sorted_users = sorted(
            self.user_scores.items(),
            key=lambda x: x[1].total_points,
            reverse=True
        )
        
        leaderboard = []
        for rank, (user_id, score) in enumerate(sorted_users[:limit], 1):
            leaderboard.append({
                'rank': rank,
                'user_id': user_id,
                'points': score.total_points,
                'level': score.level.display_name,
                'accuracy': f"{score.accuracy:.1f}%",
                'badges': len(score.badges)
            })
        
        return leaderboard
    
    def get_user_badges(self, user_id: str) -> List[Dict]:
        """Get user's earned badges"""
        if user_id not in self.user_scores:
            return []
        
        user_score = self.user_scores[user_id]
        return [
            {
                'id': badge.id,
                'name': badge.name,
                'icon': badge.icon,
                'description': badge.description,
                'points': badge.points_earned
            }
            for badge in user_score.badges
        ]


# Example usage
if __name__ == "__main__":
    engine = GameificationEngine()
    
    # Initialize user
    user_id = "user123"
    stats = engine.initialize_user(user_id)
    print(f"User initialized: {user_id}")
    
    # Simulate activities
    print("\n=== Simulating User Activities ===\n")
    
    # Daily login
    for day in range(7):
        result = engine.record_daily_login(user_id)
        print(f"Day {day + 1}: Login recorded. Streak: {result['streak']}")
    
    # Quiz completion
    quiz_result = engine.record_quiz_completion(user_id, 85)
    print(f"\nQuiz completed. Points earned: {quiz_result['points_earned']}")
    
    # Threat detection
    threat_result = engine.record_threat_detection(user_id, was_correct=True, confidence=0.9)
    print(f"Threat detected correctly. Accuracy: {threat_result['current_accuracy']:.1f}%")
    
    # Lab completion
    lab_result = engine.record_lab_completion(user_id, 90)
    print(f"Lab completed. Points earned: {lab_result['points_earned']}")
    
    # Get stats
    print("\n=== User Statistics ===")
    final_stats = engine.get_user_stats(user_id)
    print(f"Total Points: {final_stats.total_points}")
    print(f"Level: {final_stats.level.display_name}")
    print(f"Quizzes: {final_stats.quizzes_completed}")
    print(f"Labs: {final_stats.labs_completed}")
    print(f"Badges: {len(final_stats.badges)}")
    
    # Get leaderboard
    print("\n=== Leaderboard ===")
    leaderboard = engine.get_leaderboard()
    for entry in leaderboard:
        print(f"{entry['rank']}. {entry['user_id']}: {entry['points']} points ({entry['level']})")
