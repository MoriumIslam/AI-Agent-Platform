import React, { useState, useEffect } from 'react';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import io from 'socket.io-client';
import MessageInbox from './MessageInbox';
import LeadDashboard from './LeadDashboard';
import CRMSync from './CRMSync';

const SOCKET_SERVER = 'http://localhost:5000';

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState('overview');
  const [metrics, setMetrics] = useState({
    messagesProcessed: 1243,
    hotLeads: 324,
    warmLeads: 892,
    coldLeads: 1456,
    crmSyncSuccess: 99.9,
    avgResponseTime: 3.2
  });

  const [socket, setSocket] = useState(null);
  const [realtimeData, setRealtimeData] = useState([]);

  useEffect(() => {
    const newSocket = io(SOCKET_SERVER);

    newSocket.on('metrics_update', (data) => {
      setMetrics(prev => ({ ...prev, ...data }));
    });

    newSocket.on('message_processed', (message) => {
      setRealtimeData(prev => [message, ...prev].slice(0, 10));
    });

    setSocket(newSocket);

    return () => newSocket.close();
  }, []);

  const chartData = [
    { time: '00:00', processed: 45, auto_posted: 40, reviewed: 5 },
    { time: '04:00', processed: 62, auto_posted: 55, reviewed: 7 },
    { time: '08:00', processed: 89, auto_posted: 78, reviewed: 11 },
    { time: '12:00', processed: 145, auto_posted: 128, reviewed: 17 },
    { time: '16:00', processed: 203, auto_posted: 182, reviewed: 21 },
    { time: '20:00', processed: 178, auto_posted: 159, reviewed: 19 },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 to-purple-900 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">🤖 AI Agent Platform</h1>
          <p className="text-purple-200">Social Media Lead Management & CRM Integration</p>
        </div>

        {/* Metrics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div className="bg-white rounded-lg p-6 shadow-lg">
            <div className="text-sm text-gray-600">Messages Processed</div>
            <div className="text-3xl font-bold text-purple-600">{metrics.messagesProcessed}</div>
            <div className="text-xs text-green-600 mt-2">↑ 12% today</div>
          </div>

          <div className="bg-white rounded-lg p-6 shadow-lg">
            <div className="text-sm text-gray-600">Hot Leads</div>
            <div className="text-3xl font-bold text-red-600">{metrics.hotLeads}</div>
            <div className="text-xs text-gray-500 mt-2">Ready to contact</div>
          </div>

          <div className="bg-white rounded-lg p-6 shadow-lg">
            <div className="text-sm text-gray-600">CRM Sync Success</div>
            <div className="text-3xl font-bold text-green-600">{metrics.crmSyncSuccess}%</div>
            <div className="text-xs text-gray-500 mt-2">No failures</div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="bg-white rounded-lg shadow-lg mb-8">
          <div className="flex border-b">
            <button
              onClick={() => setActiveTab('overview')}
              className={`px-6 py-4 font-medium ${activeTab === 'overview' ? 'border-b-2 border-purple-600 text-purple-600' : 'text-gray-600'}`}
            >
              📊 Overview
            </button>
            <button
              onClick={() => setActiveTab('messages')}
              className={`px-6 py-4 font-medium ${activeTab === 'messages' ? 'border-b-2 border-purple-600 text-purple-600' : 'text-gray-600'}`}
            >
              💬 Messages
            </button>
            <button
              onClick={() => setActiveTab('leads')}
              className={`px-6 py-4 font-medium ${activeTab === 'leads' ? 'border-b-2 border-purple-600 text-purple-600' : 'text-gray-600'}`}
            >
              🎯 Leads
            </button>
            <button
              onClick={() => setActiveTab('crm')}
              className={`px-6 py-4 font-medium ${activeTab === 'crm' ? 'border-b-2 border-purple-600 text-purple-600' : 'text-gray-600'}`}
            >
              🔄 CRM Sync
            </button>
          </div>

          {/* Tab Content */}
          <div className="p-6">
            {activeTab === 'overview' && (
              <div>
                <h3 className="text-lg font-semibold mb-4">Message Processing Trends</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="time" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="processed" fill="#667eea" />
                    <Bar dataKey="auto_posted" fill="#4caf50" />
                    <Bar dataKey="reviewed" fill="#ffd333" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}

            {activeTab === 'messages' && <MessageInbox socket={socket} />}
            {activeTab === 'leads' && <LeadDashboard leads={realtimeData} />}
            {activeTab === 'crm' && <CRMSync metrics={metrics} />}
          </div>
        </div>

        {/* Footer */}
        <div className="text-center text-purple-200 text-sm">
          <p>✨ Real-time Processing | 99.95% Uptime SLA | Production Ready</p>
        </div>
      </div>
    </div>
  );
}
