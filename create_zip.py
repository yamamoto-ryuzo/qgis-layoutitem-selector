
import os
import zipfile
import glob

def read_metadata():
    meta = {}
    with open('metadata.txt', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                meta[k.strip()] = v.strip()
    return meta

def increment_version(ver):
    parts = ver.split('.')
    if len(parts) == 3 and all(p.isdigit() for p in parts):
        parts[2] = str(int(parts[2]) + 1)
        return '.'.join(parts)
    return ver

def main():
    meta = read_metadata()
    plugin_name = os.path.basename(os.getcwd()).replace('-', '_')
    repo_name = os.path.basename(os.getcwd())
    old_version = meta.get('version', '1.0.0')
    new_version = increment_version(old_version)

    # metadata.txtのversionを書き換え
    with open('metadata.txt', encoding='utf-8') as f:
        lines = f.readlines()
    with open('metadata.txt', 'w', encoding='utf-8') as f:
        for line in lines:
            if line.strip().startswith('version='):
                f.write(f'version={new_version}\n')
            else:
                f.write(line)
    print(f'バージョン: {old_version} → {new_version}')

    # 古いZIP削除
    for z in glob.glob(f'{repo_name}_v*.zip'):
        try:
            os.remove(z)
            print(f'古いZIP削除: {z}')
        except Exception as e:
            print(f'削除失敗: {z} {e}')

    # 必要ファイル
    include = [
        '__init__.py',
        'layout_item_selector.py',
        'metadata.txt',
        'resources.py',
        'resources.qrc',
        'icon.png',
        'README.md',
        'LICENSE'
    ]
    # i18n, ui ディレクトリも含める
    include_dirs = ['i18n', 'ui']

    zipname = f'{repo_name}_v{new_version}.zip'
    with zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # ファイル
        for f in include:
            if os.path.exists(f):
                zipf.write(f, f'{plugin_name}/{f}')
                print(f'追加: {f}')
        # ディレクトリ
        for d in include_dirs:
            if os.path.isdir(d):
                for root, dirs, files in os.walk(d):
                    for file in files:
                        rel = os.path.relpath(os.path.join(root, file), '.')
                        zipf.write(rel, f'{plugin_name}/{rel}')
                        print(f'追加: {rel}')
    print(f'✓ 配布用ZIP作成: {zipname}')

if __name__ == '__main__':
    main()
