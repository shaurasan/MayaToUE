import unreal
import sys

unreal.log(f"引数リスト: {sys.argv}")

# 🔥 1番目から-5番目までをFBXファイルリストとする
exported_files = sys.argv[1:-5]  # 🔥 FBXファイルのパスすべてをリストにする
file_path = sys.argv[-5]  # 🔥 最後の5つの引数の1つ目がファイルパス
replace = bool(int(sys.argv[-4]))  # 🔥 最後の4つ目
import_materials = bool(int(sys.argv[-3]))  # 🔥 最後の3つ目
import_textures = bool(int(sys.argv[-2]))  # 🔥 最後の2つ目
temp_box = bool(int(sys.argv[-1]))  # 🔥 最後の1つ目

unreal.log(f"FBXファイルのリスト: {exported_files}")
unreal.log(f"ファイルパス: {file_path}")
unreal.log(f"上書き: {replace}, マテリアル書き出し: {import_materials}, テクスチャ書き出し: {import_textures}, 座標維持: {temp_box}")

for source_file_path in exported_files:
    unreal.log(f"インポート中: {source_file_path}")

    task = unreal.AssetImportTask()

    task.set_editor_property("automated", True)
    task.set_editor_property("filename", source_file_path)
    task.set_editor_property("destination_path", file_path)
    task.set_editor_property("replace_existing", replace)
    task.set_editor_property("save", True)

    import_ui = unreal.FbxImportUI()
    import_ui.reset_to_default()

    import_ui.mesh_type_to_import = unreal.FBXImportType.FBXIT_STATIC_MESH
    import_ui.original_import_type = unreal.FBXImportType.FBXIT_STATIC_MESH
    import_ui.import_animations = False
    import_ui.import_as_skeletal = False
    import_ui.import_materials = import_materials
    import_ui.import_textures = import_textures
    import_ui.import_mesh = True

    task.options = import_ui

    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])

unreal.log("アセットインポートが完了しました。")
