# -*- coding: utf-8 -*-
import zipfile, os, glob

zip_name = '编程领域知识库_V2_100领域10000知识点.zip'
zf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)

# 添加所有领域JSON文件
for f in sorted(glob.glob('domains/*.json')):
    arcname = os.path.join('domains', os.path.basename(f))
    zf.write(f, arcname)

# 添加索引和README
zf.write('domains_index.json')
zf.write('README.md')

zf.close()

size_mb = os.path.getsize(zip_name) / 1024 / 1024
print(f'ZIP创建完成: {zip_name}')
print(f'文件大小: {size_mb:.2f} MB')
print(f'包含文件数: {len(zf.namelist())}')
