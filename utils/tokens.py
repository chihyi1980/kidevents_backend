import tiktoken

#計算發送到open ai 的message 有多少tokens
def count_tokens(text, model="gpt-4"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

#裁減超過的tokens
def trim_content(msg_template, tags_str, event_content, max_tokens=128000, model="gpt-4"):
    total_msg = msg_template + tags_str + event_content
    total_tokens = count_tokens(total_msg, model)

    if total_tokens <= max_tokens:
        return event_content  # 不需要裁減

    # 計算可用的 token 數量
    fixed_tokens = count_tokens(msg_template + tags_str, model)
    available_tokens = max_tokens - fixed_tokens

    # 使用二分搜尋法找到最大可用的內容長度
    encoding = tiktoken.encoding_for_model(model)
    encoded_content = encoding.encode(event_content)
    if available_tokens <= 0:
        return ""  # 無法包含任何內容

    trimmed_encoded_content = encoded_content[:available_tokens]
    trimmed_content = encoding.decode(trimmed_encoded_content)
    return trimmed_content
