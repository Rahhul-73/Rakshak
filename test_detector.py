"""
Rakshak - Test Suite for Quick Scan & AI Scam Detection
Run this script to verify scam detection accuracy locally.
"""

import sys
from detector import quick_scan, detect_scam

TEST_CASES = [
    {
        "id": 1,
        "text": "Your Paytm KYC is pending. Update now: bit.ly/kyc",
        "expected_is_scam": True,
        "expected_type": "KYC Scam"
    },
    {
        "id": 2,
        "text": "Congratulations! You won ₹10 Lakh in KBC. Send ₹5000 for processing.",
        "expected_is_scam": True,
        "expected_type": "Lottery Scam"
    },
    {
        "id": 3,
        "text": "Hi, I sent ₹50,000 to you by mistake. Please return to 9876543210@upi",
        "expected_is_scam": True,
        "expected_type": "Wrong Transfer Scam"
    },
    {
        "id": 4,
        "text": "Hello, how are you? Are we meeting today at 5 PM?",
        "expected_is_scam": False,
        "expected_type": "None"
    },
    {
        "id": 5,
        "text": "आपका एसबीआई खाता ब्लॉक कर दिया गया है। तुरंत केवाईसी अपडेट करें। लिंक पर क्लिक करें।",
        "expected_is_scam": True,
        "expected_type": "KYC Scam"
    },
    {
        "id": 6,
        "text": "Share your SBI Netbanking OTP 849201 to complete your credit card approval instantly.",
        "expected_is_scam": True,
        "expected_type": "Phishing/OTP Scam"
    }
]

def run_tests():
    print("==================================================")
    print("🛡️ RAKSHAK SCAM DETECTOR LOCAL VERIFICATION TEST")
    print("==================================================\n")

    passed_count = 0

    for test in TEST_CASES:
        print(f"Test #{test['id']}: \"{test['text']}\"")
        
        # 1. Quick scan check
        qs_res = quick_scan(test["text"])
        print(f"   ⚡ Quick Scan Regex Triggered: {qs_res['is_suspicious']} (Detected Type: {qs_res['detected_type']})")

        # 2. Full scan check
        result = detect_scam(test["text"])
        is_scam = result.get("is_scam", False)
        risk = result.get("risk_score", "Unknown")
        scam_type = result.get("scam_type", "Unknown")
        explanation = result.get("explanation", "")

        print(f"   🤖 Full AI Detector -> Scam: {is_scam} | Risk: {risk} | Type: {scam_type}")
        print(f"   📖 Explanation: {explanation}")
        if result.get("hindi_warning"):
            print(f"   🔊 Hindi Warning: {result.get('hindi_warning')}")

        # Assertion evaluation
        match = (is_scam == test["expected_is_scam"])
        if match:
            print("   ✅ PASS\n")
            passed_count += 1
        else:
            print(f"   ❌ FAIL (Expected is_scam={test['expected_is_scam']})\n")

    print("==================================================")
    print(f"SUMMARY: Passed {passed_count}/{len(TEST_CASES)} tests.")
    print("==================================================")

    if passed_count == len(TEST_CASES):
        print("🎉 ALL TESTS PASSED SUCCESSFULLY!")
        sys.exit(0)
    else:
        print("⚠️ SOME TESTS FAILED. CHECK ENGINE LOGIC.")
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
