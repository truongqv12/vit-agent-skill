import sys
import argparse
import time
from jira_api import JiraClient

def main():
    parser = argparse.ArgumentParser(description="Add comment to one or more Jira issues")
    parser.add_argument("keys", nargs="+", help="Issue keys (e.g. CCDT-391 CCDT-392)")
    parser.add_argument("--message", "-m", required=True, help="Comment body text")
    parser.add_argument("--delay", type=float, default=2.0, help="Delay between comments in seconds (default: 2.0)")
    args = parser.parse_args()

    client = JiraClient()
    total = len(args.keys)

    print("=" * 80)
    print(f" ADDING COMMENT TO {total} ISSUE(S)")
    print(f" Comment: {args.message}")
    print("=" * 80)

    success_keys = []
    failed_keys = []

    for idx, raw_key in enumerate(args.keys, 1):
        key = raw_key.strip().upper()
        try:
            print(f"[{idx}/{total}] Commenting on {key}...")
            client.add_comment(key, args.message)
            print(f"  [+] Success: {key}")
            success_keys.append(key)
        except Exception as e:
            print(f"  [-] Failed on {key}: {e}", file=sys.stderr)
            failed_keys.append((key, str(e)))

        if idx < total and args.delay > 0:
            time.sleep(args.delay)

    print("=" * 80)
    print(f" RESULT: {len(success_keys)}/{total} succeeded.")
    if failed_keys:
        print(f" Failed: {failed_keys}")
    print("=" * 80)

if __name__ == "__main__":
    main()
