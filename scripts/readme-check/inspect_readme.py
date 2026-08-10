#!/usr/bin/env python3
"""Fail-closed README structure and integrity checks.

Python 3.9+ and the standard library are the only runtime requirements.
"""

from __future__ import annotations

import argparse
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import struct
import sys
import unicodedata
from urllib.parse import unquote, urlsplit


PLACEHOLDER_RE = re.compile(r"\b(?:TODO|TBD|FIXME|PLACEHOLDER|XXX)\b", re.IGNORECASE)
ATX_RE = re.compile(r"^[ ]{0,3}(#{1,6})(?:[ \t]+(.*?)|[ \t]*)$")
SETEXT_RE = re.compile(r"^[ ]{0,3}(=+|-+)[ \t]*$")
FENCE_RE = re.compile(r"^[ ]{0,3}(`{3,}|~{3,})(.*)$")
FENCE_CLOSE_RE = re.compile(r"^[ ]{0,3}(`{3,}|~{3,})[ \t]*$")
REFERENCE_DEF_RE = re.compile(
    r"^[ ]{0,3}\[([^\]]+)\]:[ \t]*(?:<([^>\n]+)>|([^\s]+))",
    re.MULTILINE,
)
README_SIBLING_RE = re.compile(r"^README(?:\.[A-Za-z0-9_-]+)*\.md$", re.IGNORECASE)
BAD_PERCENT_RE = re.compile(r"%(?![0-9A-Fa-f]{2})")
URL_SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
CONTRACT_KEYS = ("command", "target", "target_sha256", "pass", "fails", "warns")


def finding(check: str, path: object, detail: str) -> dict:
    return {"check": check, "path": str(path), "detail": detail}


def report(command: str, target: object, sha256: str = "") -> dict:
    return {
        "command": command,
        "target": str(target),
        "target_sha256": sha256,
        "pass": True,
        "fails": [],
        "warns": [],
    }


def add_fail(result: dict, check: str, path: object, detail: str) -> None:
    result["fails"].append(finding(check, path, detail))
    result["pass"] = False


def add_warn(result: dict, check: str, path: object, detail: str) -> None:
    result["warns"].append(finding(check, path, detail))


def read_utf8(path_arg: str, result: dict) -> tuple[Path | None, str | None, bytes | None]:
    path = Path(path_arg)
    try:
        if not path.exists():
            add_fail(result, "read-target", path_arg, "target does not exist")
            return None, None, None
        if not path.is_file():
            add_fail(result, "read-target", path_arg, "target is not a regular file")
            return None, None, None
        raw = path.read_bytes()
        result["target_sha256"] = hashlib.sha256(raw).hexdigest()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            add_fail(result, "invalid-utf8", path_arg, "target is not valid UTF-8: %s" % exc)
            return path, None, raw
        return path, text, raw
    except OSError as exc:
        add_fail(result, "read-target", path_arg, "could not read target: %s" % exc)
        return None, None, None


class LinkHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, bool]] = []
        self.anchors: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value for key, value in attrs}
        lowered = tag.lower()
        if lowered == "a":
            if values.get("id"):
                self.anchors.append(str(values["id"]))
            if values.get("href"):
                self.links.append((str(values["href"]), False))
        elif lowered == "img" and values.get("src"):
            self.links.append((str(values["src"]), True))


def strip_html_comments_from_line(line: str, in_comment: bool) -> tuple[str, bool]:
    output: list[str] = []
    cursor = 0
    length = len(line)
    while cursor < length:
        if in_comment:
            end = line.find("-->", cursor)
            if end < 0:
                return "".join(output), True
            cursor = end + 3
            in_comment = False
            continue
        start = line.find("<!--", cursor)
        if start < 0:
            output.append(line[cursor:])
            break
        output.append(line[cursor:start])
        cursor = start + 4
        in_comment = True
    return "".join(output), in_comment


