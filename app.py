def remove_lines_from_file(source_filename, delete_filename, output_filename):
    """
    source_filenameからdelete_filenameに記載された行を削除し、
    結果をoutput_filenameに出力します。
    """
    
    # 2. 削除対象の特定
    # セット（set）を使うことで、行の検索を高速に行えます。
    # strip()を使って行末の改行文字を削除し、正確な比較ができるようにします。
    lines_to_delete = set()
    try:
        with open(delete_filename, 'r', encoding='utf-8') as f_delete:
            for line in f_delete:
                # 削除対象ファイルを読み込む際も、行末の改行文字を削除
                lines_to_delete.add(line.strip())
    except FileNotFoundError:
        print(f"エラー: 削除対象ファイル '{delete_filename}' が見つかりません。")
        return

    # 3. フィルタリング & 4. 結果の出力
    deleted_lines_count = 0
    
    try:
        with open(source_filename, 'r', encoding='utf-8') as f_source, \
             open(output_filename, 'w', encoding='utf-8') as f_output:
            
            for line in f_source:
                # ソースファイルを読み込む際も、行末の改行文字を削除して比較
                stripped_line = line.strip()
                
                # 削除対象セットに含まれていない行のみを書き出す
                if stripped_line not in lines_to_delete:
                    # 元のファイルから読み込んだ改行文字付きの行をそのまま書き込む
                    f_output.write(line)
                else:
                    deleted_lines_count += 1
                    
    except FileNotFoundError:
        print(f"エラー: 元ファイル '{source_filename}' が見つかりません。")
        return
        
    print(f"処理が完了しました。")
    print(f"  - 削除対象ファイル: '{delete_filename}'")
    print(f"  - 元ファイル: '{source_filename}'")
    print(f"  - 削除行数: {deleted_lines_count} 行")
    print(f"  - 結果出力ファイル: '{output_filename}'")
    
# プログラムの実行
remove_lines_from_file("target1.txt", "target1_delete.txt", "target1_deleted.txt")
# remove_lines_from_file("target2.txt", "target2_delete.txt", "target2_deleted.txt")

# --- 結果の確認（オプション） ---
print("\n--- target1_deleted.txt の内容 ---")
try:
    with open("target1_deleted.txt", "r", encoding="utf-8") as f:
        print(f.read())
except FileNotFoundError:
    print("出力ファイルが見つかりません。")