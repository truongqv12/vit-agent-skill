import sys
import argparse
import time
from jira_api import JiraClient

def main():
    parser = argparse.ArgumentParser(description="Link Jira issues")
    parser.add_argument("source", help="Source issue key (e.g. CCDT-430)")
    parser.add_argument("targets", nargs="+", help="Target issue keys to link (e.g. CCDT-391 CCDT-392)")
    parser.add_argument("--type", default="Relates", help="Link type (default: Relates)")
    parser.add_argument("--delay", type=float, default=1.5, help="Delay between calls in seconds")
    args = parser.parse_args()

    client = JiraClient()
    source_key = args.source.strip().upper()
    total = len(args.targets)

    print("=" * 80)
    print(f" LINKING {source_key} WITH {total} ISSUE(S) (Type: {args.type})")
    print("=" * 80)

    for idx, raw_target in enumerate(args.targets, 1):
        target_key = raw_target.strip().upper()
        try:
            print(f"[{idx}/{total}] Linking {source_key} -> {target_key}...")
            client.link_issues(source_key, target_key, link_type=args.type)
            print(f"  [+] Success: {source_key} <-> {target_key}")
        except Exception as e:
            print(f"  [-] Failed to link {source_key} with {target_key}: {e}", file=sys.stderr)

        if idx < total and args.delay > 0:
            time.sleep(args.delay)

if __name__ == "__main__":
    main()
