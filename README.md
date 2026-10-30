# Project Infinity-X 3.12 / Android 16 — lmi

Redmi K30 Pro（代号 lmi）的社区 UNOFFICIAL 构建、复现资料与可选 SukiSU Ultra boot。

Unofficial Android 16 build for Redmi K30 Pro (lmi), with pinned sources,
reproducible adaptation patches, installation notes and an optional SukiSU boot.
The POCO F2 Pro shares the lmi codename but has not been independently tested here.

## 下载与使用

- [刷机与回退](docs/INSTALL.zh-CN.md)
- [源码和构建](docs/BUILD.zh-CN.md)
- [可选 SukiSU 与内核复现](docs/SUKISU.zh-CN.md)
- [测试范围与已知问题](docs/STATUS.zh-CN.md)
- [隐私处理范围](docs/PRIVACY.zh-CN.md)
- 刷机包下载：外部网盘，链接由维护者稍后补充。

下载完整 ROM 后先校验 SHA-256，再执行 ADB sideload。若使用分卷，须先合并。
原 ROM 的签名和字节内容保持不变。

| 项目 | 值 |
|---|---|
| ROM | Infinity-X 3.12 / Android 16 / GAPPS / UNOFFICIAL |
| 构建日期 | 2026-10-29 |
| 测试设备 | 国行 Redmi K30 Pro，lmi |
| 内核 | 4.19.325-cip131-st15-perf-g71b13e62f057 |
| 构建类型 | userdebug |
| 可选 Root | SukiSU Ultra builtin，驱动版本 41100 |
| KPM / SUSFS | 关闭 |
| SELinux | 本机观测为 Enforcing |

刷机包默认不含 SukiSU。可选 root boot 只适用于这一版 ROM，不适用于其他 ROM 或后续版本。

主要设备树、内核和 vendor 基础来自 LineageOS、TheMuppets；
ROM 来自 Project Infinity-X，Root 来自 SukiSU-Ultra / KernelSU。
固定来源、补丁和许可证见 SOURCES.json、NOTICE、LICENSES。

本仓库不是上述上游项目的官方维护渠道。
