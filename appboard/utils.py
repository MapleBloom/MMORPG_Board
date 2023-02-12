def get_text_from_html(html):
    content = str(html)
    curr = content
    text_list = []
    sub_text = []
    count = 0
    num = 0
    symbols = ['<', '>', '&', ';']
    for c in content:
        curr = curr[1:]
        if len(text_list) >= 64:
            break
        if c == '\n' or c == '\r':
            c = ' '
        if count == 0 and num == 0 and c not in symbols:
            if (c != ' ') or (c == ' ' and (text_list == [] or text_list[-1] != ' ')):
                text_list.append(c)
        if c == '<':
            count += 1
        elif c == '>':
            count -= 1
        if c == '&':
            num += 1
            sub_text.append(c)
        elif c == ';':
            num -= 1
            if num == 0:
                sub_text = []
        if num < 0 or num > 1:
            num = 0
            if sub_text:
                text_list.append(sub_text)
                sub_text = []
    if sub_text and ('&' not in curr and ';' not in curr):
        text_list.append(sub_text)
    return ''.join(text_list)
