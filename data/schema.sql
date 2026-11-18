-- ====================================================================
-- SQLite 3 DDL Schema: Email Campaign Effectiveness Analysis Platform
-- Author: Moh Junaid (Roll: 250320140094), MCA 2nd Year (DA), ABES
-- Target Database: data/app.db
-- ====================================================================

PRAGMA foreign_keys = ON;

-- 1. Campaign Master Dimension
CREATE TABLE IF NOT EXISTS dim_campaigns (
    campaign_id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_name TEXT NOT NULL UNIQUE,
    campaign_category TEXT NOT NULL CHECK(campaign_category IN ('Product Update', 'Webinar Invite', 'Newsletter', 'Promotional Discount')),
    subject_line TEXT NOT NULL,
    subject_char_length INTEGER NOT NULL CHECK(subject_char_length > 0),
    has_personalization INTEGER NOT NULL CHECK(has_personalization IN (0, 1)),
    has_urgency INTEGER NOT NULL CHECK(has_urgency IN (0, 1)),
    campaign_variant TEXT NOT NULL DEFAULT 'None' CHECK(campaign_variant IN ('A', 'B', 'None')),
    send_date DATE NOT NULL,
    send_day_name TEXT NOT NULL CHECK(send_day_name IN ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')),
    send_hour INTEGER NOT NULL CHECK(send_hour BETWEEN 0 AND 23),
    budget_cost REAL NOT NULL DEFAULT 0.0 CHECK(budget_cost >= 0.0)
);

-- 2. Recipient Master Dimension
CREATE TABLE IF NOT EXISTS dim_recipients (
    recipient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email_address TEXT NOT NULL UNIQUE,
    recipient_domain TEXT NOT NULL,
    domain_type TEXT NOT NULL CHECK(domain_type IN ('Corporate', 'Public Webmail')),
    account_tier TEXT NOT NULL CHECK(account_tier IN ('Enterprise', 'Mid-Market', 'SMB', 'Startup')),
    industry TEXT NOT NULL CHECK(industry IN ('SaaS', 'FinTech', 'Healthcare', 'E-Commerce', 'IT Services')),
    country TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 3. Core Email Dispatches Fact Table
CREATE TABLE IF NOT EXISTS fact_email_dispatches (
    dispatch_id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign_id INTEGER NOT NULL REFERENCES dim_campaigns(campaign_id) ON DELETE RESTRICT,
    recipient_id INTEGER NOT NULL REFERENCES dim_recipients(recipient_id) ON DELETE RESTRICT,
    dispatch_timestamp DATETIME NOT NULL,
    delivery_status TEXT NOT NULL CHECK(delivery_status IN ('Delivered', 'Bounced')),
    bounce_type TEXT NOT NULL DEFAULT 'None' CHECK(bounce_type IN ('None', 'Soft', 'Hard')),
    bounce_reason TEXT,
    is_opened INTEGER NOT NULL DEFAULT 0 CHECK(is_opened IN (0, 1)),
    first_open_timestamp DATETIME,
    total_opens_count INTEGER NOT NULL DEFAULT 0 CHECK(total_opens_count >= 0),
    is_clicked INTEGER NOT NULL DEFAULT 0 CHECK(is_clicked IN (0, 1)),
    first_click_timestamp DATETIME,
    total_clicks_count INTEGER NOT NULL DEFAULT 0 CHECK(total_clicks_count >= 0),
    is_unsubscribed INTEGER NOT NULL DEFAULT 0 CHECK(is_unsubscribed IN (0, 1)),
    unsubscribe_timestamp DATETIME,
    UNIQUE(campaign_id, recipient_id)
);

-- 4. Commercial Conversions Fact Table
CREATE TABLE IF NOT EXISTS fact_conversions (
    conversion_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dispatch_id INTEGER NOT NULL UNIQUE REFERENCES fact_email_dispatches(dispatch_id) ON DELETE CASCADE,
    campaign_id INTEGER NOT NULL REFERENCES dim_campaigns(campaign_id) ON DELETE RESTRICT,
    recipient_id INTEGER NOT NULL REFERENCES dim_recipients(recipient_id) ON DELETE RESTRICT,
    conversion_timestamp DATETIME NOT NULL,
    deal_value REAL NOT NULL DEFAULT 0.0 CHECK(deal_value >= 0.0),
    funnel_stage TEXT NOT NULL CHECK(funnel_stage IN ('MQL', 'SQL', 'Opportunity Won', 'Closed Contract'))
);

-- Indexes for Sub-Second Analytical Queries
CREATE INDEX IF NOT EXISTS idx_dispatches_comp ON fact_email_dispatches(campaign_id, delivery_status, is_opened, is_clicked);
CREATE INDEX IF NOT EXISTS idx_recipients_tier ON dim_recipients(account_tier, recipient_domain);
CREATE INDEX IF NOT EXISTS idx_conversions_camp ON fact_conversions(campaign_id, deal_value);

-- 5. Flattened 40-Column Analytics View
CREATE VIEW IF NOT EXISTS vw_campaign_effectiveness_analytics AS
SELECT 
    d.dispatch_id,
    c.campaign_id,
    c.campaign_name,
    c.campaign_category,
    c.subject_line,
    c.subject_char_length,
    c.has_personalization,
    c.has_urgency,
    c.campaign_variant,
    c.budget_cost AS campaign_budget_cost,
    c.send_date AS campaign_send_date,
    c.send_day_name AS campaign_send_day_name,
    c.send_hour AS campaign_send_hour,
    r.recipient_id,
    r.email_address AS recipient_email,
    r.recipient_domain,
    r.domain_type,
    r.account_tier AS recipient_account_tier,
    r.industry AS recipient_industry,
    r.country AS recipient_country,
    d.dispatch_timestamp,
    d.delivery_status,
    CASE WHEN d.delivery_status = 'Delivered' THEN 1 ELSE 0 END AS is_delivered,
    CASE WHEN d.delivery_status = 'Bounced' THEN 1 ELSE 0 END AS is_bounced,
    d.bounce_type,
    d.bounce_reason,
    d.is_opened,
    d.first_open_timestamp,
    d.total_opens_count,
    d.is_clicked,
    d.first_click_timestamp,
    d.total_clicks_count,
    d.is_unsubscribed,
    d.unsubscribe_timestamp,
    cv.conversion_id,
    CASE WHEN cv.conversion_id IS NOT NULL THEN 1 ELSE 0 END AS is_converted,
    cv.conversion_timestamp,
    COALESCE(cv.deal_value, 0.0) AS conversion_deal_value,
    COALESCE(cv.funnel_stage, 'None') AS conversion_funnel_stage
FROM fact_email_dispatches d
JOIN dim_campaigns c ON d.campaign_id = c.campaign_id
JOIN dim_recipients r ON d.recipient_id = r.recipient_id
LEFT JOIN fact_conversions cv ON d.dispatch_id = cv.dispatch_id;
