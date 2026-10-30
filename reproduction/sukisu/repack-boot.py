#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
from pathlib import Path
import os,shlex,json,subprocess,hashlib,shutil
BASE=Path(__file__).resolve().parent
ROOT=Path(os.environ.get('ANDROID_ROOT','')).resolve()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(cmd):return subprocess.check_output([str(x) for x in cmd],text=True,stderr=subprocess.STDOUT)
baseline=BASE/'baseline/boot.img'
if sha(baseline)!='21283479f70c40ee77b7b74b953d85072b78ab52e7def464d918aa0356b22cb7':
 raise SystemExit('Baseline boot does not match this ROM release.')
report=json.loads((BASE/'abi-verification.json').read_text())
image=BASE/'out/arch/arm64/boot/Image'
if not report['passed'] or report['image_sha256']!=sha(image):
 raise SystemExit('Run verify-abi.py against this exact kernel first.')
tools=ROOT/'out/host/linux-x86/bin'
unpack=tools/'unpack_bootimg';mk=tools/'mkbootimg';avb=tools/'avbtool'
dest=BASE/'artifacts';dest.mkdir(exist_ok=True)
old_dir=dest/'baseline-unpacked';old_dir.mkdir(exist_ok=True)
old_args=shlex.split(run([unpack,'--boot_img',baseline,'--out',old_dir,'--format','mkbootimg']))
args=old_args.copy();args[args.index('--kernel')+1]=str(image)
boot=dest/'boot-lmi-infinityx-sukisu-v4.3.0.img'
run([mk]+args+['--output',str(boot)])
run([avb,'add_hash_footer','--image',boot,'--partition_name','boot','--partition_size','134217728',
 '--algorithm','NONE','--salt','457aa4e09a67387f22e3944727b7739c2d0f989cf998d3c7d18e5e09a7fd7243',
 '--prop','com.android.build.boot.os_version:16',
 '--prop','com.android.build.boot.fingerprint:POCO/infinity_lmi/lmi:16/BP4A.251205.006/eng.androi.20261029.063319:userdebug/release-keys'])
shutil.copy2(boot,dest/'boot.img')
verification=run([avb,'verify_image','--image',dest/'boot.img'])
new_dir=dest/'new-unpacked';new_dir.mkdir(exist_ok=True)
new_args=shlex.split(run([unpack,'--boot_img',boot,'--out',new_dir,'--format','mkbootimg']))
for values in [old_args,new_args]:
 for name in ['--kernel','--ramdisk','--dtb']:values[values.index(name)+1]='<'+name[2:]+'>'
assert old_args==new_args,'Boot metadata changed'
for name in ['ramdisk','dtb']:assert sha(old_dir/name)==sha(new_dir/name),name
assert sha(new_dir/'kernel')==sha(image)
assert boot.stat().st_size==134217728
result={'passed':True,'filename':boot.name,'sha256':sha(boot),'bytes':boot.stat().st_size,
 'kernel_sha256':sha(image),'ramdisk_unchanged':True,'dtb_unchanged':True,'header_and_cmdline_unchanged':True,
 'avb_verify_succeeded':True,'baseline_boot_sha256':sha(baseline)}
(dest/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
