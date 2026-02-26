import React from 'react';

export default function LeadDashboard({ leads }) {
  const leadStats = [
    { category: 'HOT', count: 324, color: 'text-red-600', bg: 'bg-red-100' },
    { category: 'WARM', count: 892, color: 'text-yellow-600', bg: 'bg-yellow-100' },
    { category: 'COLD', count: 1456, color: 'text-blue-600', bg: 'bg-blue-100' }
  ];

  return (
    <div>
      <h3 className="text-lg font-semibold mb-4">Lead Distribution</h3>

      {/* Lead Stats */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        {leadStats.map(stat => (
          <div key={stat.category} className={`p-4 rounded ${stat.bg}`}>
            <div className="text-sm font-medium text-gray-700">{stat.category} Leads</div>
            <div className={`text-2xl font-bold ${stat.color}`}>{stat.count}</div>
            <div className="text-xs text-gray-600 mt-2">
              {stat.category === 'HOT' && '🔥 Ready to contact'}
              {stat.category === 'WARM' && '⏳ Nurture needed'}
              {stat.category === 'COLD' && '❄️ Long-term'}
            </div>
          </div>
        ))}
      </div>

      {/* Lead Scoring Accuracy */}
      <div className="bg-gray-50 p-4 rounded border border-gray-200">
        <div className="flex justify-between items-center">
          <div>
            <div className="font-semibold text-gray-800">ML Model Accuracy</div>
            <div className="text-sm text-gray-600">Lead classification performance</div>
          </div>
          <div className="text-3xl font-bold text-green-600">92%</div>
        </div>
        <div className="mt-3 bg-gray-300 rounded-full h-2">
          <div className="bg-green-500 h-2 rounded-full" style={{ width: '92%' }}></div>
        </div>
      </div>
    </div>
  );
}
