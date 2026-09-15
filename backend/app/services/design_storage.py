from pathlib import Path
from app.config import settings,BASE_DIR
import shutil

# 设计稿存放路径
def design_root() -> Path:
    configured = settings.design_asset_dir.strip()
    return Path(configured).expanduser().resolve if configured else (BASE_DIR/"data"/"design-assets").resolve()

# 删除指定项目对应的所有设计稿文件夹
def remove_project_designs(project_id:int) -> None:
    root = design_root()
    project_dir = (root/str(project_id)).resolve()
    if root in project_dir.parents:
        shutil.rmtree(project_dir,ignore_errors=True)