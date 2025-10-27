import difflib

# 比較対象のファイル名
file1_name = "target1.txt"
file2_name = "target1_deleted.txt"

# --- 1. ファイル内容の読み込み ---
try:
    with open(file1_name, 'r', encoding='utf-8') as f1:
        # 行末の改行文字を保持したままリストとして読み込み
        lines1 = f1.readlines()
    with open(file2_name, 'r', encoding='utf-8') as f2:
        lines2 = f2.readlines()
except FileNotFoundError:
    print("エラー: ファイルが見つかりません。ファイル名を確認してください。")
    print(f"確認ファイル: {file1_name} および {file2_name}")
    exit()

# --- 2. 差分比較と集計 ---
differ = difflib.Differ()
diff = list(differ.compare(lines1, lines2))

# 差分行の集計用カウンター
deleted_count = 0     # target1 にのみ存在する行 (削除)
added_count = 0       # target2 にのみ存在する行 (追加)
changed_set_count = 0 # 変更された行のペアの数

# 差分結果を格納するリスト (表示用に整形)
output_lines = []
# 変更行の一時保存用 ('-'行を保存し、直後に'+'が来た場合に'変更'として再利用)
temp_deleted_line = None

for line in diff:
    prefix = line[0:2] # '  ', '- ', '+ ', '? '
    content = line[2:].rstrip() # 行末の改行文字などを除去
    
    if prefix == '- ':
        # 直前に '-' があった場合 (複数行削除の途中)
        if temp_deleted_line:
            # 前の '-' 行を「削除」として確定
            deleted_count += 1
            output_lines.append(f"**- 削除:** {temp_deleted_line}")
        
        # 現在の '-' 行を一時保存（次に '+' が来るかを確認するため）
        temp_deleted_line = content
        
    elif prefix == '+ ':
        # 直前に '-' の一時保存がある場合 -> 「変更」と見なす
        if temp_deleted_line:
            changed_set_count += 1
            # 削除行と追加行をセットで「変更」として出力リストに追加
            output_lines.append(f"**- 変更(元):** {temp_deleted_line}")
            output_lines.append(f"**+ 変更(新):** {content}")
            temp_deleted_line = None # 変更として処理済み
        else:
            # 直前に '-' がない場合 -> 「追加」と見なす
            added_count += 1
            output_lines.append(f"**+ 追加:** {content}")
        
    elif prefix in ('  ', '? '):
        # 共通行または変更の詳細行の場合
        # '-' の一時保存があれば、それは確定した「削除」行
        if temp_deleted_line:
            deleted_count += 1
            output_lines.append(f"**- 削除:** {temp_deleted_line}")
            temp_deleted_line = None # 削除として処理済み

# 最後に残った '-' 行があれば、それは「削除」として確定
if temp_deleted_line:
    deleted_count += 1
    output_lines.append(f"**- 削除:** {temp_deleted_line}")


# --- 3. 結果の出力 ---
print(f"## ファイル差分 ({file1_name} vs {file2_name})")
print("-" * 50)

# 整形した差分行を出力
for line in output_lines:
    # 期待される出力形式（変更行をセットで表示）に調整して出力
    if line.startswith("**- 変更(元):"):
        # 削除・追加を区別せず、期待される出力形式に統一
        print(line.replace("**- 変更(元):", "**- 変更:"))
    elif line.startswith("**+ 変更(新):"):
        print(line.replace("**+ 変更(新):", "**+ 変更:"))
    else:
        print(line)

print("-" * 50)

print("\n## 差分行の合計数")
print(f"**- 削除された行** ({file1_name} にのみ存在): **{deleted_count} 行**")
print(f"**+ 追加された行** ({file2_name} にのみ存在): **{added_count} 行**")
print(f"**± 変更された行** (対応する行が異なる): **{changed_set_count} 行**")