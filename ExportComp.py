import os
import maya.cmds as cmds
import time
import sys

# UI作成
def create_ui():
    # ウィンドウが開いていたら閉じる
    if cmds.window("customUI", exists=True):
        cmds.deleteUI("customUI", window=True)

    # 新しいウィンドウ作成
    window = cmds.window("customUI", title="AutoExporter", widthHeight=(400, 250), sizeable=False)

    # レイアウト
    cmds.columnLayout(adjustableColumn=True)

    # トグルボタン
    cmds.text(label="書き出し読み込み設定", align="center")
    cmds.checkBox('toggle1', label="上書き保存", value=True)  # 🔥 名前付き
    cmds.checkBox('toggle2', label="マテリアル書き出し", value=True)  # 🔥 名前付き
    cmds.checkBox('toggle3', label="テクスチャ書き出し", value=True)  # 🔥 名前付き
    cmds.checkBox('toggle4', label="座標をそのままで(未実装)", value=True)  # 🔥 名前付き

    cmds.separator(height=10, style='in')

    # ファイル指定パスフィールド (🔥 objectName='file_path'を追加)
    cmds.text(label="Select UE paths", align="center")
    cmds.textFieldButtonGrp('file_path', label="File Path", buttonCommand=lambda: browse_file_path('file_path'))
    cmds.symbolButton(image="fileOpen.png", command=lambda *args: browse_file_path('file_path'))

    # 実行ボタン
    cmds.separator(height=10, style='in')
    cmds.button(label="実行", command=lambda x: execute_action())

    cmds.showWindow(window)


# ファイルパスを選択
def browse_file_path(text_field):
    file_path = cmds.fileDialog2(fileMode=3, caption="ディレクトリを選択")
    if file_path:
        cmds.textFieldButtonGrp(text_field, edit=True, text=file_path[0])  # 🔥 文字列に変換


create_ui()


# リモート実行プロセス
sys.path.append("C:/UE/UE_5.4/Engine/Plugins/Experimental/PythonScriptPlugin/Content/Python")
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
    selected_objects = cmds.ls(selection=True)
    if not selected_objects:
        cmds.warning("オブジェクトが選択されていません")
        return []

    # projectのルートディレクトリ取得
    project_directory = cmds.workspace(query=True, rootDirectory=True)
    export_directory = os.path.join(project_directory, 'data')

    # dataフォルダが存在しなければ作成する
    if not os.path.exists(export_directory):
        os.makedirs(export_directory)
        print(f"フォルダを作成しました: {export_directory}")

    # 選択オブジェクトをFBXに書き出し
    exported_files = []
    for obj in selected_objects:
        export_path = os.path.join(export_directory, f"{obj}.fbx")
        try:
            cmds.select(obj, replace=True)
            cmds.file(
                export_path,
                force=True,
                options="mo=1;mt=1;tf=1;",
                type="FBX export",
                preserveReferences=True,
                exportSelected=True
            )
            print(f"書き出し先: {export_path}")
            exported_files.append(export_path)
        except Exception as e:
            print(f"書き出しに失敗: {obj}, エラー: {e}")

    if exported_files:
        print("書き出し完了。UEに送信中です。")

    return exported_files


# 引数の送信
def execute_action():
    toggle1_state = cmds.checkBox('toggle1', query=True, value=True)  # 🔥 名前でUI要素を参照
    toggle2_state = cmds.checkBox('toggle2', query=True, value=True)  # 🔥 名前でUI要素を参照
    toggle3_state = cmds.checkBox('toggle3', query=True, value=True)  # 🔥 名前でUI要素を参照
    toggle4_state = cmds.checkBox('toggle4', query=True, value=True)  # 🔥 名前でUI要素を参照
    file_path = cmds.textFieldButtonGrp('file_path', query=True, text=True)  # 🔥 名前でUI要素を参照

    exported_files = export_selected_objects()

    if exported_files:
        UERemoteExecution.execute_file(
            "Py_ImportCom.py",
            *exported_files,  # 🔥 リストからスペース区切りの文字列に変換
            file_path,
            str(int(toggle1_state)),
            str(int(toggle2_state)),
            str(int(toggle3_state)),
            str(int(toggle4_state))
        )
    else:
        cmds.warning("ディレクトリが選択されていません")
