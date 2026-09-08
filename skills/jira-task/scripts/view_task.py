import os
import sys
import json
import argparse
from jira_api import JiraClient

def download_file(url, output_path, client):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    res = client.session.get(url, stream=True, timeout=30)
    if res.ok:
        with open(output_path, "wb") as f:
            for chunk in res.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    return False

def render_issue(issue, client, download_attachments=False):
    key = issue.get("key", "")
    fields = issue.get("fields", {})

    summary = fields.get("summary", "Không có tiêu đề")
    status = fields.get("status", {}).get("name", "N/A") if fields.get("status") else "N/A"
    priority = fields.get("priority", {}).get("name", "N/A") if fields.get("priority") else "N/A"
    issuetype = fields.get("issuetype", {}).get("name", "Task") if fields.get("issuetype") else "Task"

    assignee = fields.get("assignee")
    assignee_name = assignee.get("displayName", assignee.get("name", "Unassigned")) if assignee else "Chưa gán"

    reporter = fields.get("reporter")
    reporter_name = reporter.get("displayName", reporter.get("name", "N/A")) if reporter else "N/A"

    duedate = fields.get("duedate", "N/A") or "N/A"
    created = fields.get("created", "")[:10]
    updated = fields.get("updated", "")[:10]

    description = fields.get("description", "Không có mô tả.") or "Không có mô tả."
    attachments = fields.get("attachment", [])
    comments = fields.get("comment", {}).get("comments", [])

    print("\n" + "=" * 90)
    print(f" 📌 [{key}] {summary}")
    print("=" * 90)
    print(f" • Loại (Type)    : {issuetype:<20} | Ưu tiên (Priority) : {priority}")
    print(f" • Trạng thái     : {status:<20} | Hạn xử lý (DueDate): {duedate}")
    print(f" • Người xử lý    : {assignee_name:<20} | Người tạo (Reporter): {reporter_name}")
    print(f" • Ngày tạo / Sửa : {created} -> {updated} | Link Jira: {client.base_url}/browse/{key}")

    print("\n" + "-" * 90)
    print(" 📝 MÔ TẢ (DESCRIPTION):")
    print("-" * 90)
    print(description.strip())

    print("\n" + "-" * 90)
    print(f" 📎 ẢNH & FILE ĐÍNH KÈM ({len(attachments)} files):")
    print("-" * 90)
    if not attachments:
        print(" (Không có file đính kèm)")
    else:
        for idx, att in enumerate(attachments, start=1):
            att_id = att.get("id")
            filename = att.get("filename")
            size_kb = round(att.get("size", 0) / 1024, 1)
            content_url = att.get("content")
            mime_type = att.get("mimeType", "")

            print(f" [{idx}] {filename} ({mime_type} - {size_kb} KB)")
            print(f"     URL trực tiếp: {content_url}")

            if download_attachments:
                local_dir = os.path.join("attachments", key)
                local_file = os.path.join(local_dir, f"{att_id}_{filename}")
                print(f"     -> Đang tải về: {local_file} ... ", end="")
                ok = download_file(content_url, local_file, client)
                if ok:
                    print(f"OK (Đã lưu tại: {os.path.abspath(local_file)})")
                else:
                    print("THẤT BẠI")

    print("\n" + "-" * 90)
    print(f" 💬 BÌNH LUẬN (COMMENTS - {len(comments)} comments):")
    print("-" * 90)
    if not comments:
        print(" (Chưa có bình luận nào)")
    else:
        for idx, c in enumerate(comments, start=1):
            c_author = c.get("author", {}).get("displayName", "N/A")
            c_created = c.get("created", "")[:19].replace("T", " ")
            c_body = c.get("body", "").strip()
            print(f" [{idx}] {c_author} ({c_created}):")
            print(f"     {c_body}\n")

def main():
    parser = argparse.ArgumentParser(description="View Jira task detail (Description, Comments, Attachments)")
    parser.add_argument("keys", nargs="+", help="One or more task keys (e.g. CCDT-99 CCDT-97)")
    parser.add_argument("-d", "--download", action="store_true", help="Download all attachments locally")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    client = JiraClient()
    fields = "summary,description,comment,attachment,status,assignee,reporter,created,updated,priority,issuetype,parent,subtasks"

    for key in args.keys:
        clean_key = key.strip().replace(",", "").upper()
        if not clean_key:
            continue
        try:
            issue = client.get_issue(clean_key, fields=fields)
            if args.json:
                print(json.dumps(issue, ensure_ascii=False, indent=2))
            else:
                render_issue(issue, client, download_attachments=args.download)
        except Exception as e:
            print(f"[ERROR] Could not fetch {clean_key}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
