import unreal
import sys

unreal.log(f"引数リスト: {sys.argv}")

exported_files = sys.argv[1:-4]  # FBXファイルのパスすべてをリストにする
file_path = sys.argv[-4]  
replace = bool(int(sys.argv[-3])) 
import_materials = bool(int(sys.argv[-2])) 
import_textures = bool(int(sys.argv[-1])) 

unreal.log(f"FBXファイルのリスト: {exported_files}")
unreal.log(f"ファイルパス: {file_path}")
unreal.log(f"上書き: {replace}, マテリアル書き出し: {import_materials}, テクスチャ書き出し: {import_textures}")

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
