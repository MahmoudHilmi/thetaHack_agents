"""Simple CLI for sending decision requests to the ORACLE API."""

import json
import sys

try:
    import httpx
except ImportError:
    import urllib.request as request
    import urllib.error as error


API_URL = "http://127.0.0.1:8000/decide"
REQUEST_TIMEOUT = 300.0


def post_decision(problem: str, user_input: str) -> dict:
    payload = {
        "problem_description": problem,
        "user_input": user_input,
    }

    headers = {"Content-Type": "application/json"}

    try:
        if "httpx" in sys.modules:
            response = httpx.post(API_URL, json=payload, headers=headers, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            return response.json()
        else:
            data = json.dumps(payload).encode("utf-8")
            req = request.Request(API_URL, data=data, headers=headers, method="POST")
            with request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                return json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        return {"error": str(exc)}


def main() -> None:
    print("ORACLE CLI")
    print("Enter a problem description to ask the model. Press Ctrl+C to quit.")

    try:
        while True:
            problem = input("\nProblem: ").strip()
            if not problem:
                print("Please enter a non-empty problem description.")
                continue

            user_input = input("Additional context (optional): ").strip()
            result = post_decision(problem, user_input)

            print("\nResult:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
    except KeyboardInterrupt:
        print("\nGoodbye.")


if __name__ == "__main__":
    main()
