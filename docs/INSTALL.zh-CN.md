# 安装、合并分卷与回退

只适用于设备代号 lmi；Redmi K30、K30 Ultra 等其他机型不适用。
本文对应 2026-10-29 的 Infinity-X 3.12 GAPPS 构建。
唯一实测设备为国行 Redmi K30 Pro，其他地区变体未独立验证。

## 准备

- Bootloader 已解锁。刷机前另行备份个人数据、聊天和照片。
- 电量充足，USB 连接稳定；使用 Google 官方 Platform-Tools。
  本次成功安装使用 37.0.1；旧版 30.0.5 在本次环境中 sideload 失败。
- 本机测试时使用国行 MIUI V14.0.5.0.SJKCNXM 固件。
  Release 不包含单独的 MIUI 固件包；其他地区应核对其对应底包要求。
  这不表示所有地区都应该刷入国行固件。
- 从网盘下载完整 ROM、SHA256SUMS.txt 和配套 recovery.img。
- 不要把别人的 NV、persist 或校准备份刷到自己的手机。

## 下载与可选分卷合并

GitHub 仓库不托管刷机包附件，网盘地址由维护者补充。
若网盘提供的是完整 ZIP，直接校验下方完整 SHA-256；无需分卷合并。
仅在下载的是 .partNN 分卷时，取得所有分卷和 release-manifest.json，
再使用本仓库脚本（Python 3）校验与合并：

~~~sh
python scripts/assemble-rom.py --directory /path/to/downloads
~~~

结果文件应为：
Project_Infinity-X-3.12-lmi-29.10.2026-GAPPS-UNOFFICIAL.zip

完整 SHA-256：
9cf66b7fa39e1f5afd2b22dfdb13739bbba6140c9456ab659e1df2434933843e

不要把分卷或源码归档直接用于 ADB sideload。

## 从其他 ROM 首次安装

以下会清除手机用户数据。请先完成备份。

1. 在 Fastboot 模式核对机型代号为 lmi。
2. 使用同一版本分发文件 配套 recovery.img：

~~~sh
fastboot getvar product
fastboot flash recovery recovery.img
fastboot reboot recovery
~~~

若设备不支持后一条重启命令，使用按键进入 Recovery。
配套 Recovery 是此 ROM 编译出的 AOSP/Lineage 衍生 Recovery。
本项目没有验证旧第三方 Recovery 对 Android 16 的解密与安装兼容性。

3. 在 Recovery 选择 Factory reset → Format data/factory reset，
   确认 Data wipe complete。
4. 选择 Apply update → Apply from ADB，然后运行：

~~~sh
adb sideload Project_Infinity-X-3.12-lmi-29.10.2026-GAPPS-UNOFFICIAL.zip
~~~

5. 确认 Recovery 报告安装成功，再重启系统。
   ADB 进度停在约 47% 后成功结束可能是正常表现，以手机端结果为准。

ROM 安装器已写入 boot、dtbo、vbmeta、vbmeta_system 和动态分区内容，
不需要额外手动刷写这些镜像；不要自行套用其他机型的刷机命令。
不要重新锁定 Bootloader。

## 可选 Root

先确认系统能正常启动，再按 SUKISU.zh-CN.md 安装可选 boot。
单独切换本版本 boot 不需要格式化数据。

## 回退

只撤销可选 SukiSU：在 Fastboot 刷回同一版本 的 boot.img。
这不会把 Android 16 回退为旧 ROM。

回到旧 ROM 属于另一套迁移流程，通常涉及重新安装和格式化；
须使用自己的备份及对应 ROM 文档。任何用户的 NV/persist 备份都不随本项目分发。
