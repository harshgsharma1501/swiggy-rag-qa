import re

def parse_financial_summary(text):

    financial_data = {}

    # -------- Net Profit/Loss after Tax --------
    match = re.search(
        r"Net Profit/\(Loss\) after Tax\s*\(?(-?\d+,?\d+)\)?\s*\(?(-?\d+,?\d+)\)?",
        text
    )

    if match:
        financial_data["net_loss_after_tax"] = {
            "FY24": match.group(1),
            "FY23": match.group(2)
        }

    # -------- Total Income --------
    match_income = re.search(
        r"Total Income\s*\n\s*(-?\d+,?\d+)\s*\n\s*(-?\d+,?\d+)",
        text
    )

    if match_income:
        financial_data["total_income"] = {
            "FY24": match_income.group(1),
            "FY23": match_income.group(2)
        }

    # -------- Total Expenses --------
    match_exp = re.search(
        r"Less: Total expenses including Depreciation\s*\n\s*(-?\d+,?\d+)\s*\n\s*(-?\d+,?\d+)",
        text
    )

    if match_exp:
        financial_data["total_expenses"] = {
            "FY24": match_exp.group(1),
            "FY23": match_exp.group(2)
        }

    # -------- Earnings Per Share --------
    match_eps = re.search(
        r"Earnings per share.*?\(?(-?\d+\.\d+)\)?\s*\(?(-?\d+\.\d+)\)?",
        text,
        re.DOTALL
    )

    if match_eps:
        financial_data["earnings_per_share"] = {
            "FY24": match_eps.group(1),
            "FY23": match_eps.group(2)
        }

    return financial_data