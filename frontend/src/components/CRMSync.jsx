import React from 'react';

export default function CRMSync({ metrics }) {
  const crmIntegrations = [
    { name: 'HubSpot', icon: '🎯', status: 'Connected', synced: 234 },
    { name: 'Salesforce', icon: '☁️', status: 'Connected', synced: 156 },
    { name: 'Pipedrive', icon: '📊', status: 'Connected', synced: 89 }
  ];

  return (
    <div>
      <h3 className="text-lg font-semibold mb-4">CRM Integrations</h3>

      <div className="grid grid-cols-3 gap-4 mb-6">
        {crmIntegrations.map(crm => (
          <div key={crm.name} className="bg-gradient-to-br from-purple-500 to-purple-700 text-white p-6 rounded-lg">
            <div className="text-3xl mb-2">{crm.icon}</div>
            <div className="font-semibold">{crm.name}</div>
            <div className="text-sm opacity-90 mt-2">{crm.status}</div>
            <div className="text-2xl font-bold mt-4">{crm.synced}</div>
            <div className="text-xs opacity-75">Synced today</div>
          </div>
        ))}
      </div>

      {/* Sync Performance */}
      <div className="bg-blue-50 p-4 rounded border border-blue-200">
        <div className="flex justify-between items-center mb-2">
          <div className="font-semibold text-gray-800">Sync Success Rate</div>
          <div className="text-2xl font-bold text-blue-600">{metrics.crmSyncSuccess}%</div>
        </div>
        <div className="text-xs text-gray-600">Leads successfully synced to CRM systems</div>
        <div className="mt-3 bg-gray-300 rounded-full h-2">
          <div className="bg-blue-500 h-2 rounded-full" style={{ width: `${metrics.crmSyncSuccess}%` }}></div>
        </div>
      </div>

      {/* Sync Details */}
      <div className="mt-6 bg-gray-50 p-4 rounded">
        <div className="font-semibold text-gray-800 mb-3">Recent Sync Activity</div>
        <div className="space-y-2 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-700">Average sync time</span>
            <span className="font-semibold text-gray-900">{metrics.avgResponseTime} sec</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-700">Last sync</span>
            <span className="font-semibold text-green-600">✓ Just now</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-700">Queued for sync</span>
            <span className="font-semibold text-gray-900">12 leads</span>
          </div>
        </div>
      </div>
    </div>
  );
}
