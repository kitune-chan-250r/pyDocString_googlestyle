import re

method_text = r'def func_name(args):\n    args = 1\n    return args'
class_text = r"""
def run(self, edit, point, flags):
    '''ポップアップを表示

    Todo:
        *パーサーメソッドを用意しdocstringを読み込む
        *ホバーしているメソッド呼び出しのメソッドが同じファイルにあるか判別
        ＞パース＞コンテンツ生成＞show popup
    '''
"""

def is_func(text):
    pattern = "'''.*'''"
    res = re.search(pattern, text, re.S)
    return res.group()

print(is_func(class_text))