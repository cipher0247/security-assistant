import React, { useState, useEffect } from 'react';
import axios from 'axios';
import SecurityScore from './SecurityScore';

/**
 * Dashboard Component
 * Main landing page showing user stats, recent activity, and quick access to tools
 */
function Dashboard({ user }) {
  const [stats, setStats] = useState(null);
  const [recentActivity, setRecentActivity] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const token = localStorage.getItem('auth_token');
        
        // Fetch user stats
        const statsResponse = await axios.get(`${API_BASE}/gamification/stats/${user.id}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        setStats(statsResponse.data);

        // Fetch recent activity
        const activityResponse = await axios.get(`${API_BASE}/user/activity`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        setRecentActivity(activityResponse.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, [user.id]);

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="animate-pulse space-y-6">
          <div className="h-32 bg-gray-200 dark:bg-gray-700 rounded-lg"></div>
          <div className="grid grid-cols-3 gap-4">
            {[1, 2, 3].map(i => <div key={i} className="h-24 bg-gray-200 dark:bg-gray-700 rounded-lg"></div>)}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
          Welcome, {user.username}! 👋
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Your AI Cybersecurity Mentor | Stay Safe Online
        </p>
      </div>

      {/* Security Score Card */}
      {stats && <SecurityScore stats={stats} />}

      {/* Quick Access Tools Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <QuickAccessCard 
          icon="🔐" 
          title="Password Strength" 
          description="Check your password security"
          link="/password"
          color="blue"
        />
        <QuickAccessCard 
          icon="🌐" 
          title="URL Safety" 
          description="Verify if a link is secure"
          link="/url"
          color="purple"
        />
        <QuickAccessCard 
          icon="🚨" 
          title="Phishing Detection" 
          description="Identify suspicious emails"
          link="/phishing"
          color="red"
        />
        <QuickAccessCard 
          icon="🤖" 
          title="AI Assistant" 
          description="Get security guidance"
          link="/assistant"
          color="green"
        />
        <QuickAccessCard 
          icon="🏆" 
          title="Leaderboard" 
          description="View top security experts"
          link="/leaderboard"
          color="yellow"
        />
        <QuickAccessCard 
          icon="📚" 
          title="Learning Hub" 
          description="Interactive security labs"
          link="/labs"
          color="indigo"
        />
      </div>

      {/* Recent Activity */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Recent Activity</h2>
        {recentActivity.length > 0 ? (
          <div className="space-y-3">
            {recentActivity.slice(0, 5).map((activity, idx) => (
              <div key={idx} className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">{getActivityIcon(activity.type)}</span>
                  <div>
                    <p className="font-semibold text-gray-900 dark:text-white">{activity.description}</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">{activity.timestamp}</p>
                  </div>
                </div>
                <span className="text-blue-600 dark:text-blue-400 font-bold">+{activity.points} pts</span>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-600 dark:text-gray-400">No activity yet. Start analyzing URLs or checking passwords!</p>
        )}
      </div>

      {/* Tips Section */}
      <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
        <TipCard 
          title="Security Tip 1" 
          icon="💡"
          content="Never reuse passwords across multiple websites. Use unique, strong passwords for each account."
        />
        <TipCard 
          title="Security Tip 2" 
          icon="🔒"
          content="Enable two-factor authentication (2FA) on important accounts. It adds an extra layer of security."
        />
      </div>
    </div>
  );
}

function QuickAccessCard({ icon, title, description, link, color }) {
  const colorClasses = {
    blue: 'bg-blue-50 dark:bg-blue-900 border-blue-200 dark:border-blue-700',
    purple: 'bg-purple-50 dark:bg-purple-900 border-purple-200 dark:border-purple-700',
    red: 'bg-red-50 dark:bg-red-900 border-red-200 dark:border-red-700',
    green: 'bg-green-50 dark:bg-green-900 border-green-200 dark:border-green-700',
    yellow: 'bg-yellow-50 dark:bg-yellow-900 border-yellow-200 dark:border-yellow-700',
    indigo: 'bg-indigo-50 dark:bg-indigo-900 border-indigo-200 dark:border-indigo-700',
  };

  return (
    <a href={link} className={`p-6 rounded-lg border-2 ${colorClasses[color]} hover:shadow-lg transition cursor-pointer`}>
      <div className="text-4xl mb-3">{icon}</div>
      <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">{title}</h3>
      <p className="text-gray-600 dark:text-gray-400 text-sm">{description}</p>
      <div className="mt-4 text-sm font-semibold text-blue-600 dark:text-blue-400">
        Get started →
      </div>
    </a>
  );
}

function TipCard({ title, icon, content }) {
  return (
    <div className="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900 dark:to-indigo-900 rounded-lg p-6 border-l-4 border-blue-600">
      <div className="flex items-start space-x-3">
        <span className="text-3xl">{icon}</span>
        <div>
          <h3 className="font-bold text-gray-900 dark:text-white mb-2">{title}</h3>
          <p className="text-gray-700 dark:text-gray-300 text-sm">{content}</p>
        </div>
      </div>
    </div>
  );
}

function getActivityIcon(type) {
  const icons = {
    'password_check': '🔐',
    'url_check': '🌐',
    'phishing_check': '🚨',
    'quiz_complete': '✅',
    'lab_complete': '🎓',
    'badge_earned': '🏆',
  };
  return icons[type] || '📊';
}

export default Dashboard;