def analyze_markdown_lines(lines: list[str]) -> tuple[list[bool], list[str], int, int | None, int | None]:
    """Return code-line mask, structural lines, code block count, open fence line, and open comment line."""
    mask = [False] * len(lines)
    structural_lines = [""] * len(lines)
    fence_char: str | None = None
    fence_length = 0
    fence_start: int | None = None
    comment_start: int | None = None
    blocks = 0
    in_indented = False
    can_start_indented = True
    in_comment = False

    for index, line in enumerate(lines):
        if fence_char is not None:
            mask[index] = True
            structural_lines[index] = line
            close = FENCE_CLOSE_RE.match(line)
            if close and close.group(1)[0] == fence_char and len(close.group(1)) >= fence_length:
                fence_char = None
                fence_length = 0
                fence_start = None
                can_start_indented = True
            continue

        indented = line.startswith("    ") or line.startswith("\t")
        if not in_comment and indented and (in_indented or can_start_indented):
            mask[index] = True
            structural_lines[index] = line
            if not in_indented:
                blocks += 1
            in_indented = True
            can_start_indented = False
            continue

        original_in_comment = in_comment
        structural_line, in_comment = strip_html_comments_from_line(line, in_comment)
        structural_lines[index] = structural_line
        if not original_in_comment and in_comment and comment_start is None:
            comment_start = index + 1
        elif original_in_comment and not in_comment:
            comment_start = None

        opening = FENCE_RE.match(structural_line)
        if opening:
            fence = opening.group(1)
            # Backtick info strings may not contain a backtick.
            if fence[0] == "`" and "`" in opening.group(2):
                pass
            else:
                fence_char = fence[0]
                fence_length = len(fence)
                fence_start = index + 1
                blocks += 1
                mask[index] = True
                in_indented = False
                can_start_indented = False
                continue

        if structural_line.strip() == "":
            if in_indented:
                mask[index] = True
            else:
                can_start_indented = True
            continue
        in_indented = False
        # Indented code cannot interrupt a paragraph. Four-space lines
        # immediately following paragraph or list text are continuations,
        # so keep them visible to checks such as placeholder detection.
        can_start_indented = bool(
            ATX_RE.match(structural_line)
            or SETEXT_RE.match(structural_line)
            or re.match(r"^[ ]{0,3}(?:-{3,}|\*{3,}|_{3,})[ \t]*$", structural_line)
        )

    return mask, structural_lines, blocks, fence_start, comment_start


def clean_heading(value: str) -> str:
    value = re.sub(r"[ \t]+#+[ \t]*$", "", value).strip()
    return html.unescape(value)


def headings_from(lines: list[str], code_mask: list[bool]) -> list[dict]:
    headings: list[dict] = []
    for index, line in enumerate(lines):
        if code_mask[index]:
            continue
        match = ATX_RE.match(line)
        if match:
            headings.append(
                {
                    "level": len(match.group(1)),
                    "text": clean_heading(match.group(2) or ""),
                    "line": index + 1,
                    "end_line": index + 1,
                }
            )
            continue
        if index > 0 and not code_mask[index - 1]:
            underline = SETEXT_RE.match(line)
            previous = lines[index - 1].strip()
            if underline and previous and not ATX_RE.match(lines[index - 1]):
                headings.append(
                    {
                        "level": 1 if underline.group(1)[0] == "=" else 2,
                        "text": previous,
                        "line": index,
                        "end_line": index + 1,
                    }
                )
    headings.sort(key=lambda item: item["line"])
    return headings


def gfm_slug(text: str) -> str:
    text = re.sub(r"<[^>]*>", "", text)
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = html.unescape(text).strip().lower()
    output: list[str] = []
    for character in text:
        category = unicodedata.category(character)
        if character.isspace():
            output.append("-")
        elif category.startswith("P") and character not in "-_":
            continue
        elif category.startswith("C"):
            continue
        else:
            output.append(character)
    return "".join(output)


def anchors_from(text: str, headings: list[dict]) -> set[str]:
    parser = LinkHTMLParser()
    try:
        parser.feed(text)
    except Exception:
        # HTMLParser is forgiving; a malformed tag must not hide heading anchors.
        pass
    anchors = set(parser.anchors)
    counts: dict[str, int] = {}
    for heading in headings:
        base = gfm_slug(heading["text"])
        suffix = counts.get(base, 0)
        anchors.add(base if suffix == 0 else "%s-%d" % (base, suffix))
        counts[base] = suffix + 1
    return anchors


def destination_from_payload(payload: str) -> str:
    payload = payload.strip()
    if not payload:
        return ""
    if payload.startswith("<"):
        end = payload.find(">")
        if end < 0:
            return payload
        destination = payload[1:end]
        remainder = payload[end + 1 :].strip()
        if remainder and not valid_link_title(remainder):
            return payload
        return destination
    escaped = False
    depth = 0
    chars: list[str] = []
    destination_end = len(payload)
    for position, character in enumerate(payload):
        if escaped:
            chars.append(character)
            escaped = False
        elif character == "\\":
            escaped = True
        elif character.isspace() and depth == 0:
            destination_end = position
            break
        else:
            if character == "(":
                depth += 1
            elif character == ")" and depth:
                depth -= 1
            chars.append(character)
    destination = "".join(chars)
    remainder = payload[destination_end:].strip()
    if remainder and not valid_link_title(remainder):
        return payload
    return destination


