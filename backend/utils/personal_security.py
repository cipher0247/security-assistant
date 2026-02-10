
privacy_checklists = {
    "facebook": [
        {"id": "fb1", "text": "Enable Two-Factor Authentication (2FA)", "desc": "Settings > Security and Login > Use two-factor authentication."},
        {"id": "fb2", "text": "Review 'Where You're Logged In'", "desc": "Settings > Security and Login. Log out of unrecognized devices."},
        {"id": "fb3", "text": "Limit Past Posts", "desc": "Settings > Privacy > Limit The Audience for Old Posts."},
        {"id": "fb4", "text": "Hide Friend List", "desc": "Settings > Privacy > Who can see your friends list? Set to 'Only me'."}
    ],
    "google": [
        {"id": "gg1", "text": "Run Security Checkup", "desc": "Go to myaccount.google.com/security-checkup."},
        {"id": "gg2", "text": "Manage Third-Party Access", "desc": "Security > Third-party apps with account access. Remove unused apps."},
        {"id": "gg3", "text": "Turn on 2-Step Verification", "desc": "Security > Signing in to Google > 2-Step Verification."},
        {"id": "gg4", "text": "Auto-Delete Activity", "desc": "Data & Privacy > Web & App Activity > Auto-delete."}
    ],
    "instagram": [
        {"id": "ig1", "text": "Set Account to Private", "desc": "Settings > Privacy > Private Account."},
        {"id": "ig2", "text": "Enable 2FA", "desc": "Settings > Security > Two-Factor Authentication."},
        {"id": "ig3", "text": "Check Login Activity", "desc": "Settings > Security > Login Activity. Log out of suspicious locations."},
        {"id": "ig4", "text": "Restrict Story Sharing", "desc": "Settings > Privacy > Story. Disable 'Allow Sharing to Messages'."}
    ],
    "linkedin": [
        {"id": "li1", "text": "Turn on Two-Step Verification", "desc": "Settings & Privacy > Sign in & security > Two-step verification."},
        {"id": "li2", "text": "Review Active Sessions", "desc": "Settings & Privacy > Sign in & security > Where you're signed in."},
        {"id": "li3", "text": "Hide Profile from Search Engines", "desc": "Visibility > Edit your public profile > Edit Visibility > Public Profile Visibility > Off."}
    ]
}

scam_decision_tree = {
    "start": {
        "question": "How did you receive the communication?",
        "options": [
            {"text": "Email", "next": "email_check"},
            {"text": "SMS / Text", "next": "sms_check"},
            {"text": "Phone Call", "next": "call_check"},
            {"text": "Social Media Message", "next": "social_check"}
        ]
    },
    "email_check": {
        "question": "Does the email ask for urgent action (e.g., 'Account suspended', 'Pay now')?",
        "options": [
            {"text": "Yes, it creates urgency", "next": "sender_check"},
            {"text": "No, it seems informational", "next": "link_check"}
        ]
    },
    "sender_check": {
        "question": "Check the sender address carefully. Does it match the official domain perfectly? (e.g., support@paypal.com vs support@paypa1.com)",
        "options": [
            {"text": "It looks weird / misspelled", "next": "result_scam"},
            {"text": "It looks official", "next": "link_check"}
        ]
    },
    "link_check": {
        "question": "Hover over links (don't click). do they point to the expected official website?",
        "options": [
            {"text": "No, they point to random URLs", "next": "result_scam"},
            {"text": "Yes, they look correct", "next": "request_check"}
        ]
    },
    "request_check": {
        "question": "Are they asking for sensitive info (Password, SSN, Credit Card) or payment via Gift Cards/Crypto?",
        "options": [
            {"text": "Yes, asking for sensitive info/payment", "next": "result_scam"},
            {"text": "No, just general info", "next": "result_safe"}
        ]
    },
    # SMS Logic
    "sms_check": {
        "question": "Is it from an unknown number sending a link or asking for money?",
        "options": [
            {"text": "Yes", "next": "result_scam"},
            {"text": "No, it's a verification code I requested", "next": "result_safe"}
        ]
    },
    # Call Logic
    "call_check": {
        "question": "Is it a recorded message (robocall) or someone claiming to be from 'Tech Support' / 'IRS' / 'Police'?",
        "options": [
            {"text": "Yes, threatening legal action or virus", "next": "result_scam"},
            {"text": "No, it's a personal call", "next": "result_safe"}
        ]
    },
    # Social Logic
    "social_check": {
        "question": "Is a friend asking for money/emergency help, or a stranger offering 'easy money' / crypto investment?",
        "options": [
            {"text": "Yes, asking for money/crypto", "next": "verify_friend"},
            {"text": "No, just chatting", "next": "result_safe"}
        ]
    },
    "verify_friend": {
        "question": "Call the friend on their phone number. Did they confirm they sent it?",
        "options": [
            {"text": "No, they didn't send it (or I can't reach them)", "next": "result_scam"},
            {"text": "Yes, I spoke to them", "next": "result_safe"}
        ]
    },
    # Results
    "result_scam": {
        "result": "HIGH RISK: LIKELY A SCAM",
        "advice": "Do not reply, click links, or send money. Block the sender and report it.",
        "is_final": True
    },
    "result_safe": {
        "result": "LIKELY SAFE (But be cautious)",
        "advice": "Proceed with caution. If you are unsure, contact the organization directly through their official website.",
        "is_final": True
    }
}

hacked_symptoms = [
    {"id": "h1", "symptom": "Battery draining much faster than usual", "risk": 1},
    {"id": "h2", "symptom": "Phone/Laptop feels hot even when not in use", "risk": 1},
    {"id": "h3", "symptom": "Unknown apps appeared on my device", "risk": 3},
    {"id": "h4", "symptom": "Pop-ups ads appear even on home screen", "risk": 2},
    {"id": "h5", "symptom": "Friends receiving spam messages from me", "risk": 3},
    {"id": "h6", "symptom": "Passwords changed without my knowledge", "risk": 5},
    {"id": "h7", "symptom": "Mouse cursor moving by itself", "risk": 4},
    {"id": "h8", "symptom": "Antivirus disabled itself", "risk": 4}
]

digital_declutter_steps = [
    {"title": "Unsubscribe from Email Lists", "desc": "Search 'unsubscribe' in your inbox and clear out marketing emails you don't read."},
    {"title": "Delete Unused Apps", "desc": "Scroll through your phone. If you haven't used it in 3 months, delete it."},
    {"title": "Review Browser Extensions", "desc": "Remove extensions you don't recognize or use. They can track your browsing."},
    {"title": "Clear Old Downloads", "desc": "Delete files in your Downloads folder that you no longer need."},
    {"title": "Check 'Have I Been Pwned'", "desc": "See if your email was in a data breach and change passwords for affected accounts."},
    {"title": "Backup Photos & Documents", "desc": "Ensure your important memories are backed up (Cloud or External Drive)."},
    {"title": "Update Operations System", "desc": "Ensure your Phone and PC are running the latest updates."}
]
