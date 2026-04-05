"""
Email dataset for the Customer Email Triage environment.
30+ realistic customer support emails with ground-truth labels.
"""
from __future__ import annotations

from typing import Any, Dict, List
import random

# Each email dict has:
#   id, subject, body, sender, sender_tier, timestamp, thread_length,
#   previous_interactions, ground_truth: {priority, category, reply_keywords}
EMAILS: List[Dict[str, Any]] = [
    {
        "id": "em001",
        "subject": "URGENT: Production database is DOWN!!!",
        "body": (
            "Hi Support,\n\n"
            "Our entire production DB went down 20 minutes ago. We have 50,000 active users "
            "completely blocked. We are losing $10,000/minute in revenue. This is catastrophic.\n\n"
            "Error: connection pool exhausted, all 500 connections maxed out.\n"
            "DB host: db-prod-01.internal\n\n"
            "Please escalate IMMEDIATELY to your on-call DBA team.\n\n"
            "- CTO, AcmeCorp"
        ),
        "sender": "cto@acmecorp.com",
        "sender_tier": "enterprise",
        "timestamp": "2024-03-15T09:02:00Z",
        "thread_length": 1,
        "previous_interactions": 12,
        "ground_truth": {
            "priority": "urgent",
            "category": "technical",
            "reply_keywords": ["escalate", "on-call", "investigating", "priority", "team", "connection"],
        },
    },
    {
        "id": "em002",
        "subject": "Invoice #8821 charged twice",
        "body": (
            "Hello,\n\n"
            "I noticed my credit card was charged $299 twice this month for invoice #8821. "
            "I'd like a refund for the duplicate charge.\n\n"
            "Transaction dates: March 1 and March 2.\n\n"
            "Thanks,\nSarah"
        ),
        "sender": "sarah.johnson@gmail.com",
        "sender_tier": "pro",
        "timestamp": "2024-03-15T10:15:00Z",
        "thread_length": 1,
        "previous_interactions": 2,
        "ground_truth": {
            "priority": "high",
            "category": "billing",
            "reply_keywords": ["refund", "duplicate", "charge", "invoice", "process", "apologize"],
        },
    },
    {
        "id": "em003",
        "subject": "How do I export my data?",
        "body": (
            "Hi,\n\n"
            "Quick question — I'd like to export all my project data as a CSV. "
            "Is there a way to do that in the dashboard?\n\n"
            "Thanks!"
        ),
        "sender": "mark.t@outlook.com",
        "sender_tier": "free",
        "timestamp": "2024-03-15T11:30:00Z",
        "thread_length": 1,
        "previous_interactions": 0,
        "ground_truth": {
            "priority": "low",
            "category": "general",
            "reply_keywords": ["export", "csv", "settings", "dashboard", "data", "download"],
        },
    },
    {
        "id": "em004",
        "subject": "API rate limit hit — need increase",
        "body": (
            "Hello,\n\n"
            "We've been hitting the 1,000 req/min API rate limit and it's starting to affect "
            "our integration in production. We need an emergency limit increase to 10,000 req/min.\n\n"
            "Our account ID is ENT-44201. Please expedite.\n\n"
            "Best,\nDev Team at TechFlow"
        ),
        "sender": "dev@techflow.io",
        "sender_tier": "enterprise",
        "timestamp": "2024-03-15T08:45:00Z",
        "thread_length": 3,
        "previous_interactions": 8,
        "ground_truth": {
            "priority": "high",
            "category": "technical",
            "reply_keywords": ["rate limit", "increase", "account", "team", "review", "enterprise"],
        },
    },
    {
        "id": "em005",
        "subject": "I want a refund — this product is terrible",
        "body": (
            "I've been using your product for 3 months and it's been a complete disaster. "
            "The UI is confusing, support is slow, and nothing works as advertised. "
            "I want a FULL refund of my annual subscription ($1,188). This is ridiculous.\n\n"
            "- Angry customer"
        ),
        "sender": "disgruntled@hotmail.com",
        "sender_tier": "pro",
        "timestamp": "2024-03-15T14:00:00Z",
        "thread_length": 1,
        "previous_interactions": 5,
        "ground_truth": {
            "priority": "high",
            "category": "refunds",
            "reply_keywords": ["refund", "sorry", "experience", "annual", "process", "understand"],
        },
    },
    {
        "id": "em006",
        "subject": "Win a $1000 Amazon gift card — LIMITED TIME",
        "body": (
            "Congratulations! You have been selected to win a $1000 Amazon gift card! "
            "Click the link below to claim your prize!! This offer expires in 24 hours.\n\n"
            "CLAIM NOW: http://totally-legit-prizes.xyz/claim?ref=8821"
        ),
        "sender": "noreply@totally-legit-prizes.xyz",
        "sender_tier": "free",
        "timestamp": "2024-03-15T07:22:00Z",
        "thread_length": 1,
        "previous_interactions": 0,
        "ground_truth": {
            "priority": "spam",
            "category": "spam",
            "reply_keywords": [],
        },
    },
    {
        "id": "em007",
        "subject": "Cannot login to my account - password reset not working",
        "body": (
            "Hi,\n\n"
            "I've tried resetting my password 5 times today and I'm not receiving the reset email. "
            "I've checked my spam folder. My account email is user@company.com and I need access "
            "urgently for a client presentation in 2 hours.\n\n"
            "Please help!\n- Alex"
        ),
        "sender": "alex.wu@company.com",
        "sender_tier": "pro",
        "timestamp": "2024-03-15T09:30:00Z",
        "thread_length": 1,
        "previous_interactions": 3,
        "ground_truth": {
            "priority": "urgent",
            "category": "account",
            "reply_keywords": ["password", "reset", "email", "account", "send", "immediately"],
        },
    },
    {
        "id": "em008",
        "subject": "Feature request: dark mode",
        "body": (
            "Hey team,\n\n"
            "Love the product but would really appreciate a dark mode option! "
            "My eyes are burning after long sessions. Any chance this is on your roadmap?\n\n"
            "Cheers,\nJamie"
        ),
        "sender": "jamie@designstudio.co",
        "sender_tier": "free",
        "timestamp": "2024-03-15T13:00:00Z",
        "thread_length": 1,
        "previous_interactions": 1,
        "ground_truth": {
            "priority": "low",
            "category": "general",
            "reply_keywords": ["feature", "dark mode", "roadmap", "feedback", "consider", "thank"],
        },
    },
    {
        "id": "em009",
        "subject": "GDPR data deletion request",
        "body": (
            "To Whom It May Concern,\n\n"
            "Pursuant to Article 17 of the GDPR, I am formally requesting the deletion of all "
            "personal data associated with my account (email: priya.m@example.eu). "
            "Please confirm deletion within the legally mandated 30-day window and provide "
            "written confirmation.\n\n"
            "Regards,\nPriya Mehta"
        ),
        "sender": "priya.m@example.eu",
        "sender_tier": "free",
        "timestamp": "2024-03-15T15:00:00Z",
        "thread_length": 1,
        "previous_interactions": 0,
        "ground_truth": {
            "priority": "high",
            "category": "compliance",
            "reply_keywords": ["GDPR", "deletion", "data", "confirm", "30 days", "compliance", "right"],
        },
    },
    {
        "id": "em010",
        "subject": "Upgrade from Pro to Enterprise — pricing question",
        "body": (
            "Hi,\n\n"
            "We're growing fast and considering upgrading from Pro to Enterprise. "
            "Can you send me the Enterprise pricing sheet and a comparison of plan features?\n\n"
            "We have 45 users currently.\n\nThanks,\nRobert Chen, VP Engineering"
        ),
        "sender": "rchen@startup.io",
        "sender_tier": "pro",
        "timestamp": "2024-03-15T10:45:00Z",
        "thread_length": 1,
        "previous_interactions": 4,
        "ground_truth": {
            "priority": "medium",
            "category": "billing",
            "reply_keywords": ["enterprise", "pricing", "upgrade", "features", "plan", "team", "send"],
        },
    },
    {
        "id": "em011",
        "subject": "Data sync failing since this morning",
        "body": (
            "Hello,\n\n"
            "Our Salesforce sync has been failing since 6 AM UTC. We're getting error code E-5021: "
            "'OAuth token refresh failed'. This is blocking our sales team from updating records.\n\n"
            "Account: PRO-78234. Affected users: 12.\n\nPlease advise.\n\n- IT Ops"
        ),
        "sender": "it-ops@retailco.com",
        "sender_tier": "pro",
        "timestamp": "2024-03-15T09:15:00Z",
        "thread_length": 2,
        "previous_interactions": 6,
        "ground_truth": {
            "priority": "high",
            "category": "technical",
            "reply_keywords": ["OAuth", "sync", "token", "investigate", "error", "Salesforce", "refresh"],
        },
    },
    {
        "id": "em012",
        "subject": "Hi :) just saying thanks!",
        "body": (
            "Hey!\n\n"
            "Just wanted to drop a note to say your support team was AMAZING last week. "
            "Especially Priya — she went above and beyond to help me figure out the API. "
            "Keep up the great work!\n\n— Marco"
        ),
        "sender": "marco.f@gmail.com",
        "sender_tier": "free",
        "timestamp": "2024-03-15T16:00:00Z",
        "thread_length": 1,
        "previous_interactions": 7,
        "ground_truth": {
            "priority": "low",
            "category": "general",
            "reply_keywords": ["thank", "appreciate", "team", "feedback", "wonderful"],
        },
    },
    {
        "id": "em013",
        "subject": "Missing features in latest update — considering cancellation",
        "body": (
            "Your latest update removed the bulk export feature we relied on heavily. "
            "This was a key feature for our workflow and its removal is unacceptable. "
            "We are considering cancelling our enterprise contract ($36,000/year) unless this "
            "is restored within 5 business days.\n\n- Eva, Head of Data Analytics"
        ),
        "sender": "eva.k@bigcorp.com",
        "sender_tier": "enterprise",
        "timestamp": "2024-03-15T11:00:00Z",
        "thread_length": 1,
        "previous_interactions": 20,
        "ground_truth": {
            "priority": "urgent",
            "category": "technical",
            "reply_keywords": ["restore", "feature", "export", "escalate", "priority", "understand", "team", "urgent"],
        },
    },
    {
        "id": "em014",
        "subject": "Can I get a receipt for my last payment?",
        "body": (
            "Hello,\n\nCould you send me a receipt/invoice for my last payment? "
            "I need it for expense reporting.\n\nThanks!"
        ),
        "sender": "finance@smallbiz.net",
        "sender_tier": "pro",
        "timestamp": "2024-03-15T12:00:00Z",
        "thread_length": 1,
        "previous_interactions": 1,
        "ground_truth": {
            "priority": "low",
            "category": "billing",
            "reply_keywords": ["invoice", "receipt", "send", "payment", "attached", "email"],
        },
    },
    {
        "id": "em015",
        "subject": "Security incident — unauthorized access to our account",
        "body": (
            "URGENT: We have detected unauthorized access to our organization's account. "
            "Two admin users were deleted and our API keys were rotated without our knowledge. "
            "This happened between 2-3 AM UTC today. Please immediately:\n"
            "1. Freeze our account\n"
            "2. Provide access logs\n"
            "3. Escalate to your security team\n\n"
            "Account: ENT-90011\n\n— CISO, GlobalBank Ltd"
        ),
        "sender": "ciso@globalbank.com",
        "sender_tier": "enterprise",
        "timestamp": "2024-03-15T03:45:00Z",
        "thread_length": 1,
        "previous_interactions": 34,
        "ground_truth": {
            "priority": "urgent",
            "category": "compliance",
            "reply_keywords": ["security", "freeze", "logs", "escalate", "incident", "team", "investigate", "immediately"],
        },
    },
    {
        "id": "em016",
        "subject": "Discount for non-profit organizations?",
        "body": (
            "Hello,\n\nWe're a registered non-profit (501c3) and would love to use your platform. "
            "Do you offer a non-profit discount or a free tier for charities?\n\n"
            "Best,\nLisa — Community Health Connect"
        ),
        "sender": "lisa@communityhealthconnect.org",
        "sender_tier": "free",
        "timestamp": "2024-03-15T14:30:00Z",
        "thread_length": 1,
        "previous_interactions": 0,
        "ground_truth": {
            "priority": "medium",
            "category": "billing",
            "reply_keywords": ["nonprofit", "discount", "program", "apply", "team", "special"],
        },
    },
    {
        "id": "em017",
        "subject": "Your amazing offer exclusive to you!!!",
        "body": (
            "Hi there! You've been pre-approved for a $50,000 business loan! "
            "No credit check needed. Reply with your SSN and bank account details to claim!"
        ),
        "sender": "offers@quick-money-now.biz",
        "sender_tier": "free",
        "timestamp": "2024-03-15T06:00:00Z",
        "thread_length": 1,
        "previous_interactions": 0,
        "ground_truth": {
            "priority": "spam",
            "category": "spam",
            "reply_keywords": [],
        },
    },
    {
        "id": "em018",
        "subject": "Webhook events not being delivered",
        "body": (
            "Hi support,\n\n"
            "Our webhook endpoint has not received any events for the past 6 hours. "
            "Endpoint: https://api.ourapp.com/webhooks/inbound\n"
            "We've verified our endpoint is responding 200 OK to test pings.\n"
            "Events affected: payment.completed, invoice.created\n\n"
            "Please investigate. This is blocking our payment reconciliation process."
        ),
        "sender": "backend@fintech-co.com",
        "sender_tier": "pro",
        "timestamp": "2024-03-15T13:30:00Z",
        "thread_length": 2,
        "previous_interactions": 9,
        "ground_truth": {
            "priority": "high",
            "category": "technical",
            "reply_keywords": ["webhook", "events", "investigate", "endpoint", "delivery", "team", "check"],
        },
    },
    {
        "id": "em019",
        "subject": "Accidental double subscription — please cancel one",
        "body": (
            "Hi,\n\nI accidentally created two subscriptions last week. "
            "I only need one. Please cancel subscription ID SUB-44512 and process a refund "
            "for the unused period.\n\nThanks,\nTom"
        ),
        "sender": "tom.w@personal.com",
        "sender_tier": "free",
        "timestamp": "2024-03-15T11:45:00Z",
        "thread_length": 1,
        "previous_interactions": 2,
        "ground_truth": {
            "priority": "medium",
            "category": "billing",
            "reply_keywords": ["cancel", "refund", "subscription", "process", "account", "unused"],
        },
    },
    {
        "id": "em020",
        "subject": "Integration with Zapier — setup help needed",
        "body": (
            "Hey!\n\n"
            "I'm trying to connect your app to Zapier but can't find the API key in the dashboard. "
            "Where is it? Also, is there a Zapier template I can start from?\n\nThanks!"
        ),
        "sender": "user123@zapieruser.com",
        "sender_tier": "free",
        "timestamp": "2024-03-15T15:30:00Z",
        "thread_length": 1,
        "previous_interactions": 0,
        "ground_truth": {
            "priority": "low",
            "category": "technical",
            "reply_keywords": ["API key", "Zapier", "settings", "integration", "template", "help"],
        },
    },
    {
        "id": "em021",
        "subject": "SSO/SAML integration broken after our Azure AD migration",
        "body": (
            "Hi,\n\n"
            "We migrated our identity provider from Okta to Azure AD last night. "
            "Now none of our 200+ users can log in via SSO. Error: 'SAML assertion validation failed'.\n"
            "We've verified our metadata XML is correctly configured on Azure side.\n"
            "This is blocking all enterprise users. Need urgent assistance.\n\n"
            "Account ENT-33901, Contact: IT Director"
        ),
        "sender": "it-director@enterprise-client.com",
        "sender_tier": "enterprise",
        "timestamp": "2024-03-15T08:00:00Z",
        "thread_length": 4,
        "previous_interactions": 15,
        "ground_truth": {
            "priority": "urgent",
            "category": "technical",
            "reply_keywords": ["SAML", "SSO", "Azure", "metadata", "assist", "engineer", "escalate", "urgent"],
        },
    },
    {
        "id": "em022",
        "subject": "Request to transfer account ownership",
        "body": (
            "Hello,\n\n"
            "I am leaving the company and need to transfer ownership of our team account to "
            "my colleague Jane Smith (jane.smith@company.com). How do I do this?\n\n"
            "Thanks,\nDavid"
        ),
        "sender": "david.r@company.com",
        "sender_tier": "pro",
        "timestamp": "2024-03-15T12:30:00Z",
        "thread_length": 1,
        "previous_interactions": 3,
        "ground_truth": {
            "priority": "medium",
            "category": "account",
            "reply_keywords": ["transfer", "ownership", "account", "steps", "verify", "identity"],
        },
    },
    {
        "id": "em023",
        "subject": "Bulk license purchase — 500 seats",
        "body": (
            "Hi Sales,\n\n"
            "We're interested in purchasing 500 seats for our organization. "
            "Can you provide volume discounts and a dedicated account manager?\n\n"
            "Need approval doc by end of quarter.\n\n— Procurement, Mega Industries"
        ),
        "sender": "procurement@mega-industries.com",
        "sender_tier": "enterprise",
        "timestamp": "2024-03-15T10:00:00Z",
        "thread_length": 1,
        "previous_interactions": 2,
        "ground_truth": {
            "priority": "high",
            "category": "billing",
            "reply_keywords": ["volume", "discount", "account manager", "seats", "pricing", "enterprise", "quote"],
        },
    },
    {
        "id": "em024",
        "subject": "How does the free trial work?",
        "body": (
            "Hi,\n\n"
            "I'm considering signing up. Can you tell me how the free trial works? "
            "Is a credit card required? How many days?\n\nThanks!"
        ),
        "sender": "curious.user@yahoo.com",
        "sender_tier": "free",
        "timestamp": "2024-03-15T16:30:00Z",
        "thread_length": 1,
        "previous_interactions": 0,
        "ground_truth": {
            "priority": "low",
            "category": "general",
            "reply_keywords": ["trial", "free", "days", "credit card", "no", "features", "start"],
        },
    },
    {
        "id": "em025",
        "subject": "Compliance audit — need SOC 2 Type II report",
        "body": (
            "Dear Compliance Team,\n\n"
            "Our organization is conducting an annual vendor security audit. "
            "Please provide your most recent SOC 2 Type II report, data processing agreement (DPA), "
            "and penetration test summary.\n\n"
            "Deadline: 5 business days.\n\n"
            "— Vendor Risk Management, InsuranceCo"
        ),
        "sender": "vendor-risk@insuranceco.com",
        "sender_tier": "enterprise",
        "timestamp": "2024-03-15T09:00:00Z",
        "thread_length": 1,
        "previous_interactions": 1,
        "ground_truth": {
            "priority": "high",
            "category": "compliance",
            "reply_keywords": ["SOC 2", "report", "DPA", "compliance", "send", "team", "audit", "security"],
        },
    },
    {
        "id": "em026",
        "subject": "Re: [Ticket #44512] Still not resolved after 1 week",
        "body": (
            "I opened a ticket 7 days ago about my billing issue and NO ONE has responded. "
            "I've sent 3 follow-up emails. This is completely unacceptable customer service. "
            "I'm going to file a chargeback if this isn't resolved TODAY.\n\n— Furious customer"
        ),
        "sender": "mike.d@business.net",
        "sender_tier": "pro",
        "timestamp": "2024-03-15T14:45:00Z",
        "thread_length": 5,
        "previous_interactions": 7,
        "ground_truth": {
            "priority": "urgent",
            "category": "billing",
            "reply_keywords": ["apologize", "ticket", "resolve", "immediately", "priority", "escalate", "follow up"],
        },
    },
    {
        "id": "em027",
        "subject": "Suggestion: add keyboard shortcuts",
        "body": (
            "Hey, love the app! One thing that would make it even better — keyboard shortcuts. "
            "Specifically Cmd+K for search and Cmd+Enter to submit. Lots of power users would appreciate it!\n\n— Fan"
        ),
        "sender": "poweruser@mac.com",
        "sender_tier": "free",
        "timestamp": "2024-03-15T17:00:00Z",
        "thread_length": 1,
        "previous_interactions": 0,
        "ground_truth": {
            "priority": "low",
            "category": "general",
            "reply_keywords": ["suggestion", "keyboard", "roadmap", "consider", "thank", "feedback"],
        },
    },
    {
        "id": "em028",
        "subject": "API returning 500 errors intermittently",
        "body": (
            "Hello,\n\n"
            "We're getting intermittent HTTP 500 errors from POST /api/v2/records endpoint. "
            "Happens roughly 1 in 50 requests. Payload size doesn't seem to matter. "
            "Error message: 'Internal server error: null pointer at RecordService.java:244'.\n"
            "This is affecting our data ingestion pipeline.\n\n"
            "Request ID from last error: req_8821ab4d"
        ),
        "sender": "backend@data-company.com",
        "sender_tier": "pro",
        "timestamp": "2024-03-15T11:15:00Z",
        "thread_length": 2,
        "previous_interactions": 4,
        "ground_truth": {
            "priority": "high",
            "category": "technical",
            "reply_keywords": ["500", "error", "investigate", "request ID", "team", "intermittent", "report"],
        },
    },
    {
        "id": "em029",
        "subject": "Cancel my subscription",
        "body": (
            "Please cancel my subscription. I'm no longer using the service.\n\n— Thanks"
        ),
        "sender": "user.cancelling@email.com",
        "sender_tier": "free",
        "timestamp": "2024-03-15T18:00:00Z",
        "thread_length": 1,
        "previous_interactions": 1,
        "ground_truth": {
            "priority": "medium",
            "category": "billing",
            "reply_keywords": ["cancel", "process", "confirm", "refund", "account", "sad", "leave"],
        },
    },
    {
        "id": "em030",
        "subject": "Congratulations you are our lucky winner!!!",
        "body": (
            "You have WON a brand new iPhone 15 Pro Max!!! "
            "To claim your prize just pay $5.99 shipping. Offer expires in 1 hour!!!! "
            "Click: http://win-today.scam/claim"
        ),
        "sender": "winner@win-today.scam",
        "sender_tier": "free",
        "timestamp": "2024-03-15T05:00:00Z",
        "thread_length": 1,
        "previous_interactions": 0,
        "ground_truth": {
            "priority": "spam",
            "category": "spam",
            "reply_keywords": [],
        },
    },
]


def get_emails_for_task(task_name: str, seed: int | None = None) -> List[Dict[str, Any]]:
    """
    Return a shuffled subset of emails appropriate for the given task.
    - priority-triage: 10 emails, variety of priorities
    - full-routing: 12 emails, variety of categories
    - full-pipeline: 15 emails, all types including hard cases
    """
    rng = random.Random(seed)

    if task_name == "priority-triage":
        # Balanced across all 5 priority levels
        subset = EMAILS[:20]
        rng.shuffle(subset)
        return subset[:10]
    elif task_name == "full-routing":
        subset = EMAILS[:25]
        rng.shuffle(subset)
        return subset[:12]
    else:  # full-pipeline
        subset = EMAILS[:]
        rng.shuffle(subset)
        return subset[:15]
