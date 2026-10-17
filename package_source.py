"""Build the portable source package and copy its documentation into the source viewer."""
from pathlib import Path
import shutil
import zipfile
ROOT = Path(__file__).resolve().parent
included = ['FEATURE_COMPARISON.md', 'README.md', 'DATA_README.md', 'prepare_data.py', 'serve.py', 'check_engine.cjs', 'check_workspace.cjs', 'AI_SETUP.md', 'INPUT_REVIEW.md', 'package_source.py', '.gitignore']
folder = ROOT / 'dist' / 'source'
(folder / 'files').mkdir(parents=True, exist_ok=True)
for name in included:
    if not name.startswith('.'):
        shutil.copyfile(ROOT / name, folder / 'files' / name)
archive = folder / 'microbelog-source.zip'
with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for name in included:
        z.write(ROOT / name, 'microbelog/' + name)
    for path in sorted((ROOT / 'dist').rglob('*')):
        if path.is_file() and path != archive:
            z.write(path, 'microbelog/' + path.relative_to(ROOT).as_posix())
print(archive)
