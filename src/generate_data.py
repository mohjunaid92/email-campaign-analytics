"""
Synthetic Data Generation Engine for Email Campaign Effectiveness Analysis
Project: MCA 2nd Year Data Analytics, ABES Engineering College
Author: Moh Junaid (Roll No: 250320140094)
Mentor: Mr. Dinesh
Target Database: SQLite (data/app.db) + Excel + CSVs
"""

import os
import random
import sqlite3
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Set deterministic seed
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# ---------------------------------------------------------
# 1. Master Campaign Data (dim_campaigns) - 25 campaigns
# ---------------------------------------------------------
CAMPAIGN_CATEGORIES = [
    'Product Update',
    'Webinar Invite',
    'Newsletter',
    'Promotional Discount'
]

CAMPAIGN_TEMPLATES = [
    ("Q1 Product Innovations & Feature Roundup", "Product Update", "Discover What's New in Nexura Cloud v4.2", 0, 0, 850.0),
    ("Mastering Enterprise Multi-Cloud Security", "Webinar Invite", "Join Live: Defending B2B SaaS Against Modern Cyber Threats", 0, 1, 1200.0),
    ("The B2B Tech Leader - March Edition", "Newsletter", "March Tech Insights: AI Trends Reshaping Enterprise Workflows", 0, 0, 450.0),
    ("Spring Cloud Optimization Sprint - 25% Off", "Promotional Discount", "Exclusive Offer: Accelerate Your Cloud Migration Today!", 1, 1, 1500.0),
    ("Kubernetes Cost Optimization Framework", "Product Update", "Cut Container Costs by 35%: New DevOps Module Released", 0, 0, 950.0),
    ("C-Suite Breakfast RoundTable: FinTech Scale", "Webinar Invite", "Executive Invite: High-Volume Transaction Security in 2026", 1, 1, 1800.0),
    ("The B2B Tech Leader - April Edition", "Newsletter", "April Digest: Why Data Observability Outpaces Monitoring", 0, 0, 450.0),
    ("Special Q2 Onboarding Acceleration Discount", "Promotional Discount", "Limited Time: Save 20% on Nexura Managed Support", 0, 1, 1350.0),
    ("Zero Trust Architecture Whitepaper Launch", "Product Update", "Download: The 2026 Enterprise Zero-Trust Implementation Playbook", 1, 0, 1100.0),
    ("AI-Driven APM & Log Telemetry Deep Dive", "Webinar Invite", "Hands-on Workshop: Eliminating MTTR with Predictive Telemetry", 0, 0, 1400.0),
    ("The B2B Tech Leader - May Edition", "Newsletter", "May Insights: Navigating Compliance in Multi-Tenant Environments", 0, 0, 450.0),
    ("Mid-Year Cloud Infrastructure Modernization", "Promotional Discount", "Mid-Year Boost: Double Your Dedicated Server Bandwidth Free", 0, 1, 1600.0),
    ("Microservices Observability Suite Release", "Product Update", "Announcing Nexura Trace: Full-Stack Microservices Telemetry", 1, 0, 1250.0),
    ("Enterprise DevOps Automation Summit", "Webinar Invite", "Free Virtual Summit: Scaling CI/CD Pipelines to 1,000 Deploys/Day", 0, 0, 2000.0),
    ("The B2B Tech Leader - June Edition", "Newsletter", "June Review: Real-World Lessons from Hybrid Cloud Transformations", 0, 0, 450.0),
    ("Flash Sale: 48-Hour Cloud Security Audit", "Promotional Discount", "Urgent: Claim Your Complimentary Infrastructure Threat Assessment", 0, 1, 1750.0),
    ("Next-Gen API Gateway & Mesh Architecture", "Product Update", "Upgrade Alert: Sub-Millisecond Latency with Nexura Mesh", 0, 0, 1050.0),
    ("Demystifying SOC2 & ISO27001 Readiness", "Webinar Invite", "Interactive Webinar: Streamlining Enterprise Audit Compliance", 1, 0, 1300.0),
    ("The B2B Tech Leader - July Edition", "Newsletter", "July Brief: How Platform Engineering Is Replacing Traditional Ops", 0, 0, 450.0),
    ("Q3 Cloud Migration Incentive Program", "Promotional Discount", "Switch to Nexura: Get $5,000 in Migration Cloud Credits", 1, 1, 2200.0),
    ("Serverless Database Auto-Scaler v2.0", "Product Update", "Meet Auto-Scaler v2.0: Instant Zero-to-Peak Provisioning", 0, 0, 900.0),
    ("Architecting High-Availability Systems", "Webinar Invite", "Live Masterclass: Designing 99.999% SLA Cloud Topologies", 0, 0, 1500.0),
    ("The B2B Tech Leader - August Edition", "Newsletter", "August Perspectives: The Future of Sovereign Cloud in India", 0, 0, 450.0),
    ("Q3 Cloud DevOps Suite Release [Variant A]", "Product Update", "Upgrade to DevOps Suite: Modern Tools for Fast Delivery", 0, 0, 1200.0),
    ("Q3 Cloud DevOps Suite Release [Variant B]", "Product Update", "Hi {{first_name}}, Boost Your Team's Deploy Velocity by 40%", 1, 1, 1200.0)
]