def valid_link_title(value: str) -> bool:
    if len(value) < 2:
        return False
    pairs = {'"': '"', "'": "'", "(": ")"}
    return value[0] in pairs and value[-1] == pairs[value[0]]


def inline_links(text: str) -> list[tuple[str, bool]]:
    found: list[tuple[str, bool]] = []
    length = len(text)
    index = 0
    while index < length:
        image = text.startswith("![", index)
        if image:
            label_start = index + 2
        elif text[index] == "[":
            label_start = index + 1
        else:
            index += 1
            continue

        cursor = label_start
        escaped = False
        while cursor < length:
            char = text[cursor]
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == "]":
                break
            cursor += 1
        if cursor >= length:
            index += 1
            continue
        after = cursor + 1
        while after < length and text[after] in " \t\n":
            after += 1
        if after >= length or text[after] != "(":
            index = cursor + 1
            continue

        payload_start = after + 1
        pointer = payload_start
        depth = 1
        escaped = False
        angle = False
        quote: str | None = None
        while pointer < length:
            char = text[pointer]
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif quote:
                if char == quote:
                    quote = None
            elif char in "\"'" and pointer > payload_start and text[pointer - 1].isspace():
                quote = char
            elif char == "<":
                angle = True
            elif char == ">" and angle:
                angle = False
            elif not angle and char == "(":
                depth += 1
            elif not angle and char == ")":
                depth -= 1
                if depth == 0:
                    destination = destination_from_payload(text[payload_start:pointer])
                    if destination:
                        found.append((destination, image))
                    pointer += 1
                    break
            pointer += 1
        index = max(pointer, cursor + 1)
    return found


def links_from(text: str) -> list[tuple[str, bool]]:
    links = inline_links(text)
    definitions: dict[str, str] = {}
    for match in REFERENCE_DEF_RE.finditer(text):
        label = re.sub(r"\s+", " ", match.group(1).strip()).casefold()
        definitions[label] = match.group(2) or match.group(3)

    use_re = re.compile(r"(!?)\[([^\]]+)\](?:\[([^\]]*)\])")
    for match in use_re.finditer(text):
        label = (match.group(3) or match.group(2)).strip()
        normalized = re.sub(r"\s+", " ", label).casefold()
        if normalized in definitions:
            links.append((definitions[normalized], bool(match.group(1))))

    # CommonMark shortcut references: [label] and ![label]. Definitions and
    # inline/full references are excluded by their following delimiter. A full
    # reference's second bracket may also match, so de-duplicate below.
    shortcut_re = re.compile(r"(?<!\])(!?)\[([^\]\n]+)\](?![ \t]*(?:\(|\[|:))")
    for match in shortcut_re.finditer(text):
        normalized = re.sub(r"\s+", " ", match.group(2).strip()).casefold()
        if normalized in definitions:
            links.append((definitions[normalized], bool(match.group(1))))

    parser = LinkHTMLParser()
    try:
        parser.feed(text)
        links.extend(parser.links)
    except Exception:
        pass
    unique: list[tuple[str, bool]] = []
    seen: set[tuple[str, bool]] = set()
    for item in links:
        if item not in seen:
            seen.add(item)
            unique.append(item)
    return unique


def visible_text(lines: list[str], code_mask: list[bool]) -> str:
    return "\n".join("" if code_mask[index] else line for index, line in enumerate(lines))


def parse_markdown(path: Path, text: str, result: dict) -> dict:
    raw_lines = text.splitlines()
    mask, structural_lines, code_blocks, fence_start, comment_start = analyze_markdown_lines(raw_lines)
    if fence_start is not None:
        add_fail(
            result,
            "unterminated-fence",
            path,
            "fenced code block opened on line %d is not closed" % fence_start,
        )
    if comment_start is not None:
        add_fail(
            result,
            "unterminated-html-comment",
            path,
            "HTML comment opened on line %d is not closed" % comment_start,
        )
    headings = headings_from(structural_lines, mask)
    visible = visible_text(raw_lines, mask)
    structural_visible = visible_text(structural_lines, mask)
    return {
        "lines": structural_lines,
        "raw_lines": raw_lines,
        "code_mask": mask,
        "code_blocks": code_blocks,
        "headings": headings,
        "visible": visible,
        "structural_visible": structural_visible,
        "anchors": anchors_from(structural_visible, headings),
        "links": links_from(structural_visible),
    }


