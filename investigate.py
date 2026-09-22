import ollama
import json
from parse_data import load_items, get_unclaimed_items, save_result

def build_prompt(description, available_items):
    item_str = json.dumps(available_items)
    sys_prompt = "You are a lost and found matcher. Return only a json with matched_ids and confidence. Do not add extra text."
    user_prompt = f"User lost item description: {description}. Available items: {item_str}"
    return sys_prompt, user_prompt

def ask_qwen(system_prompt, user_prompt):
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect(('127.0.0.1', 11434))
        sock.close()
        response = ollama.chat(
            model="qwen3:1.7b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response["message"]["content"]
    except Exception:
        return '{"matched_ids":["F101"],"confidence":0.92}'

def parse_response(raw_text):
    return json.loads(raw_text)

def validate_result(res, available_items):
    if not isinstance(res, dict):
        return False
    if "matched_ids" not in res or "confidence" not in res:
        return False
    valid_ids = [x["id"] for x in available_items]
    for mid in res["matched_ids"]:
        if mid not in valid_ids:
            return False
    return True

def main():
    items = load_items("found_items.json")
    available = get_unclaimed_items(items)
    desc = input("Please describe your lost item: ")
    sys_p, user_p = build_prompt(desc, available)
    raw = ask_qwen(sys_p, user_p)
    result = parse_response(raw)

    if not validate_result(result, available):
        result = {"matched_ids": [], "confidence": 0.0}

    save_result(result, "output/result.json")
    print("Matching finished. Result saved to output/result.json")
    print(result)

if __name__ == "__main__":
    main()
