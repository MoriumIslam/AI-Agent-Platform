-- PostgreSQL Database Schema for AI Agent Platform
-- Tables: companies, social_connections, leads, messages, responses, crm_sync_logs

-- ============= CORE TABLES =============

CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    subscription_tier VARCHAR(50), -- free, pro, enterprise
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_companies_id ON companies(id);
CREATE INDEX idx_companies_subscription ON companies(subscription_tier);

-- ============= SOCIAL MEDIA CONNECTIONS =============

CREATE TABLE social_connections (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES companies(id),
    platform VARCHAR(50), -- instagram, twitter, linkedin
    account_id VARCHAR(255),
    access_token TEXT ENCRYPTED, -- AES-256 encrypted
    refresh_token TEXT ENCRYPTED,
    expires_at TIMESTAMP,
    connected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

CREATE INDEX idx_social_connections_company ON social_connections(company_id);
CREATE INDEX idx_social_connections_platform ON social_connections(platform);

-- ============= LEADS TABLE =============

CREATE TABLE leads (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(20),
    platform VARCHAR(50), -- source platform
    source_user_id VARCHAR(255),
    lead_score INT DEFAULT 50, -- 0-100
    lead_category VARCHAR(20), -- HOT, WARM, COLD
    sentiment DECIMAL(3,2), -- -1 to 1
    crm_contact_id VARCHAR(255), -- external CRM ID
    crm_system VARCHAR(50), -- hubspot, salesforce, etc
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

CREATE INDEX idx_leads_company ON leads(company_id);
CREATE INDEX idx_leads_score ON leads(lead_score);
CREATE INDEX idx_leads_category ON leads(lead_category);
CREATE INDEX idx_leads_crm_id ON leads(crm_contact_id);

-- ============= MESSAGES TABLE =============

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL,
    lead_id INTEGER,
    platform VARCHAR(50),
    author_id VARCHAR(255),
    author_name VARCHAR(255),
    message_text TEXT,
    message_id VARCHAR(255) UNIQUE, -- external platform message ID
    processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (lead_id) REFERENCES leads(id)
);

CREATE INDEX idx_messages_company ON messages(company_id);
CREATE INDEX idx_messages_lead ON messages(lead_id);
CREATE INDEX idx_messages_platform ON messages(platform);
CREATE INDEX idx_messages_processed ON messages(processed);

-- ============= RESPONSES TABLE =============

CREATE TABLE responses (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL,
    message_id INTEGER NOT NULL,
    response_text TEXT,
    confidence DECIMAL(3,2), -- 0.0 - 1.0
    should_post BOOLEAN,
    actually_posted BOOLEAN DEFAULT FALSE,
    posted_at TIMESTAMP,
    crm_action_taken BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (message_id) REFERENCES messages(id)
);

CREATE INDEX idx_responses_company ON responses(company_id);
CREATE INDEX idx_responses_message ON responses(message_id);
CREATE INDEX idx_responses_confidence ON responses(confidence);

-- ============= CRM SYNC LOGS =============

CREATE TABLE crm_sync_logs (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL,
    lead_id INTEGER,
    crm_system VARCHAR(50), -- hubspot, salesforce
    crm_id VARCHAR(255),
    sync_direction VARCHAR(20), -- outbound, inbound
    status VARCHAR(50), -- success, failed, pending
    error_message TEXT,
    attempt_count INT DEFAULT 1,
    last_attempt_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (lead_id) REFERENCES leads(id)
);

CREATE INDEX idx_crm_sync_company ON crm_sync_logs(company_id);
CREATE INDEX idx_crm_sync_lead ON crm_sync_logs(lead_id);
CREATE INDEX idx_crm_sync_status ON crm_sync_logs(status);

-- ============= AUDIT LOGS =============

CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    company_id INTEGER,
    user_id INTEGER,
    action VARCHAR(100), -- create, update, delete
    resource_type VARCHAR(50), -- lead, message, response
    resource_id INTEGER,
    changes JSONB, -- JSON of what changed
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_logs_company ON audit_logs(company_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_created ON audit_logs(created_at);

-- ============= USAGE METRICS =============

CREATE TABLE usage_metrics (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL,
    date DATE DEFAULT CURRENT_DATE,
    messages_processed INT,
    responses_generated INT,
    auto_posted INT,
    leads_scored INT,
    crm_syncs_attempted INT,
    crm_syncs_succeeded INT,
    cost_usd DECIMAL(10,4),
    FOREIGN KEY (company_id) REFERENCES companies(id)
);

CREATE INDEX idx_usage_metrics_company ON usage_metrics(company_id);
CREATE INDEX idx_usage_metrics_date ON usage_metrics(date);

-- ============= VIEWS =============

-- Real-time dashboard view
CREATE VIEW dashboard_metrics AS
SELECT 
    c.id as company_id,
    c.name,
    COUNT(DISTINCT m.id) as total_messages,
    COUNT(DISTINCT CASE WHEN l.lead_category = 'HOT' THEN l.id END) as hot_leads,
    COUNT(DISTINCT CASE WHEN l.lead_category = 'WARM' THEN l.id END) as warm_leads,
    COUNT(DISTINCT CASE WHEN l.lead_category = 'COLD' THEN l.id END) as cold_leads,
    ROUND(AVG(r.confidence)::numeric, 2) as avg_response_confidence,
    COUNT(DISTINCT CASE WHEN r.actually_posted THEN r.id END) as responses_posted
FROM companies c
LEFT JOIN messages m ON c.id = m.company_id
LEFT JOIN leads l ON c.id = l.company_id
LEFT JOIN responses r ON c.id = r.company_id
GROUP BY c.id, c.name;

-- ============= FUNCTIONS =============

-- Update timestamp function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
CREATE TRIGGER companies_updated_at BEFORE UPDATE ON companies
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER leads_updated_at BEFORE UPDATE ON leads
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============= PARTITIONING (for large tables) =============

-- Partition messages table by month
ALTER TABLE messages ADD COLUMN month DATE;

-- Create partitions (example: 2026-02)
CREATE TABLE messages_2026_02 PARTITION OF messages
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