def generate_campaigns():
    campaigns = []
    start_date = datetime(2026, 1, 5)
    
    for idx, (title, cat, subj, has_p, has_u, cost) in enumerate(CAMPAIGN_TEMPLATES, start=1):
        # Spaced every 8-10 days
        send_dt = start_date + timedelta(days=(idx - 1) * 9, hours=random.choice([9, 10, 11, 14, 15, 16]))
        day_name = send_dt.strftime("%A")
        
        # A/B variant indicator
        if "Variant A" in title:
            variant = "A"
        elif "Variant B" in title:
            variant = "B"
        else:
            variant = "None"
            
        campaigns.append({
            "campaign_id": idx,
            "campaign_name": title,
            "campaign_category": cat,
            "subject_line": subj,
            "subject_char_length": len(subj),
            "has_personalization": has_p,
            "has_urgency": has_u,
            "campaign_variant": variant,
            "send_date": send_dt.strftime("%Y-%m-%d"),
            "send_day_name": day_name,
            "send_hour": send_dt.hour,
            "budget_cost": cost
        })
    return pd.DataFrame(campaigns)

# ---------------------------------------------------------
# 2. Master Recipient Data (dim_recipients) - 150 contacts
# ---------------------------------------------------------
INDIAN_FIRST_NAMES = [
    "Aarav", "Priya", "Rohan", "Ananya", "Vikram", "Neha", "Rahul", "Sneha",
    "Aditya", "Pooja", "Amit", "Kavita", "Siddharth", "Divya", "Rajesh",
    "Ritu", "Gaurav", "Swati", "Karan", "Meera", "Manoj", "Shweta", "Arjun",
    "Isha", "Naveen", "Tanvi", "Suresh", "Sunita", "Harsh", "Deepika"
]

INDIAN_LAST_NAMES = [
    "Sharma", "Patel", "Verma", "Iyer", "Singh", "Gupta", "Nair", "Joshi",
    "Kumar", "Reddy", "Mehta", "Bose", "Chawla", "Deshmukh", "Choudhury",
    "Pillai", "Agarwal", "Bhatia", "Malhotra", "Saxena", "Menon", "Rao",
    "Chatterjee", "Mishra", "Pandey", "Kapoor", "Trivedi", "Sengupta"
]

CORPORATE_DOMAINS = [
    ("tcs-technologies.in", "Corporate"),
    ("infosys-global.com", "Corporate"),
    ("wipro-systems.com", "Corporate"),
    ("hcl-enterprise.in", "Corporate"),
    ("techmahindra-cloud.com", "Corporate"),
    ("paytm-payments.in", "Corporate"),
    ("zomato-logistics.com", "Corporate"),
    ("swiggy-delivery.in", "Corporate"),
    ("zerodha-trading.com", "Corporate"),
    ("razorpay-solutions.in", "Corporate"),
    ("delhivery-freight.com", "Corporate"),
    ("policybazaar-group.in", "Corporate"),
    ("freshworks-saas.com", "Corporate"),
    ("postman-api.io", "Corporate"),
    ("inmobi-media.com", "Corporate"),
    ("techcorp-old.in", "Corporate"), # problematic bounce domain
    ("gmail.com", "Public Webmail"),
    ("yahoo.co.in", "Public Webmail")
]

ACCOUNT_TIERS = ["Enterprise", "Mid-Market", "SMB", "Startup"]
TIER_WEIGHTS = [0.25, 0.35, 0.25, 0.15]

