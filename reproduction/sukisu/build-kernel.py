#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
from pathlib import Path
import os,sys,json,subprocess,shutil,fcntl,time,signal,datetime,difflib
BASE=Path(__file__).resolve().parent
ROOT=Path(os.environ.get('ANDROID_ROOT','')).resolve()
if not (ROOT/'build/envsetup.sh').is_file():
    raise SystemExit('Set ANDROID_ROOT to the fixed Android source checkout.')
RELEASE=BASE.parents[1]
baseline=BASE/'baseline'
baseline.mkdir(exist_ok=True)
for source_name,target_name in [('kernel-baseline.config','.config'),('baseline-Module.symvers','Module.symvers'),('kernel.release','kernel.release')]:
    target=baseline/target_name
    if not target.exists():shutil.copy2(RELEASE/'configs'/source_name,target)
JOBS=int(os.environ.get('JOBS','8'))
if not 1 <= JOBS <= 64:raise SystemExit('JOBS must be between 1 and 64.')
KERNEL=BASE/'kernel'
OUT=BASE/'out'
LOG=BASE/'build.log'
STATUS=BASE/'build-status.json'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(data):
    tmp=STATUS.with_suffix('.tmp');tmp.write_text(json.dumps(data,indent=2)+'\n');tmp.replace(STATUS)
def config(path):
    result={}
    for line in path.read_text().splitlines():
        if line.startswith('CONFIG_') and '=' in line:
            k,v=line.split('=',1);result[k]=v
        elif line.startswith('# CONFIG_') and line.endswith(' is not set'):
            result[line[2:-11]]='n'
    return result
