# 可选 SukiSU Ultra

只适用于本仓库 2026-10-29 的 Infinity-X 3.12 lmi ROM。
Root boot 保留原 ramdisk、DTB 和启动参数，只替换内核并重新生成 AVB 哈希尾部。
它不适用于其他 ROM 或后续版本，即使内核版本字符串相同。

## 安装和撤销

从网盘取得配套文件后，先验证 SHA256SUMS.txt，确认手机已能正常运行本版 ROM，再进入 Fastboot：

~~~sh
fastboot flash boot boot-lmi-infinityx-sukisu-v4.3.0.img
fastboot reboot
~~~

安装官方普通版 SukiSU v4.3.0 管理器，按应用需要授权。
管理器从 [官方 Release](https://github.com/SukiSU-Ultra/SukiSU-Ultra/releases/tag/v4.3.0)
获取，不随本仓库重新打包。
不要同时刷入另一套 Magisk Root。

撤销本次可选 Root：

~~~sh
fastboot flash boot boot.img
fastboot reboot
~~~

这里的 boot.img 必须来自同一个 ROM 版本。无需格式化或改写 Recovery/固件。

## 配置与验证范围

- CONFIG_KSU=y，基础 builtin 手工 Hook。
- KPM、SUSFS、KSU 调试模式关闭；ADB Root 功能编译在内，但不代表默认授权。
- CFI、LTO、MODVERSIONS 保留，SELinux 本机观测为 Enforcing。
- 内核 release 字符串保持基线值，以匹配现有模块的 vermagic；
  同时比较实际导出符号 CRC，不能只靠修改字符串判断兼容。
- 基础 Root 实机可用；尚未验证所有第三方模块和 Zygisk/Xposed 组合。

## 重建内核

先按 BUILD.zh-CN.md 获得固定 Android 源码和工具链，并完成普通 ROM 构建。
在 Linux 文件系统中准备本发布仓库副本，从网盘取得同一版本的源码归档和 boot.img。

~~~sh
tar -xzf kernel-sources-lmi-sukisu-v4.3.0.tar.gz -C reproduction/sukisu
mkdir -p reproduction/sukisu/baseline
cp boot.img reproduction/sukisu/baseline/boot.img
export ANDROID_ROOT=/path/to/infinityx-android
python3 reproduction/sukisu/build-kernel.py
python3 reproduction/sukisu/verify-abi.py
python3 reproduction/sukisu/repack-boot.py
~~~

工具生成新的内核与 boot，不自动刷机。
源码归档不包含编译器；工具链由固定 Android manifest 获取。
修改源码或配置后，必须重新验证 ABI 和硬件功能。

## 原始基线与源码补丁

- 普通内核基线：LineageOS 71b13e62f057a649b77fe4062feb73ee72ad609c。
- 手工 Hook 补丁：patches/kernel/0001-basic-sukisu.patch。
- 驱动基线：SukiSU builtin 85d3b0483df224f1dcf6f2880b3181d3f2ca4e0f。
- 完整兼容修正：patches/sukisu/0001-lmi-compat-and-offline-metadata.patch。
- 基础/Root 完整配置位于 configs/。

若从公开上游重建，先在各自基线提交应用对应补丁，
再将 kernel/drivers/kernelsu 链接到相邻 driver/kernel。
归档已包含该链接和 .scmversion。
从归档恢复普通内核时，在 kernel 目录反向应用内核 Hook 补丁、
使用 kernel-baseline.config；driver/ 不参与普通内核构建。
