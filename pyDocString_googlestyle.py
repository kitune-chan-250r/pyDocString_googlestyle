'''commands

Todo:
    *パーサーメソッドを用意しdocstringを読み込む
    *ホバーしているメソッド呼び出しのメソッドが同じファイルにあるか判別
    ＞パース＞コンテンツ生成＞show popup
'''

import sublime, sublime_plugin, mdpopups

class InsertModuleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        text = ['hello world']
        self.view.show_popup_menu(text, None)

class InsertClassCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, 'hello world')

class InsertFuncCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, 'hello world')
        
class TestCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        text = ['hello world']
        window = sublime.active_window()
        #self.view.show_popup_menu(text, None)
        content = ''
        self.view.show_popup(content)

class ShowPopupCommand(sublime_plugin.TextCommand):
    def run(self, edit, point, flags):
        '''ポップアップを表示

        Todo:
            *パーサーメソッドを用意しdocstringを読み込む
            *ホバーしているメソッド呼び出しのメソッドが同じファイルにあるか判別
            ＞パース＞コンテンツ生成＞show popup
        '''
        #popupの位置に使う
        line = self.view.rowcol(point)[0] + 1
        location = _visivle_text_point(self.view, line - 1, 0)

        #potisonからスコープネームや単語を取得
        str_word = self.view.substr(self.view.word(point)) #カーソル位置の単語取得
        scope = self.view.scope_name(point)
        print(scope)
        score_class = self.view.score_selector(point, 'entity.name.class.python')
        score_method = self.view.score_selector(point, 'entity.name.function.python')
        score_fanc_call = self.view.score_selector(point, 'meta.function-call.python')
        #関数かクラスか判別
        if score_class > 0:
            scope_type = 'Class'
        elif score_method > 0 or score_fanc_call > 0:
            scope_type = 'Function'
        else:
            return

        css = _load_popup_css('popup.css')

        content = (
                    '<div class="content">'
                    '{0} : {1}'
                    '</div>'
                ).format(scope_type, str_word)
        #show_popupのcontentはHTML形式で記述
        self.view.show_popup(content, sublime.HIDE_ON_MOUSE_MOVE_AWAY, point)
        #mdpopups.show_popup(self.view, content, css, flags, location)
        mdpopups.update_popup(self.view, content, None, css)

        ext = self.view.extract_scope(point)
        lines = self.view.substr(ext)

def _visivle_text_point(view, row, col):
    viewport = view.visible_region()
    _, vp_col = view.rowcol(viewport.begin())
    return view.text_point(row, vp_col + col)

def _load_popup_css(path):
    css_lines = []
    css_path = 'Packages/pyDocString_googlestyle/' + path
    css_lines.append(sublime.load_resource(css_path))
    return ''.join(css_lines)

def _to_html(text):
    yield html.escape(text, quote=False).replace('  ', '&nbsp;&nbsp;') or '↵'

class EventListener(sublime_plugin.EventListener):
    #　マウスオーバーでこのメソッドが実行
    def on_hover(self, view, point, hover_zone):
        '''sublimeの設定をインポートしてホバーが有効日されているか判定
        if not view_settings.get('enable_hover_diff_popup'):
            return
        
        参考コードではここでポップアップを出力するコマンドを実行している'''

        view.run_command('show_popup', {
            'point': point, 'flags': sublime.HIDE_ON_MOUSE_MOVE})

        view.find()
        
        