TEST_CASES = [

    # Financial
    {
        "question": "What was the standalone net loss after tax in FY24?",
        "expected": "(18,880)",
        "type": "financial"
    },
    {
        "question": "What was the consolidated total income in FY23?",
        "expected": "87,145",
        "type": "financial"
    },
    {
        "question": "What were the consolidated total expenses in FY24?",
        "expected": "139,474",
        "type": "financial"
    },
    {
        "question": "What was the earnings per share in FY23?",
        "expected": "(17.38)",
        "type": "financial"
    },

    # Governance
    {
        "question": "How many board meetings were held?",
        "expected": "6",
        "type": "narrative"
    },
    {
        "question": "Who is the Managing Director and Group CEO?",
        "expected": "Sriharsha Majety",
        "type": "narrative"
    },

    # Operational
    {
        "question": "How many cities does Swiggy operate in?",
        "expected": "653",
        "type": "narrative"
    },

    # Hallucination
    {
        "question": "Who is the CEO of Zomato?",
        "expected": "The information is not available",
        "type": "refusal"
    },
    {
        "question": "What was the total income in FY25?",
        "expected": "The information is not available",
        "type": "refusal"
    }
]