INDUSTRIES = ["SaaS", "FinTech", "Healthcare", "E-Commerce", "IT Services"]

def generate_recipients(n=150):
    recipients = []
    base_onboard = datetime(2025, 6, 1)
    
    for i in range(1, n + 1):
        fn = random.choice(INDIAN_FIRST_NAMES)
        ln = random.choice(INDIAN_LAST_NAMES)
        dom, dom_type = random.choice(CORPORATE_DOMAINS)
        email = f"{fn.lower()}.{ln.lower()}{random.randint(10, 99)}@{dom}"
        
        tier = np.random.choice(ACCOUNT_TIERS, p=TIER_WEIGHTS)
        ind = random.choice(INDUSTRIES)
        country = "India"
        created_dt = base_onboard + timedelta(days=random.randint(0, 180), hours=random.randint(8, 18))
        
        recipients.append({
            "recipient_id": i,
            "email_address": email,
            "recipient_domain": dom,
            "domain_type": dom_type,
            "account_tier": tier,
            "industry": ind,
            "country": country,
            "created_at": created_dt.strftime("%Y-%m-%d %H:%M:%S")
        })
    return pd.DataFrame(recipients)

# ---------------------------------------------------------
# 3. Core Dispatches Fact (fact_email_dispatches) - 375 rows
# ---------------------------------------------------------
def generate_dispatches(df_campaigns, df_recipients):
    dispatches = []
    dispatch_id = 1
    
    # 25 campaigns * 15 recipients = 375 dispatches
    for _, camp in df_campaigns.iterrows():
        c_id = int(camp["campaign_id"])
        c_cat = camp["campaign_category"]
        c_day = camp["send_day_name"]
        c_hour = int(camp["send_hour"])
        has_p = int(camp["has_personalization"])
        variant = camp["campaign_variant"]
        send_date_str = camp["send_date"]
        
        target_recipients = df_recipients.sample(n=15, replace=False, random_state=c_id + 42)
        
        for _, rec in target_recipients.iterrows():
            r_id = int(rec["recipient_id"])
            r_dom = rec["recipient_domain"]
            r_tier = rec["account_tier"]
            
            send_dt = datetime.strptime(f"{send_date_str} {c_hour:02d}:00:00", "%Y-%m-%d %H:%M:%S") + timedelta(minutes=random.randint(0, 45))
            
            # --- PATTERN 5: Domain Bounce Hygiene ---
            # 'techcorp-old.in' has 50% hard bounce rate; others < 2%
            if r_dom == "techcorp-old.in" and random.random() < 0.50:
                del_status = "Bounced"
                b_type = "Hard"
                b_reason = "DNS host domain defunct / mailbox unavailable"
            elif random.random() < 0.02:
                del_status = "Bounced"
                b_type = random.choice(["Soft", "Hard"])
                b_reason = "Mailbox full / Server timeout" if b_type == "Soft" else "User unknown"
            else:
                del_status = "Delivered"
                b_type = "None"
                b_reason = None
            
            is_open = 0
            open_dt_str = None
            total_opens = 0
            is_click = 0
            click_dt_str = None
            total_clicks = 0
            is_unsub = 0
            unsub_dt_str = None
            
            if del_status == "Delivered":
                # --- PATTERN 1: Send-Time Peak Engagement ---
                # Tuesday & Thursday 10am-3pm have higher open base (0.38) vs other times (0.24)
                base_open_prob = 0.28
                if c_day in ["Tuesday", "Thursday"] and c_hour in [10, 11, 14, 15]:
                    base_open_prob += 0.16
                elif c_day in ["Friday", "Saturday", "Sunday"]:
                    base_open_prob -= 0.10
                
                # --- PATTERN 4: A/B Testing Variant B superiority ---
                if variant == "B":
                    base_open_prob += 0.20
                elif variant == "A":
                    base_open_prob -= 0.05
                
                # Personalization boost
                if has_p == 1:
                    base_open_prob += 0.06
                    
                # Account Tier variation (Pattern 2)
                if r_tier == "Startup":
                    base_open_prob += 0.08
                elif r_tier == "Enterprise":
                    base_open_prob -= 0.03
                    
                base_open_prob = max(0.08, min(0.75, base_open_prob))
                
                if random.random() < base_open_prob:
                    is_open = 1
                    open_dt = send_dt + timedelta(minutes=random.randint(5, 720))
                    open_dt_str = open_dt.strftime("%Y-%m-%d %H:%M:%S")
                    total_opens = np.random.choice([1, 2, 3, 4], p=[0.55, 0.28, 0.12, 0.05])
                    
                    # --- PATTERN 3: CTOR Content Quality ---
                    # Webinar Invite & Product Update have high CTOR (0.42); Promo Discount has 0.18
                    base_click_prob = 0.30
                    if c_cat in ["Webinar Invite", "Product Update"]:
                        base_click_prob = 0.44
                    elif c_cat == "Promotional Discount":
                        base_click_prob = 0.18
                        
                    if random.random() < base_click_prob:
                        is_click = 1
                        click_dt = open_dt + timedelta(minutes=random.randint(1, 45))
                        click_dt_str = click_dt.strftime("%Y-%m-%d %H:%M:%S")
                        total_clicks = np.random.choice([1, 2, 3], p=[0.65, 0.25, 0.10])
                
                # Unsubscribe behavior
                if is_open == 1 and random.random() < 0.012:
                    is_unsub = 1
                    unsub_dt_str = open_dt_str
            
            dispatches.append({
                "dispatch_id": dispatch_id,
                "campaign_id": c_id,
                "recipient_id": r_id,
                "dispatch_timestamp": send_dt.strftime("%Y-%m-%d %H:%M:%S"),
                "delivery_status": del_status,
                "bounce_type": b_type,
                "bounce_reason": b_reason,
                "is_opened": is_open,
                "first_open_timestamp": open_dt_str,
                "total_opens_count": total_opens,
                "is_clicked": is_click,
                "first_click_timestamp": click_dt_str,
                "total_clicks_count": total_clicks,
                "is_unsubscribed": is_unsub,
                "unsubscribe_timestamp": unsub_dt_str
            })
            dispatch_id += 1

    df_d = pd.DataFrame(dispatches)

    # Inject data quality issues (Outliers & Missing values)
    # Outlier: Automated security scanner bot on row 12
    df_d.at[12, "total_opens_count"] = 42
    df_d.at[12, "is_opened"] = 1
    
    # 2-3% missing values in bounce_reason for bounced records
    for i in range(len(df_d)):
        if df_d.at[i, "delivery_status"] == "Bounced" and random.random() < 0.25:
            df_d.at[i, "bounce_reason"] = None

    return df_d

