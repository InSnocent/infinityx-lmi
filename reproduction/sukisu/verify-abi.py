#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
from pathlib import Path
import hashlib,json,sys
BASE=Path(__file__).resolve().parent
RELEASE=BASE.parents[1]
def symvers(path):
 result={}
 for line in path.read_text().splitlines():
  f=line.split()
  if len(f)>=3:result[f[1]]=int(f[0],16)
 return result
old=symvers(RELEASE/'configs/baseline-Module.symvers')
new=symvers(BASE/'out/Module.symvers')
release=(BASE/'out/include/config/kernel.release').read_text().strip()
expected=(RELEASE/'configs/kernel.release').read_text().strip()
missing=[n for n in old if n not in new]
changed=[n for n in old if n in new and old[n]!=new[n]]
image=BASE/'out/arch/arm64/boot/Image'
passed=release==expected and not missing and not changed
result={'passed':passed,'release':release,'baseline_export_count':len(old),'new_export_count':len(new),
 'missing_exports':missing,'changed_crcs':changed,'image_sha256':hashlib.sha256(image.read_bytes()).hexdigest(),
 'scope':'Checks all baseline export CRCs, including those needed by the original vendor modules. Runtime hardware still needs testing.'}
(BASE/'abi-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
if not passed:sys.exit(1)