def local_destination(destination: str) -> tuple[str, str] | None:
    decoded = html.unescape(destination.strip())
    if decoded.startswith("//"):
        return None
    parsed = urlsplit(decoded)
    if parsed.scheme or parsed.netloc:
        return None
    path = unquote(parsed.path)
    fragment = unquote(parsed.fragment)
    if path.startswith("/"):
        return None
    return path, fragment


def is_root_relative_destination(destination: str) -> bool:
    decoded = html.unescape(destination.strip())
    if decoded.startswith("//"):
        return False
    parsed = urlsplit(decoded)
    return not parsed.scheme and not parsed.netloc and unquote(parsed.path).startswith("/")


def destination_format_error(destination: str) -> str | None:
    value = html.unescape(destination.strip())
    looks_external = value.startswith("//") or URL_SCHEME_RE.match(value) is not None
    if not looks_external:
        return None
    if any(character.isspace() for character in value):
        return "external link destination contains whitespace"
    if BAD_PERCENT_RE.search(value):
        return "external link destination contains an invalid percent escape"
    try:
        parsed = urlsplit(value)
        # Accessing hostname/port performs additional bracket and port checks.
        hostname = parsed.hostname
        _ = parsed.port
    except ValueError as exc:
        return "link destination is malformed: %s" % exc
    if value.startswith("//"):
        if not parsed.netloc or not hostname:
            return "protocol-relative URL has no host"
    elif parsed.scheme.lower() in {"http", "https"}:
        if not parsed.netloc or not hostname:
            return "%s URL has no host" % parsed.scheme.lower()
    elif parsed.scheme.lower() == "mailto" and not parsed.path:
        return "mailto URL has no recipient"
    return None


def image_metadata(path: Path) -> tuple[bool, str, bool]:
    try:
        data = path.read_bytes()
    except OSError as exc:
        return False, "could not read image while checking metadata: %s" % exc, True

    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        offset = 8
        metadata_detail = ""
        saw_iend = False
        while offset < len(data):
            if offset + 12 > len(data):
                return False, "PNG contains a truncated chunk header", True
            size = struct.unpack(">I", data[offset : offset + 4])[0]
            chunk_type = data[offset + 4 : offset + 8]
            end = offset + 12 + size
            if end > len(data):
                return (
                    False,
                    "PNG chunk %r declares %d data bytes beyond the file boundary"
                    % (chunk_type, size),
                    True,
                )
            if chunk_type in {b"tEXt", b"iTXt", b"zTXt"} and not metadata_detail:
                metadata_detail = "PNG contains %s metadata chunk" % chunk_type.decode("ascii")
            if chunk_type == b"IEND":
                if size != 0:
                    return False, "PNG IEND chunk must have zero data bytes", True
                saw_iend = True
                break
            offset = end
        if not saw_iend:
            return False, "PNG is missing a complete IEND chunk", True
        return bool(metadata_detail), metadata_detail, False

    if data.startswith(b"\xff\xd8"):
        offset = 2
        while offset + 4 <= len(data):
            if data[offset] != 0xFF:
                offset += 1
                continue
            while offset < len(data) and data[offset] == 0xFF:
                offset += 1
            if offset >= len(data):
                break
            marker = data[offset]
            offset += 1
            if marker in {0xD8, 0xD9} or 0xD0 <= marker <= 0xD7:
                continue
            if offset + 2 > len(data):
                break
            size = struct.unpack(">H", data[offset : offset + 2])[0]
            if size < 2 or offset + size > len(data):
                break
            payload = data[offset + 2 : offset + size]
            if marker == 0xE1:
                label = "APP1 Exif" if payload.startswith(b"Exif\x00\x00") else "APP1"
                return True, "JPEG contains %s metadata" % label, False
            if marker == 0xDA:
                break
            offset += size
    return False, "", False