# ---------------------------------------------------------
# 4. Financial Conversions Fact (fact_conversions) - ~35 rows
# ---------------------------------------------------------
def generate_conversions(df_dispatches, df_recipients):
    conversions = []
    conv_id = 1
    
    rec_tier_map = dict(zip(df_recipients["recipient_id"], df_recipients["account_tier"]))
    clicked_dispatches = df_dispatches[df_dispatches["is_clicked"] == 1]
    
    for _, disp in clicked_dispatches.iterrows():
        r_id = int(disp["recipient_id"])
        c_id = int(disp["campaign_id"])
        d_id = int(disp["dispatch_id"])
        tier = rec_tier_map.get(r_id, "Mid-Market")
        
        # --- PATTERN 2: Deal Values by Tier ---
        # Conversion likelihood given click ~ 65%
        if random.random() < 0.68:
            if tier == "Enterprise":
                deal = round(float(np.random.uniform(4800, 8900)), 2)
                stage = np.random.choice(["Opportunity Won", "Closed Contract"], p=[0.35, 0.65])
            elif tier == "Mid-Market":
                deal = round(float(np.random.uniform(2200, 4400)), 2)
                stage = np.random.choice(["SQL", "Opportunity Won", "Closed Contract"], p=[0.25, 0.45, 0.30])
            elif tier == "SMB":
                deal = round(float(np.random.uniform(700, 1600)), 2)
                stage = np.random.choice(["MQL", "SQL", "Closed Contract"], p=[0.3, 0.4, 0.3])
            else: # Startup
                deal = round(float(np.random.uniform(350, 900)), 2)
                stage = np.random.choice(["MQL", "SQL", "Opportunity Won"], p=[0.4, 0.4, 0.2])
                
            conv_dt = datetime.strptime(disp["first_click_timestamp"], "%Y-%m-%d %H:%M:%S") + timedelta(days=random.randint(1, 12), hours=random.randint(1, 6))
            
            conversions.append({
                "conversion_id": conv_id,
                "dispatch_id": d_id,
                "campaign_id": c_id,
                "recipient_id": r_id,
                "conversion_timestamp": conv_dt.strftime("%Y-%m-%d %H:%M:%S"),
                "deal_value": deal,
                "funnel_stage": stage
            })
            conv_id += 1

    df_c = pd.DataFrame(conversions)
    # Inject 1 outlier enterprise deal
    if len(df_c) > 0:
        df_c.at[0, "deal_value"] = 28500.00
        df_c.at[0, "funnel_stage"] = "Closed Contract"
        
    return df_c

