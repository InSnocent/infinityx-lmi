#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Verify and assemble the exact signed ROM ZIP from Release parts."""
from pathlib import Path
import argparse,json,hashlib,shutil,os
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--directory',type=Path,default=Path('.'))
p.add_argument('--output',type=Path)
args=p.parse_args()
folder=args.directory.resolve()
manifest=json.loads((folder/'release-manifest.json').read_text(encoding='utf-8'))['rom']
output=args.output or folder/manifest['filename']
if output.exists():raise SystemExit('Refusing to overwrite an existing file: '+str(output))
if not output.parent.is_dir():raise SystemExit('Output parent must already exist.')
if shutil.disk_usage(output.parent).free<manifest['bytes']+64*1024**2:
 raise SystemExit('Insufficient free space to assemble the ROM.')
temporary=output.with_name(output.name+'.partial')
if temporary.exists():raise SystemExit('Partial output already exists; inspect it before retrying.')
total=hashlib.sha256();size=0
try:
 with temporary.open('xb') as dest:
  for entry in manifest['parts']:
   name=entry['filename']
   if Path(name).name!=name:raise RuntimeError('Invalid part filename')
   source=folder/name
   if source.is_symlink():raise RuntimeError('Symlink part refused')
   part=hashlib.sha256();n=0
   with source.open('rb') as f:
    while chunk:=f.read(8*1024**2):
     part.update(chunk);total.update(chunk);dest.write(chunk);n+=len(chunk);size+=len(chunk)
   if n!=entry['bytes'] or part.hexdigest()!=entry['sha256']:
    raise RuntimeError('Part hash/size mismatch: '+name)
   print('Verified:',name)
 if size!=manifest['bytes'] or total.hexdigest()!=manifest['sha256']:
  raise RuntimeError('Combined ROM hash/size mismatch')
 if output.exists():raise RuntimeError('Output appeared during assembly; refusing to replace it')
 # Link first so an existing output can never be overwritten, even in a race.
 os.link(temporary,output);temporary.unlink()
 print('ROM verified:',output.name)
 print('SHA-256:',total.hexdigest())
except BaseException:
 if temporary.exists():temporary.unlink()
 raise