def inspect_links(path: Path, parsed: dict, result: dict, public: bool) -> None:
    metadata_checked: set[Path] = set()
    for destination, is_image in parsed["links"]:
        format_error = destination_format_error(destination)
        if format_error:
            add_fail(result, "link-format", path, "%s: %s" % (format_error, destination))
            continue
        if not is_image and is_root_relative_destination(destination):
            add_warn(result, "root-relative-link", path, "root-relative link target cannot be resolved locally: %s" % destination)
            continue
        local = local_destination(destination)
        if local is None:
            continue
        relative, fragment = local
        target = path if relative == "" else path.parent / relative
        label = destination
        if relative and (not target.exists() or not target.is_file()):
            add_fail(
                result,
                "local-image" if is_image else "relative-link",
                path,
                "local %s target does not exist: %s" % ("image" if is_image else "link", label),
            )
            continue

        if fragment:
            if relative == "":
                if fragment not in parsed["anchors"]:
                    add_fail(result, "page-anchor", path, "unresolved page anchor: #%s" % fragment)
            elif target.suffix.lower() in {".md", ".markdown"}:
                nested = report("inspect", target)
                nested_path, nested_text, _ = read_utf8(str(target), nested)
                if nested_path is None or nested_text is None:
                    add_fail(result, "cross-file-anchor", path, "could not parse anchor target: %s" % label)
                else:
                    nested_parsed = parse_markdown(nested_path, nested_text, nested)
                    if nested["fails"] or fragment not in nested_parsed["anchors"]:
                        add_fail(result, "cross-file-anchor", path, "unresolved cross-file anchor: %s" % label)

        if is_image and relative and target.is_file() and target not in metadata_checked:
            metadata_checked.add(target)
            has_metadata, detail, read_error = image_metadata(target)
            if read_error:
                add_fail(result, "image-read", target, detail)
                continue
            if has_metadata:
                if public:
                    add_fail(result, "image-metadata", target, detail)
                else:
                    add_warn(result, "image-metadata", target, detail)


def section_signature(lines: list[str], code_mask: list[bool], start: int, end: int) -> tuple[str, ...]:
    blocks: list[str] = []
    current: str | None = None
    for index in range(start, end):
        line = lines[index]
        stripped = line.strip()
        if not stripped:
            current = None
            continue
        if code_mask[index]:
            kind = "code"
        elif re.match(r"^[ ]{0,3}(?:[-+*]|\d+[.)])[ \t]+", line):
            kind = "list"
        elif re.match(r"^[ ]{0,3}>", line):
            kind = "quote"
        elif re.match(r"^[ ]{0,3}\|.*\|[ \t]*$", line):
            kind = "table"
        elif re.search(r"!\[[^\]]*\]\(", line) or re.search(r"<img\b", line, re.IGNORECASE):
            kind = "image"
        elif ATX_RE.match(line) or SETEXT_RE.match(line):
            kind = "heading"
        else:
            kind = "paragraph"
        if kind != current:
            blocks.append(kind)
            current = kind
    return tuple(blocks)


def inspect_structure(path: Path, parsed: dict, result: dict) -> None:
    previous: dict | None = {"level": 1, "line": 0}
    for heading in parsed["headings"]:
        if heading["level"] > previous["level"] + 1:
            add_fail(
                result,
                "heading-level-jump",
                path,
                "heading level jumps from H%d on line %d to H%d on line %d"
                % (previous["level"], previous["line"], heading["level"], heading["line"]),
            )
        previous = heading

    h2 = [heading for heading in parsed["headings"] if heading["level"] == 2]
    signatures: list[tuple[str, ...]] = []
    for index, heading in enumerate(h2):
        start = heading["end_line"]
        end = h2[index + 1]["line"] - 1 if index + 1 < len(h2) else len(parsed["lines"])
        signatures.append(section_signature(parsed["lines"], parsed["code_mask"], start, end))
    for index in range(2, len(signatures)):
        if signatures[index] == signatures[index - 1] == signatures[index - 2]:
            names = [h2[position]["text"] for position in range(index - 2, index + 1)]
            add_warn(result, "repeated-section-shape", path, "three consecutive sections share one block shape: %s" % ", ".join(names))


def load_json(path: Path, result: dict, check: str) -> object | None:
    try:
        if not path.exists() or not path.is_file():
            add_fail(result, check, path, "required JSON file is missing or not a regular file")
            return None
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        return json.loads(text)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        add_fail(result, check, path, "invalid JSON file: %s" % exc)
        return None


def nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_string_list(value: object, allow_empty: bool) -> bool:
    return (
        isinstance(value, list)
        and (allow_empty or len(value) > 0)
        and all(nonempty_string(item) for item in value)
    )