# ---------------------------------------------------------
# 5. Populate SQLite Database with schema.sql
# ---------------------------------------------------------
def populate_sqlite(df_camp, df_rec, df_disp, df_conv):
    db_path = os.path.join(DATA_DIR, "app.db")
    schema_path = os.path.join(DATA_DIR, "schema.sql")
    
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    with open(schema_path, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)
    
    # Insert records
    df_camp.to_sql("dim_campaigns", conn, if_exists="append", index=False)
    df_rec.to_sql("dim_recipients", conn, if_exists="append", index=False)
    df_disp.to_sql("fact_email_dispatches", conn, if_exists="append", index=False)
    df_conv.to_sql("fact_conversions", conn, if_exists="append", index=False)
    
    conn.commit()
    
    # Run Foreign Key Check
    fk_errors = cursor.execute("PRAGMA foreign_key_check;").fetchall()
    
    # Fetch 39-column joined view
    df_view = pd.read_sql_query("SELECT * FROM vw_campaign_effectiveness_analytics;", conn)
    conn.close()
    
    return db_path, fk_errors, df_view

# ---------------------------------------------------------
# 6. Main Orchestrator & Exporter
# ---------------------------------------------------------
def main():
    print("="*60)
    print("Executing Synthetic Data Generation Engine (Seed 42)...")
    print("="*60)
    
    df_campaigns = generate_campaigns()
    df_recipients = generate_recipients(n=150)
    df_dispatches = generate_dispatches(df_campaigns, df_recipients)
    df_conversions = generate_conversions(df_dispatches, df_recipients)
    
    print(f"Generated dim_campaigns: {len(df_campaigns)} rows")
    print(f"Generated dim_recipients: {len(df_recipients)} rows")
    print(f"Generated fact_email_dispatches: {len(df_dispatches)} rows")
    print(f"Generated fact_conversions: {len(df_conversions)} rows")
    
    # Export CSVs
    df_campaigns.to_csv(os.path.join(DATA_DIR, "dim_campaigns.csv"), index=False)
    df_recipients.to_csv(os.path.join(DATA_DIR, "dim_recipients.csv"), index=False)
    df_dispatches.to_csv(os.path.join(DATA_DIR, "fact_email_dispatches.csv"), index=False)
    df_conversions.to_csv(os.path.join(DATA_DIR, "fact_conversions.csv"), index=False)
    print("Exported individual table CSV files to data/")
    
    # Populate SQLite
    db_path, fk_errors, df_view = populate_sqlite(df_campaigns, df_recipients, df_dispatches, df_conversions)
    print(f"Populated SQLite database: {db_path}")
    print(f"Foreign Key Violations: {len(fk_errors)} (Must be 0)")
    print(f"Joined View vw_campaign_effectiveness_analytics: {len(df_view)} rows, {df_view.shape[1]} columns")
    
    # Export Joined View CSV
    df_view.to_csv(os.path.join(DATA_DIR, "vw_campaign_effectiveness_analytics.csv"), index=False)
    
    # Export Multi-Sheet Excel
    excel_path = os.path.join(DATA_DIR, "email_campaign_analytics_data.xlsx")
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        df_campaigns.to_excel(writer, sheet_name="dim_campaigns", index=False)
        df_recipients.to_excel(writer, sheet_name="dim_recipients", index=False)
        df_dispatches.to_excel(writer, sheet_name="fact_email_dispatches", index=False)
        df_conversions.to_excel(writer, sheet_name="fact_conversions", index=False)
        df_view.to_excel(writer, sheet_name="vw_analytics_view", index=False)
    print(f"Exported master multi-sheet Excel file: {excel_path}")
    
    print("="*60)
    print("STEP 10 Dataset Generation Complete!")
    print("="*60)

if __name__ == "__main__":
    main()
