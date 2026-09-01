import json
from datetime import datetime

def main():
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    report = {
        "timestamp": now,
        "status": "success",
        "message": "Daily task executed successfully."
    }

    text = (
        f"Daily task report\n"
        f"Time: {report['timestamp']}\n"
        f"Status: {report['status']}\n"
        f"Message: {report['message']}\n"
    )

    with open("daily_report.txt", "w", encoding="utf-8") as f:
        f.write(text)

    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
  