BRIEF_STRING_KEYS = {
    "purpose",
    "reader_now",
    "reader_after",
    "final_action",
    "decision_criteria",
    "decider",
    "publish_class",
    "summary_30s",
}
BRIEF_LIST_KEYS = {"anxieties", "evidence", "constraints"}


def validate_brief(value: object, path: Path, result: dict) -> str | None:
    if not isinstance(value, dict):
        add_fail(result, "brief-schema", path, "brief.json must contain one object")
        return None
    required = BRIEF_STRING_KEYS | BRIEF_LIST_KEYS
    missing = sorted(required - set(value))
    if missing:
        add_fail(result, "brief-schema", path, "missing required keys: %s" % ", ".join(missing))
    for key in sorted(BRIEF_STRING_KEYS):
        if key in value and not nonempty_string(value[key]):
            add_fail(result, "brief-schema", path, "%s must be a non-empty string" % key)
    for key in ("anxieties", "evidence"):
        if key in value and not validate_string_list(value[key], allow_empty=False):
            add_fail(result, "brief-schema", path, "%s must contain at least one non-empty string" % key)
    if "constraints" in value and not validate_string_list(value["constraints"], allow_empty=True):
        add_fail(result, "brief-schema", path, "constraints must be an array of non-empty strings")
    publish = value.get("publish_class")
    if publish not in {"public", "internal", "private"}:
        add_fail(result, "brief-schema", path, "publish_class must be public, internal, or private")
        return None
    return str(publish)


BRIDGE_SECTION_KEYS = {
    "heading",
    "prev_conclusion",
    "question",
    "answer",
    "next_question",
    "bridge_text",
}
BRIDGE_EXEMPT_KEYS = {"heading", "reason"}


def validate_bridges(value: object, path: Path, h2_headings: list[str], result: dict) -> None:
    if not isinstance(value, dict):
        add_fail(result, "bridges-schema", path, "bridges.json must contain one object")
        return
    sections = value.get("sections")
    exempt = value.get("exempt")
    if not isinstance(sections, list) or not isinstance(exempt, list):
        add_fail(result, "bridges-schema", path, "sections and exempt must be arrays")
        return
    if not sections:
        add_fail(result, "bridges-schema", path, "sections must contain at least one entry")

    section_names: list[str] = []
    exempt_names: list[str] = []
    for index, entry in enumerate(sections):
        if not isinstance(entry, dict) or not BRIDGE_SECTION_KEYS.issubset(entry):
            add_fail(result, "bridges-schema", path, "sections[%d] is missing required fields" % index)
            continue
        for key in sorted(BRIDGE_SECTION_KEYS):
            if not nonempty_string(entry.get(key)):
                add_fail(result, "bridges-schema", path, "sections[%d].%s must be a non-empty string" % (index, key))
        if nonempty_string(entry.get("heading")):
            section_names.append(entry["heading"])
    for index, entry in enumerate(exempt):
        if not isinstance(entry, dict) or not BRIDGE_EXEMPT_KEYS.issubset(entry):
            add_fail(result, "bridges-schema", path, "exempt[%d] is missing heading or reason" % index)
            continue
        for key in sorted(BRIDGE_EXEMPT_KEYS):
            if not nonempty_string(entry.get(key)):
                add_fail(result, "bridges-schema", path, "exempt[%d].%s must be a non-empty string" % (index, key))
        if nonempty_string(entry.get("heading")):
            exempt_names.append(entry["heading"])

    if not h2_headings:
        if len(sections) != 1 or section_names != ["-"]:
            add_fail(
                result,
                "bridges-coverage",
                path,
                "README files without H2 headings must declare exactly one sections entry with heading '-'",
            )
        if exempt:
            add_fail(result, "bridges-coverage", path, "README files without H2 headings may not declare exempt headings")
        return

    declared = section_names + exempt_names
    repeated_readme = sorted({name for name in h2_headings if h2_headings.count(name) > 1})
    if repeated_readme:
        add_fail(
            result,
            "bridges-coverage",
            path,
            "duplicate README H2 headings cannot be mapped uniquely: %s" % ", ".join(repeated_readme),
        )
    duplicates = sorted({name for name in declared if declared.count(name) > 1})
    if duplicates:
        add_fail(result, "bridges-coverage", path, "headings declared more than once: %s" % ", ".join(duplicates))
    missing = [name for name in h2_headings if name not in declared]
    extra = [name for name in declared if name not in h2_headings]
    if missing:
        add_fail(result, "bridges-coverage", path, "README H2 headings are not covered: %s" % ", ".join(missing))
    if extra:
        add_fail(result, "bridges-coverage", path, "unknown headings are declared: %s" % ", ".join(extra))
    if h2_headings and len(exempt_names) == len(h2_headings):
        add_fail(result, "bridges-coverage", path, "all README sections may not be exempt")
    if h2_headings and len(exempt_names) > len(h2_headings) / 2:
        add_warn(result, "exempt-majority", path, "more than half of README H2 sections are exempt")


