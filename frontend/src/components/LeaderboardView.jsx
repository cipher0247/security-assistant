import React, { useState, useEffect } from 'react';
import axios from 'axios';

/**
 * LeaderboardView Component
 * Shows rankings of top security experts and allows filtering
 */
function LeaderboardView({ user }) {
  const [leaderboard, setLeaderboard] = useState([]);
  const [filter, setFilter] = useState('weekly');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [userRank, setUserRank] = useState(null);

  const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

  useEffect(() => {
    fetchLeaderboard();
  }, [filter]);

  const fetchLeaderboard = async () => {
    setLoading(true);
    setError(null);

    try {
      const token = localStorage.getItem('auth_token');
      const response = await axios.get(
        `${API_BASE}/gamification/leaderboard?period=${filter}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setLeaderboard(response.data.leaderboard || []);
      setUserRank(response.data.user_rank);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to load leaderboard');
    } finally {
      setLoading(false);
    }
  };

  const getLevelBadge = (level) => {
    const badges = {
      'Beginner': { icon: '🌱', color: 'bg-gray-100 text-gray-800' },
      'Explorer': { icon: '🔍', color: 'bg-blue-100 text-blue-800' },
      'Hunter': { icon: '🎯', color: 'bg-purple-100 text-purple-800' },
      'Defender': { icon: '🛡️', color: 'bg-red-100 text-red-800' },
      'Expert': { icon: '⭐', color: 'bg-yellow-100 text-yellow-800' },
    };
    return badges[level] || { icon: '❓', color: 'bg-gray-100 text-gray-800' };
  };

  const getMedalIcon = (rank) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return `#${rank}`;
  };

  return (
    <div className="max-w-5xl mx-auto px-4">
      <div className="bg-gradient-to-r from-yellow-400 to-orange-400 rounded-lg shadow-lg p-8 mb-8 text-white">
        <div className="flex items-center space-x-4 mb-6">
          <span className="text-5xl">🏆</span>
          <div>
            <h1 className="text-4xl font-bold">Security Leaderboard</h1>
            <p className="text-yellow-100">Top cybersecurity experts in the community</p>
          </div>
        </div>

        {/* User's Current Rank */}
        {userRank && (
          <div className="bg-white/20 rounded-lg p-4 backdrop-blur">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-yellow-100 text-sm font-semibold mb-1">YOUR CURRENT RANK</p>
                <p className="text-3xl font-bold">#{userRank.rank}</p>
              </div>
              <div className="text-right">
                <p className="text-yellow-100 text-sm font-semibold mb-1">POINTS</p>
                <p className="text-3xl font-bold">{userRank.points}</p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Filter Buttons */}
      <div className="flex gap-2 mb-6 flex-wrap">
        {['daily', 'weekly', 'monthly', 'all-time'].map((period) => (
          <button
            key={period}
            onClick={() => setFilter(period)}
            className={`px-6 py-2 rounded-lg font-semibold transition ${
              filter === period
                ? 'bg-blue-600 text-white'
                : 'bg-white dark:bg-gray-800 text-gray-800 dark:text-white border border-gray-300 dark:border-gray-600 hover:border-blue-500'
            }`}
          >
            {period === 'daily' && '📅 Daily'}
            {period === 'weekly' && '📊 Weekly'}
            {period === 'monthly' && '📈 Monthly'}
            {period === 'all-time' && '⭐ All Time'}
          </button>
        ))}
      </div>

      {/* Leaderboard Table */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden">
        {loading ? (
          <div className="p-8 text-center">
            <div className="animate-spin inline-block w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full"></div>
            <p className="mt-4 text-gray-600 dark:text-gray-400">Loading leaderboard...</p>
          </div>
        ) : error ? (
          <div className="p-8 text-center">
            <p className="text-red-600 dark:text-red-400">Error: {error}</p>
          </div>
        ) : leaderboard.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="bg-gray-100 dark:bg-gray-700 border-b dark:border-gray-600">
                  <th className="px-6 py-4 text-left font-bold text-gray-900 dark:text-white">Rank</th>
                  <th className="px-6 py-4 text-left font-bold text-gray-900 dark:text-white">Username</th>
                  <th className="px-6 py-4 text-left font-bold text-gray-900 dark:text-white">Level</th>
                  <th className="px-6 py-4 text-right font-bold text-gray-900 dark:text-white">Points</th>
                  <th className="px-6 py-4 text-right font-bold text-gray-900 dark:text-white">Accuracy</th>
                  <th className="px-6 py-4 text-right font-bold text-gray-900 dark:text-white">Badges</th>
                </tr>
              </thead>
              <tbody>
                {leaderboard.map((entry, idx) => {
                  const levelBadge = getLevelBadge(entry.level);
                  const isCurrentUser = entry.user_id === user.id;
                  
                  return (
                    <tr 
                      key={entry.user_id} 
                      className={`border-b dark:border-gray-700 transition ${
                        isCurrentUser 
                          ? 'bg-blue-50 dark:bg-blue-900' 
                          : 'hover:bg-gray-50 dark:hover:bg-gray-700'
                      }`}
                    >
                      <td className="px-6 py-4">
                        <div className="flex items-center space-x-2">
                          <span className="text-2xl font-bold">{getMedalIcon(idx + 1)}</span>
                          <span className="font-bold text-gray-900 dark:text-white">#{idx + 1}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center space-x-3">
                          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-bold">
                            {entry.username.charAt(0).toUpperCase()}
                          </div>
                          <div>
                            <p className="font-semibold text-gray-900 dark:text-white">{entry.username}</p>
                            {isCurrentUser && <p className="text-xs text-blue-600 dark:text-blue-400">You</p>}
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <span className={`px-3 py-1 rounded-full font-semibold text-sm ${levelBadge.color}`}>
                          {levelBadge.icon} {entry.level}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-right">
                        <span className="font-bold text-gray-900 dark:text-white">{entry.points}</span>
                      </td>
                      <td className="px-6 py-4 text-right">
                        <span className="font-bold text-gray-900 dark:text-white">{entry.accuracy || 0}%</span>
                      </td>
                      <td className="px-6 py-4 text-right">
                        <span className="inline-flex items-center justify-center w-8 h-8 rounded-full bg-yellow-100 dark:bg-yellow-900 font-bold text-yellow-900 dark:text-yellow-100">
                          {entry.badge_count || 0}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="p-8 text-center">
            <p className="text-gray-600 dark:text-gray-400">No leaderboard data available yet</p>
          </div>
        )}
      </div>

      {/* Info Section */}
      <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
        <InfoCard 
          icon="🎯"
          title="How to Climb"
          description="Complete security challenges, analyze URLs and emails, and participate in quizzes to earn points and badges."
        />
        <InfoCard 
          icon="🏆"
          title="Levels"
          description="Progress from Beginner to Expert by earning points. Each level unlocks new features and badges."
        />
        <InfoCard 
          icon="🎖️"
          title="Badges"
          description="Collect special badges by achieving milestones like perfect quiz scores, streak bonuses, and threat detection."
        />
      </div>
    </div>
  );
}

function InfoCard({ icon, title, description }) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <div className="text-4xl mb-4">{icon}</div>
      <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">{title}</h3>
      <p className="text-gray-600 dark:text-gray-400 text-sm">{description}</p>
    </div>
  );
}

export default LeaderboardView;
