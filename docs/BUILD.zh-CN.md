# 源码与构建

SOURCES.json 记录上游基线和本次补丁；manifests/pinned.xml 固定了 1176 个项目。
公开 manifest 将相对 GitHub 地址改为明确的公共地址，源码提交保持不变。
它不包含本地 Git/.repo 配置、访问凭据或原始机器日志。

## 获取固定源码

在 Linux 文件系统中使用 Android repo 工具：

~~~sh
mkdir infinityx-android
cd infinityx-android
repo init -u https://github.com/InSnocent/infinityx-lmi.git -b main -m manifests/pinned.xml --git-lfs
repo sync -c -j4 --fail-fast --no-clone-bundle
python3 .repo/manifests/scripts/apply-rom-patches.py .
~~~

脚本检查设备树基线和补丁是否已经应用，不会 reset、clean 或覆盖无关改动。
如上游以后不再提供某个固定提交，需要先解决源可获取性，不能悄悄换成最新分支。

## 环境

使用 Linux x86_64 构建环境；WSL2 可用。源码、输出和 ccache 应放在 Linux 文件系统，
配置足够的内存、swap 和 SSD 空间；资源较少时降低并行任务数。

预留数百 GB Linux 文件系统空间。WSL 中不要在 /mnt/c 或 /mnt/e 的 NTFS
目录直接编译 Android；这些位置可用于保存分发文件。
需要 Android 构建常用依赖及 32 位兼容库、Git LFS、ccache、fontconfig 与至少一种系统字体。
repo init 必须启用 --git-lfs，以匹配本次成功环境并取得 LFS 管理的大文件。
Recovery 字体生成需要可用的系统字体；Arch Linux 可使用 ttf-dejavu，
无需为此修改 ROM 源码。编译器和 JDK 使用固定源码中的预编译版本。

## 构建 ROM

~~~sh
export CCACHE_DIR=/path/to/ccache
export CCACHE_MAXSIZE=10G
export GOMAXPROCS=4
source build/envsetup.sh
export BUILD_USERNAME=Codex
lunch infinity_lmi bp4a userdebug
m bacon -j4
~~~

不要在启用 shell errexit/pipefail 的包装器中盲目 source envsetup。
本版本启用 GAPPS，输出位于 out/target/product/lmi。

产物文件名包含新构建的时间；重新构建不保证与已发布 ZIP 位级一致，
即便源码相同，构建时间和文件系统元数据也可能改变。

## 内核对应源码

完整源码归档 kernel-sources-lmi-sukisu-v4.3.0.tar.gz 可与刷机包一同通过网盘分发。
它包含集成后的完整 kernel/ 和 driver/ 源码（无 .git、构建输出或个人日志），
配合本仓库配置和固定 Android 工具链，可复现 SukiSU 内核。
普通 ROM 内核的基线提交以及反向撤销 SukiSU 补丁的方法见 README 的
「可选 Root（SukiSU Ultra）」与 patches/、configs/。

保留上游版权；不要将本社区构建当成官方 Infinity-X 或 LineageOS 发布。
