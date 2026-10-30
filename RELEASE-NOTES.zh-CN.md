# Infinity-X 3.12 / Android 16 / lmi — UNOFFICIAL

首个公开版本，构建日期 2026-10-29，实测设备为国行 Redmi K30 Pro。

- 默认 ROM 不含 Root；可选 SukiSU Ultra boot 单独提供，KPM/SUSFS 关闭。
- 源码固定清单、适配补丁、完整内核/驱动源码归档和复现说明随版本提供。
- ROM 及相关镜像通过外部网盘分发，GitHub 仅提供源码、补丁与技术文档。
- 下载完整原始 ROM 后校验 SHA-256；如使用分卷，可运行 scripts/assemble-rom.py 合并。
  完整 ROM 的 SHA-256 必须为
  9cf66b7fa39e1f5afd2b22dfdb13739bbba6140c9456ab659e1df2434933843e。
- recovery.img 是配套 AOSP/Lineage 衍生 Recovery。
- 刷机前阅读 README 的「如何使用」；首次从其他 ROM 迁移涉及清除用户数据。
- root boot 只适用于本版 ROM；回退只需刷回同版 boot.img，不格式化。
- MIUI 固件、手机个人备份和校准/NV 数据不在 GitHub 仓库中。
- 实测范围和指示灯/前摄相关现象见 docs/STATUS.zh-CN.md。
- 隐私处理范围和扫描限制见 PRIVACY-AUDIT.json。

来源与致谢：Project Infinity-X、LineageOS、TheMuppets、SukiSU-Ultra、
KernelSU、AOSP 和 Linux 贡献者。
