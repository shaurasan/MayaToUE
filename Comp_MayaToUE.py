from maya import cmds
from maya.common.ui import LayoutManager
import os
import time
import sys


def create_ui():
    if cmds.window('ImportTools', ex = True):
        cmds.deleteUI('ImportTools')
    cmds.window('ImportTools', title = 'MayaToUnreal', widthHeight = (400,250), sizeable = False)
            
    tabs = cmds.tabLayout(innerMarginWidth = 5, innerMarginHeight = 5)
    child1 = cmds.columnLayout(adjustableColumn = True, rowSpacing = 10)

    cmds.text('インポート設定', font = 'boldLabelFont')

    #チェックボックス
    cmds.checkBox('replace', label = '上書き保存', value = True)
    cmds.checkBox('material', label = 'マテリアル書き出し', value = True)
    cmds.checkBox('texture', label = 'テクスチャ書き出し', value = True)

    cmds.separator(height = 10, style='in')

    with LayoutManager(cmds.rowLayout(numberOfColumns = 3, adj = 2)) as field:
        
        #テキストボックスとボタン
        cmds.text('インポート先')
        cmds.textField('file_path')
        cmds.iconTextButton(image = 'browseFolder.png', st = 'iconOnly', command = lambda: browse_file_path('file_path'))

    cmds.button(label = '実行', command =lambda _: execute_action())
        
    cmds.tabLayout(tabs, e = True, tabLabel = [(child1, 'ImportOption')])

    cmds.showWindow('ImportTools')

def browse_file_path(text_field):
    file_path = cmds.fileDialog2(fileMode = 3, caption = 'インポート先を選択')
    if file_path:
        cmds.textField(text_field, edit = True, text = file_path[0])

create_ui()

#-----処理ライン-----



from remote_execution import RemoteExecution

class UERemoteExecution:
    @classmethod
    def execute_file(cls, file_path: str, *args):
        remote_execute = RemoteExecution()
        remote_execute.start()

        time.sleep(2)
        if remote_execute.remote_nodes:
            remote_execute.open_command_connection(remote_execute.remote_nodes[0])
            remote_execute.run_command(f"{file_path} {' '.join(args)}")
        remote_execute.stop()




# 書き出しプロセス
def export_selected_objects():
    # オブジェクト取得
    selected_objects = cmds.ls(selection = True)
    if not selected_objects:
        cmds.warning('オブジェクトが選択されていません')
        return []

    # projectのルートディレクトリ取得
    project_directory = cmds.workspace(query = True, rootDirectory = True)
    export_directory = os.path.join(project_directory, 'data')

    # dataフォルダが存在しなければ作成する
    if not os.path.exists(export_directory):
        os.makedirs(export_directory)
        print(f'フォルダを作成しました: {export_directory}')

    # 選択オブジェクトをFBXに書き出し
    exported_files = []
    for obj in selected_objects:
        export_path = os.path.join(export_directory, f'{obj}.fbx')
        try:
            cmds.select(obj, replace=True)
            cmds.file(
                export_path,
                force = True,
                options = 'mo = ; mt = 1; tf = 1; upAxis = z ; zAxis = y ; unitScale = 1;',
                type = 'FBX export',
                preserveReferences = True,
                exportSelected = True
            )
            print(f'書き出し先: {export_path}')
            exported_files.append(export_path)
        except Exception as e:
            print(f'書き出しに失敗: {obj}, エラー: {e}')

    if exported_files:
        print('書き出し完了。UEに送信中です。')

    return exported_files


# 引数の送信
def execute_action():
    toggle1_state = cmds.checkBox('replace', query = True, value = True)  
    toggle2_state = cmds.checkBox('material', query = True, value = True)  
    toggle3_state = cmds.checkBox('texture', query = True, value = True)  
    file_path = cmds.textField('file_path', query = True, text = True)  
    exported_files = export_selected_objects()

    if exported_files:
        UERemoteExecution.execute_file(
            'Py_ImportSample.py',
            *exported_files,  # リストからスペース区切りの文字列に変換
            file_path,
            str(int(toggle1_state)),
            str(int(toggle2_state)),
            str(int(toggle3_state)),
        )
    else:
        cmds.warning('ディレクトリが選択されていません')
