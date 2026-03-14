import React from 'react';

/**
 * SecurityScore Component
 * Displays user's security level, badges, and achievements
 */
function SecurityScore({ stats }) {
  const levelColors = {
    'Beginner': 'bg-gray-100 text-gray-800 border-gray-400',
    'Explorer': 'bg-blue-100 text-blue-800 border-blue-400',
    'Hunter': 'bg-purple-100 text-purple-800 border-purple-400',
    'Defender': 'bg-red-100 text-red-800 border-red-400',
    'Expert': 'bg-yellow-100 text-yellow-800 border-yellow-400',
  };

  const getLevelDescription = (level) => {
    const descriptions = {
      'Beginner': 'Just starting your security journey',
      'Explorer': 'Learning the basics of cybersecurity',
      'Hunter': 'Actively detecting and preventing threats',
      'Defender': 'Protecting yourself and others online',
      'Expert': 'Mastered cybersecurity awareness',
    };
    return descriptions[level] || '';
  };

  const getProgressPercentage = (points, level) => {
    const levelThresholds = {
      'Beginner': [0, 50],
      'Explorer': [50, 150],
      'Hunter': [150, 350],
      'Defender': [350, 600],
      'Expert': [600, 999999],
    };
    
    const [min, max] = levelThresholds[level];
    return ((points - min) / (max - min)) * 100;
  };

  return (
    <div className="mb-8 grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Main Score Card */}
      <div className="lg:col-span-2 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-lg shadow-lg p-8 text-white">
        <div className="flex items-start justify-between mb-6">
          <div>
            <h2 className="text-3xl font-bold mb-2">Security Score</h2>
            <p className="text-blue-100">Your cybersecurity mastery level</p>
          </div>
          <div className="text-6xl">🛡️</div>
        </div>

        <div className="mb-6">
          <div className="flex items-end justify-between mb-2">
            <span className="font-semibold text-lg">{stats.total_points} / {stats.next_level_points || '∞'}</span>
            <span className={`px-3 py-1 rounded-full font-bold border-2 ${levelColors[stats.level] || levelColors['Beginner']}`}>
              {stats.level}
            </span>
          </div>
          <div className="w-full bg-blue-400/30 rounded-full h-3 overflow-hidden">
            <div 
              className="bg-white h-full transition-all duration-500 rounded-full" 
              style={{ width: `${getProgressPercentage(stats.total_points, stats.level)}%` }}
            ></div>
          </div>
          <p className="text-blue-100 text-sm mt-2">{getLevelDescription(stats.level)}</p>
        </div>

        <div className="grid grid-cols-3 gap-4">
          <div className="bg-white/20 rounded-lg p-3">
            <p className="text-blue-100 text-xs font-semibold mb-1">DAILY STREAK</p>
            <p className="text-2xl font-bold">{stats.daily_login_streak || 0}🔥</p>
          </div>
          <div className="bg-white/20 rounded-lg p-3">
            <p className="text-blue-100 text-xs font-semibold mb-1">ACCURACY</p>
            <p className="text-2xl font-bold">{stats.accuracy || 0}%</p>
          </div>
          <div className="bg-white/20 rounded-lg p-3">
            <p className="text-blue-100 text-xs font-semibold mb-1">BADGES</p>
            <p className="text-2xl font-bold">{stats.badges?.length || 0}/12</p>
          </div>
        </div>
      </div>

      {/* Badges Section */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">Achievements</h3>
        <div className="grid grid-cols-3 gap-3">
          {stats.badges && stats.badges.length > 0 ? (
            stats.badges.map((badge, idx) => (
              <div key={idx} className="flex flex-col items-center">
                <div className="text-3xl mb-2 bg-yellow-100 dark:bg-yellow-900 p-2 rounded-lg">
                  {getBadgeIcon(badge)}
                </div>
                <p className="text-xs text-center text-gray-700 dark:text-gray-300 truncate w-full" title={badge}>
                  {badge}
                </p>
              </div>
            ))
          ) : (
            <div className="col-span-3 text-center py-6">
              <p className="text-gray-600 dark:text-gray-400 text-sm">
                Complete activities to earn badges!
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function getBadgeIcon(badge) {
  const icons = {
    'quiz_perfectionist': '🎯',
    'phishing_detective': '🔍',
    'file_inspector': '📁',
    'lab_master': '🧪',
    'daily_guardian': '⏰',
    'security_scholar': '📚',
    'password_guardian': '🔐',
    'url_analyst': '🔗',
    'expert_analyst': '⭐',
    'streak_champion': '🔥',
    'threat_warrior': '⚔️',
    'early_adopter': '🚀',
  };
  return icons[badge] || '🏆';
}

export default SecurityScore;