lock=open(BASE/'build.lock','a+')
fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
assert (BASE/'baseline/boot.img').stat().st_size==134217728
assert (KERNEL/'drivers/kernelsu/Kconfig').is_file(), 'integration not ready'
assert (KERNEL/'.scmversion').read_text().strip()=='-g71b13e62f057'
assert not subprocess.check_output(['git','-C',str(ROOT/'kernel/xiaomi/sm8250'),'status','--porcelain'],text=True).strip(), 'original kernel checkout changed'
OUT.mkdir(exist_ok=True)
state={'phase':'configuring','started_utc':now(),'pid':os.getpid(),'output':str(OUT),'jobs':JOBS,'phone_writes':False}
save(state)
env=dict(os.environ)
paths=['out/host/linux-x86/bin','prebuilts/tools-lineage/linux-x86/bin','prebuilts/build-tools/linux-x86/bin','prebuilts/clang/host/linux-x86/clang-r563880c/bin','prebuilts/rust/linux-x86/1.88.0/bin','prebuilts/clang-tools/linux-x86/bin']
env.update(PATH=':'.join(str(ROOT/q) for q in paths)+':/usr/local/sbin:/usr/local/bin:/usr/bin:/usr/sbin:/bin',HIP_PATH='none',PERL5LIB=str(ROOT/'prebuilts/tools-lineage/common/perl-base'),BISON_PKGDATADIR=str(ROOT/'prebuilts/build-tools/common/bison'),CCACHE_DIR=os.environ.get('CCACHE_DIR',str(ROOT.parent/'ccache')),CCACHE_BASEDIR=str(ROOT))
sysroot=ROOT/'prebuilts/gcc/linux-x86/host/x86_64-linux-glibc2.17-4.8/sysroot'
kt=ROOT/'prebuilts/kernel-build-tools/linux-x86'
cmd=[str(ROOT/'prebuilts/build-tools/linux-x86/bin/make'),'KBUILD_BUILD_USER=Codex','KBUILD_BUILD_HOST=android-builder',f'-j{JOBS}',f'HOSTCFLAGS=--sysroot={sysroot} -I{kt}/include',f'HOSTLDFLAGS=--sysroot={sysroot} -Wl,-rpath,{kt}/lib64 -L {kt}/lib64 -fuse-ld=lld --rtlib=compiler-rt','LLVM=1','LLVM_IAS=1',f'LZ4={kt}/bin/lz4',f'LEX={ROOT}/prebuilts/build-tools/linux-x86/bin/flex',f'YACC={ROOT}/prebuilts/build-tools/linux-x86/bin/bison',f'M4={ROOT}/prebuilts/build-tools/linux-x86/bin/m4',f'PAHOLE={kt}/bin/pahole',f'LIBCLANG_PATH={ROOT}/prebuilts/clang/host/linux-x86/clang-r563880c/lib',f'DTC_EXT={ROOT}/out/host/linux-x86/bin/dtc','TARGET_BOARD_PLATFORM=kona','-C',str(KERNEL),f'O={OUT}','ARCH=arm64','CC=ccache clang','LD=ld.lld']
(BASE/'build-command.json').write_text(json.dumps({'argv':cmd,'environment_overrides':{k:env[k] for k in ['PATH','HIP_PATH','PERL5LIB','BISON_PKGDATADIR','CCACHE_DIR','CCACHE_BASEDIR']}},indent=2)+'\n')
with LOG.open('a',buffering=1) as log:
 def run(argv,phase):
    state.update(phase=phase,updated_utc=now());save(state)
    log.write('\n=== '+now()+' '+phase+' ===\n');log.flush()
    process=subprocess.Popen(argv,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
    while process.poll() is None:
        build_free=shutil.disk_usage(BASE).free;host_free=shutil.disk_usage(ROOT).free
        if build_free<25*1024**3 or host_free<35*1024**3:
            os.killpg(process.pid,signal.SIGTERM);process.wait(timeout=30)
            raise RuntimeError('disk guard stopped '+phase)
        state.update(updated_utc=now(),child_pid=process.pid,build_free_gib=round(build_free/1024**3,2),host_free_gib=round(host_free/1024**3,2));save(state)
        time.sleep(10)
    if process.returncode:raise RuntimeError(phase+' failed with '+str(process.returncode))
 try:
    if not (OUT/'.config').exists():shutil.copy2(BASE/'baseline/.config',OUT/'.config')
    subprocess.run([str(KERNEL/'scripts/config'),'--file',str(OUT/'.config'),'--enable','KSU','--disable','KSU_SUSFS','--disable','KPM','--disable','KSU_DEBUG'],check=True)
    run(cmd+['olddefconfig'],'olddefconfig')
    original=config(BASE/'baseline/.config');current=config(OUT/'.config')
    changed={key:{'before':original.get(key),'after':current.get(key)} for key in sorted(set(original)|set(current)) if original.get(key)!=current.get(key)}
    (BASE/'config-changes.json').write_text(json.dumps(changed,indent=2)+'\n')
    for key in ['CONFIG_CFI','CONFIG_CFI_CLANG','CONFIG_LTO','CONFIG_LTO_CLANG','CONFIG_MODVERSIONS','CONFIG_LOCALVERSION','CONFIG_LOCALVERSION_AUTO']:
        assert current[key]==original[key],(key,current.get(key),original.get(key))
    assert current['CONFIG_KSU']=='y'
    for key in ['CONFIG_KPM','CONFIG_KSU_SUSFS','CONFIG_KSU_DEBUG']:assert current.get(key,'n')=='n',(key,current.get(key))
    unexpected=[key for key in changed if not key.startswith('CONFIG_KSU') and key!='CONFIG_KPM']
    assert not unexpected,('unexpected configuration changes',unexpected)
    run(cmd+['headers_install'],'headers_install')
    assert (OUT/'usr/include/linux/unistd.h').exists()
    run(cmd+['Image','modules'],'kernel_and_modules')
    release=(OUT/'include/config/kernel.release').read_text().strip()
    assert release==(BASE/'baseline/kernel.release').read_text().strip(),release
    assert (OUT/'arch/arm64/boot/Image').stat().st_size>10000000
    state.update(phase='build_succeeded',release=release,finished_utc=now(),exit_code=0);save(state)
 except BaseException as e:
    state.update(phase='build_failed',error=str(e),finished_utc=now(),exit_code=1);save(state)
    raise
