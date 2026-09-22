import re
from config import COURSE_FEES, QUESTIONS
 
def workflow(question):
    codes = re.findall(r"[A-Z]{2}\d{3}", question.upper())
    fees = [COURSE_FEES[code] for code in codes if code in COURSE_FEES]
 
    if not fees:
        return "Sorry, I can only answer questions about course fees."
 
    text = question.lower()
    if "total" in text:
        total = sum(fees)
        percent = re.search(r"(\d+)\s*%", text)
        if "scholarship" in text and percent:
            total = total * (1 - int(percent.group(1)) / 100)
        return f"Total fee: Rs. {total:,.0f}"
 
    if len(fees) == 1:
        return f"Fee for {codes[0]}: Rs. {fees[0]:,}"
 
    return "Sorry, I do not have a rule for this type of question."
 
if __name__ == "__main__":
    print("\n=== SYSTEM 2: RULE-BASED WORKFLOW (no LLM) ===\n")
    for question in QUESTIONS:
        print("Q:", question)
        print("A:", workflow(question))
        print("-" * 70)
