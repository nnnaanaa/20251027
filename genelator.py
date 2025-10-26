import random
import string

def generate_random_line(length):
    # 使用する文字セット: 英大文字、英小文字、数字、一部の記号
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(length))

print("--- パターン 1: ランダムな半角英数字と記号 (15バイト x 20列) ---")
for i in range(20):
    line = generate_random_line(15)
    # 行番号を付けて出力 (表示上は20行としてカウント)
    print(f"[{i+1:02d}] {line}")