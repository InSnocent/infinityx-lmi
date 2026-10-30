#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Apply this release's two ROM adaptations without resetting user changes."""
from pathlib import Path
import argparse,json,subprocess
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('android_root',type=Path)
args=parser.parse_args()
source=args.android_root.resolve()
release=Path(__file__).resolve().parents[1]
pins=json.loads((release/'SOURCES.json').read_text())['device_revisions']
jobs=[
 ('device/xiaomi/lmi','patches/rom/0001-infinity-lmi-product.patch'),
 ('device/xiaomi/sm8250-common','patches/rom/0002-infinity-common-config.patch'),
]
pending=[]
for relative,patch in jobs:
 repo=source/relative
 head=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()
 if head!=pins[relative]:raise SystemExit('Unexpected baseline: '+relative)
 path=release/patch
 reverse=subprocess.run(['git','-C',str(repo),'apply','--reverse','--check',str(path)],capture_output=True)
 if reverse.returncode==0:
  print('Already applied:',relative);continue
 check=subprocess.run(['git','-C',str(repo),'apply','--check',str(path)],capture_output=True,text=True)
 if check.returncode:raise SystemExit('Patch does not apply cleanly to '+relative+'\n'+check.stderr)
 pending.append((repo,path))
for repo,path in pending:
 subprocess.run(['git','-C',str(repo),'apply',str(path)],check=True)
 print('Applied:',repo.relative_to(source))
