#!/usr/bin/env python3
"""
Read Messages history from ~/Library/Messages/chat.db (requires Full Disk Access).
Ported from apple-mcp utils/message.ts query shape; output is JSON lines / JSON array.

This is not AppleScript; it complements messages/send_message.applescript.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import sys
from datetime import datetime, timezone


def _apple_time_to_iso(apple_ns: int | None) -> str | None:
    if apple_ns is None:
        return None
    # Core Data / Messages: nanoseconds since 2001-01-01
    try:
        base = datetime(2001, 1, 1, tzinfo=timezone.utc).timestamp()
        ts = base + float(apple_ns) / 1e9
        return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()
    except Exception:
        return None


def normalize_phone_variants(phone: str) -> list[str]:
    cleaned = re.sub(r"[^0-9+]", "", phone)
    out: list[str] = []
    if re.fullmatch(r"\+1\d{10}", cleaned):
        out.append(cleaned)
    elif re.fullmatch(r"1\d{10}", cleaned):
        out.append(f"+{cleaned}")
    elif re.fullmatch(r"\d{10}", cleaned):
        out.append(f"+1{cleaned}")
    else:
        s = set()
        if cleaned.startswith("+1"):
            s.add(cleaned)
        elif cleaned.startswith("1"):
            s.add(f"+{cleaned}")
        else:
            s.add(f"+1{cleaned}")
        out.extend(sorted(s))
    return list(dict.fromkeys(out))


def fetch_by_phone(db_path: str, phone: str, limit: int) -> list[dict]:
    phones = normalize_phone_variants(phone)
    placeholders = ",".join("?" * len(phones))
    sql = f"""
            SELECT
                m.ROWID as message_id,
                CASE
                    WHEN m.text IS NOT NULL AND m.text != '' THEN m.text
                    WHEN m.attributedBody IS NOT NULL THEN '[attributedBody]'
                    ELSE NULL
                END as content,
                m.date as date_raw,
                h.id as sender,
                m.is_from_me,
                m.cache_has_attachments
            FROM message m
            INNER JOIN handle h ON h.ROWID = m.handle_id
            WHERE h.id IN ({placeholders})
                AND (m.text IS NOT NULL OR m.attributedBody IS NOT NULL OR m.cache_has_attachments = 1)
                AND m.is_from_me IS NOT NULL
                AND m.item_type = 0
                AND m.is_audio_message = 0
            ORDER BY m.date DESC
            LIMIT ?
            """
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        cur = con.execute(sql, (*phones, limit))
        rows = cur.fetchall()
    finally:
        con.close()

    out: list[dict] = []
    for row in rows:
        mid, content, date_raw, sender, is_from_me, cache_att = row
        out.append(
            {
                "message_id": mid,
                "content": content,
                "date": _apple_time_to_iso(date_raw),
                "sender": sender,
                "is_from_me": bool(is_from_me),
                "cache_has_attachments": bool(cache_att),
            }
        )
    return out


def fetch_unread(db_path: str, limit: int) -> list[dict]:
    sql = """
            SELECT
                m.ROWID as message_id,
                CASE
                    WHEN m.text IS NOT NULL AND m.text != '' THEN m.text
                    WHEN m.attributedBody IS NOT NULL THEN '[attributedBody]'
                    ELSE NULL
                END as content,
                m.date as date_raw,
                h.id as sender,
                m.is_from_me,
                m.cache_has_attachments
            FROM message m
            INNER JOIN handle h ON h.ROWID = m.handle_id
            WHERE m.is_from_me = 0
                AND m.is_read = 0
                AND (m.text IS NOT NULL OR m.attributedBody IS NOT NULL OR m.cache_has_attachments = 1)
                AND m.is_audio_message = 0
                AND m.item_type = 0
            ORDER BY m.date DESC
            LIMIT ?
            """
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        cur = con.execute(sql, (limit,))
        rows = cur.fetchall()
    finally:
        con.close()

    out: list[dict] = []
    for row in rows:
        mid, content, date_raw, sender, is_from_me, cache_att = row
        out.append(
            {
                "message_id": mid,
                "content": content,
                "date": _apple_time_to_iso(date_raw),
                "sender": sender,
                "is_from_me": bool(is_from_me),
                "cache_has_attachments": bool(cache_att),
            }
        )
    return out


def main() -> int:
    p = argparse.ArgumentParser(description="Read Messages from chat.db (read-only).")
    p.add_argument(
        "--db",
        default=os.path.expanduser("~/Library/Messages/chat.db"),
        help="Path to chat.db",
    )
    p.add_argument("--limit", type=int, default=10)
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("unread", help="Unread messages from others")

    sp = sub.add_parser("by-phone", help="Messages for a handle id (phone)")
    sp.add_argument("phone", help="Phone or handle id as in DB")

    args = p.parse_args()
    db = os.path.expanduser(args.db)
    if not os.path.isfile(db):
        print(json.dumps({"error": f"database not found: {db}"}), file=sys.stderr)
        return 2

    try:
        if args.cmd == "unread":
            data = fetch_unread(db, args.limit)
        else:
            data = fetch_by_phone(db, args.phone, args.limit)
    except sqlite3.Error as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        return 1

    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())