def validate_work(work_dir: Path, h2_headings: list[str], result: dict) -> str | None:
    brief_path = work_dir / "brief.json"
    bridges_path = work_dir / "bridges.json"
    brief = load_json(brief_path, result, "brief-json")
    bridges = load_json(bridges_path, result, "bridges-json")
    publish = validate_brief(brief, brief_path, result) if brief is not None else None
    if bridges is not None:
        validate_bridges(bridges, bridges_path, h2_headings, result)
    return publish


def outline_data(parsed: dict) -> dict:
    headings = parsed["headings"]
    output: list[dict] = []
    for index, heading in enumerate(headings):
        start = heading["end_line"]
        end = headings[index + 1]["line"] - 1 if index + 1 < len(headings) else len(parsed["lines"])
        signature = section_signature(parsed["lines"], parsed["code_mask"], start, end)
        output.append(
            {
                "level": heading["level"],
                "heading": heading["text"],
                "line": heading["line"],
                "line_count": max(0, end - start),
                "blocks": list(signature),
            }
        )
    return {"headings": output, "code_blocks": parsed["code_blocks"]}


def inspect_command(args: argparse.Namespace) -> dict:
    result = report("inspect", args.target)
    path, text, _ = read_utf8(args.target, result)
    if path is None or text is None:
        return result
    parsed = parse_markdown(path, text, result)
    for match in PLACEHOLDER_RE.finditer(parsed["visible"]):
        line = parsed["visible"].count("\n", 0, match.start()) + 1
        add_fail(result, "placeholder", path, "%s remains on line %d" % (match.group(0), line))
    inspect_structure(path, parsed, result)

    if args.no_work:
        add_warn(result, "work-files-skipped", path, "brief.json and bridges.json were skipped by --no-work")
        publish = "public"
    else:
        publish = validate_work(Path(args.work_dir), [h["text"] for h in parsed["headings"] if h["level"] == 2], result)
    # Unknown or invalid publish class is treated as public.
    inspect_links(path, parsed, result, public=(publish not in {"internal", "private"}))
    return result


def outline_command(args: argparse.Namespace) -> dict:
    result = report("outline", args.target)
    path, text, _ = read_utf8(args.target, result)
    if path is None or text is None:
        result["outline"] = {"headings": [], "code_blocks": 0}
        return result
    parsed = parse_markdown(path, text, result)
    result["outline"] = outline_data(parsed)
    return result


def nav_link(path: Path, destination: str, line: int, first_h2_line: int) -> bool:
    if line >= first_h2_line:
        return False
    local = local_destination(destination)
    if local is None:
        return False
    relative, _ = local
    return bool(relative) and Path(relative).parent in {Path("."), Path("")} and README_SIBLING_RE.match(Path(relative).name) is not None


def structural_sets(path: Path, parsed: dict) -> tuple[set[str], set[str]]:
    link_set: set[str] = set()
    image_set: set[str] = set()
    first_h2 = next((h["line"] for h in parsed["headings"] if h["level"] == 2), len(parsed["lines"]) + 1)
    header_text = "\n".join(
        "" if parsed["code_mask"][index] else parsed["lines"][index]
        for index in range(min(first_h2 - 1, len(parsed["lines"])))
    )
    header_nav = {
        destination
        for destination, is_image in links_from(header_text)
        if not is_image and nav_link(path, destination, 1, first_h2)
    }
    body_text = "\n".join(
        "" if parsed["code_mask"][index] else parsed["lines"][index]
        for index in range(max(0, first_h2 - 1), len(parsed["lines"]))
    )
    body_links = set(links_from(body_text))
    for destination, is_image in parsed["links"]:
        if not is_image and destination in header_nav and (destination, False) not in body_links:
            continue
        normalized = html.unescape(unquote(destination.strip()))
        (image_set if is_image else link_set).add(normalized)
    return link_set, image_set


