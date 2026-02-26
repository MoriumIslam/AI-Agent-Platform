import React from 'react';

export default function MessageInbox() {
  const messages = [
    {
      id: 1,
      platform: 'Instagram',
      author: '@johndoe',
      text: 'I need help with API integration',
      score: 87,
      category: 'HOT',
      timestamp: '2 mins ago'
    },
    {
      id: 2,
      platform: 'Twitter',
      author: '@techuser',
      text: 'Great product! When is pricing available?',
      score: 75,
      category: 'WARM',
      timestamp: '5 mins ago'
    },
    {
      id: 3,
      platform: 'LinkedIn',
      author: 'Sarah Smith',
      text: 'Interested in enterprise plan',
      score: 92,
      category: 'HOT',
      timestamp: '8 mins ago'
    }
  ];

  const getBgColor = (category) => {
    if (category === 'HOT') return 'bg-red-100 border-l-4 border-red-500';
    if (category === 'WARM') return 'bg-yellow-100 border-l-4 border-yellow-500';
    return 'bg-blue-100 border-l-4 border-blue-500';
  };

  return (
    <div>
      <h3 className="text-lg font-semibold mb-4">Recent Messages</h3>
      <div className="space-y-3">
        {messages.map(msg => (
          <div key={msg.id} className={`p-4 rounded ${getBgColor(msg.category)}`}>
            <div className="flex justify-between items-start">
              <div>
                <div className="font-semibold text-gray-800">{msg.platform} - {msg.author}</div>
                <div className="text-sm text-gray-700 mt-1">{msg.text}</div>
                <div className="text-xs text-gray-600 mt-2">{msg.timestamp}</div>
              </div>
              <div className="text-right">
                <div className="text-lg font-bold text-gray-800">{msg.score}</div>
                <span className={`inline-block px-2 py-1 rounded text-xs font-bold text-white ${msg.category === 'HOT' ? 'bg-red-500' :
                    msg.category === 'WARM' ? 'bg-yellow-500' :
                      'bg-blue-500'
                  }`}>{msg.category}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