def langs_command(args: argparse.Namespace) -> dict:
    result = report("langs", args.target)
    canonical_path, canonical_text, _ = read_utf8(args.target, result)
    if canonical_path is None or canonical_text is None:
        return result
    canonical = parse_markdown(canonical_path, canonical_text, result)
    canonical_links, canonical_images = structural_sets(canonical_path, canonical)
    expected_levels = [heading["level"] for heading in canonical["headings"]]

    for translation_arg in args.translations:
        nested = report("langs", translation_arg)
        translation_path, translation_text, _ = read_utf8(translation_arg, nested)
        if translation_path is None or translation_text is None:
            for item in nested["fails"]:
                add_fail(result, item["check"], item["path"], item["detail"])
            continue
        translated = parse_markdown(translation_path, translation_text, nested)
        for item in nested["fails"]:
            add_fail(result, item["check"], item["path"], item["detail"])
        levels = [heading["level"] for heading in translated["headings"]]
        if len(levels) != len(expected_levels):
            add_fail(result, "section-count", translation_path, "heading count differs: expected %d, got %d" % (len(expected_levels), len(levels)))
        if levels != expected_levels:
            add_fail(result, "heading-levels", translation_path, "heading level sequence differs: expected %s, got %s" % (expected_levels, levels))
        if translated["code_blocks"] != canonical["code_blocks"]:
            add_fail(result, "code-block-count", translation_path, "code block count differs: expected %d, got %d" % (canonical["code_blocks"], translated["code_blocks"]))
        links, images = structural_sets(translation_path, translated)
        if links != canonical_links:
            add_fail(result, "link-targets", translation_path, "link target set differs: expected %s, got %s" % (sorted(canonical_links), sorted(links)))
        if images != canonical_images:
            add_fail(result, "image-targets", translation_path, "image target set differs: expected %s, got %s" % (sorted(canonical_images), sorted(images)))
    return result


class Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.print_usage(sys.stderr)
        self.exit(2, "%s: error: %s\n" % (self.prog, message))


def build_parser() -> argparse.ArgumentParser:
    parser = Parser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    outline = subparsers.add_parser("outline", help="extract heading and block structure")
    outline.add_argument("target")
    outline.add_argument("--json", action="store_true", dest="as_json")

    inspect = subparsers.add_parser("inspect", help="inspect one README")
    inspect.add_argument("target")
    work = inspect.add_mutually_exclusive_group()
    work.add_argument("--work-dir", default=".readme-work")
    work.add_argument("--no-work", action="store_true")
    inspect.add_argument("--json", action="store_true", dest="as_json")

    langs = subparsers.add_parser("langs", help="compare translated README structures")
    langs.add_argument("target")
    langs.add_argument("translations", nargs="+")
    langs.add_argument("--json", action="store_true", dest="as_json")
    return parser


def print_human(result: dict) -> None:
    if result["command"] == "outline" and result["pass"]:
        print("OUTLINE %s" % result["target"])
    else:
        status = "PASS" if result["pass"] else "FAIL"
        print("%s %s %s" % (status, result["command"], result["target"]))
    if result["command"] == "outline" and "outline" in result:
        for heading in result["outline"]["headings"]:
            print("%s %s (line %d, %d lines) [%s]" % (
                "#" * heading["level"],
                heading["heading"],
                heading["line"],
                heading["line_count"],
                ", ".join(heading["blocks"]),
            ))
    for item in result["fails"]:
        print("FAIL %s %s: %s" % (item["check"], item["path"], item["detail"]))
    for item in result["warns"]:
        print("WARN %s %s: %s" % (item["check"], item["path"], item["detail"]))


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "inspect":
            result = inspect_command(args)
        elif args.command == "langs":
            result = langs_command(args)
        else:
            result = outline_command(args)
    except Exception as exc:
        # Runtime defects and unexpected I/O remain content failures, never usage errors.
        result = report(args.command, getattr(args, "target", ""))
        add_fail(result, "internal-error", getattr(args, "target", ""), "%s: %s" % (type(exc).__name__, exc))

    if args.as_json:
        contract = {key: result[key] for key in CONTRACT_KEYS}
        if args.command == "outline":
            contract["outline"] = result.get("outline", {"headings": [], "code_blocks": 0})
        print(json.dumps(contract, ensure_ascii=False, sort_keys=True))
    else:
        print_human(result)
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
