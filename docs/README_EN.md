# Project Infinity-X 3.12 / Android 16 — lmi

[简体中文](../README.md) | English

Unofficial community build of Project Infinity-X for Redmi K30 Pro (codename lmi),
with reproduction materials and an optional SukiSU Ultra boot. Provided for reference.

---
### Screenshots

| | | |
|--|--|--|
|![Home screen](images/1.png)|![Settings menu](images/2W.png)|![Quick Settings tiles](images/3W.png)|
|![About](images/5.png)|![Settings menu](images/2B.png)|![Quick Settings tiles](images/3B.png)|

---
## Documentation

The technical documents below are currently Chinese-only.

- [Source and build](BUILD.zh-CN.md)
- [Test scope and known issues](STATUS.zh-CN.md)
- [Release notes](../RELEASE-NOTES.zh-CN.md)
- [Privacy scan scope and limits](../PRIVACY-AUDIT.json)
- ROM downloads:
  - [SourceForge](https://sourceforge.net/projects/lmi-infinityx-a16-unofficial/)
  - [MEGA](https://mega.nz/file/MpRRAbQZ#m8YWwipUbB9SgZYBAJYTBfFywAgBH5bQXrIK2YnE_FE)
  - Quark Drive (not yet available)

After downloading the full ROM, verify its SHA-256 checksum first, then sideload with ADB.
Merge split archives first if needed.
The signature and bytes of the original ROM are left unchanged.

~~~sh
# Windows
certutil -hashfile Project_Infinity-X-3.12-lmi-29.10.2026-GAPPS-UNOFFICIAL.zip SHA256
# Linux / macOS
sha256sum Project_Infinity-X-3.12-lmi-29.10.2026-GAPPS-UNOFFICIAL.zip
~~~

The full ROM SHA-256 must be
`9cf66b7fa39e1f5afd2b22dfdb13739bbba6140c9456ab659e1df2434933843e`;
hashes for the other files are listed in [SHA256SUMS.txt](../SHA256SUMS.txt).

If only `.partNN` parts are available, download all parts plus release-manifest.json
and merge them (Python 3):

~~~sh
python ../scripts/assemble-rom.py --directory /path/to/downloads
~~~

Do not use split archives or the source archive directly with ADB sideload.

| Item | Value |
|---|---|
| ROM | Infinity-X 3.12 / Android 16 / GAPPS / UNOFFICIAL |
| Build date | 2026-10-29 |
| Test device | China-region Redmi K30 Pro, lmi |
| Kernel | 4.19.325-cip131-st15-perf-g71b13e62f057 |
| Build type | userdebug |
| Optional root | SukiSU Ultra built-in, driver version 41100 |
| KPM / SUSFS | Disabled |
| SELinux | Observed as Enforcing on the test device |

The flashable package does not include SukiSU by default. The optional root boot
applies only to this ROM release, not to other ROMs or later builds.

Device trees, kernel and vendor foundations come from LineageOS and TheMuppets;
the ROM comes from Project Infinity-X, and root comes from SukiSU-Ultra / KernelSU.
Pinned sources, patches and licenses are listed in SOURCES.json, NOTICE and LICENSES.

## How to Use

### Preparation
- The device must be lmi (Redmi K30 Pro). Redmi K30, K30 Ultra and other models are
  not applicable; the POCO F2 Pro shares the lmi codename but was not independently tested here.
- Unlocked Bootloader.
- Firmware base: China-region MIUI V14.0.5.0.SJKCNXM.
- Full ROM and matching recovery.img downloaded from the cloud drive.
- For root, the optional SukiSU Ultra build from Releases.
- Google's official Platform-Tools (or the traditional fastboot and adb).
- Back up personal data, chats and photos yourself before flashing.
- Sufficient battery level and a stable USB connection.

### First-time Installation from Another ROM

The steps below wipe user data on the phone. Back up first.

1. In Fastboot mode, confirm the device codename is lmi.
2. Flash the matching recovery.img from the same distribution:

~~~sh
fastboot getvar product
fastboot flash recovery recovery.img
fastboot reboot recovery
~~~

If the last command is unsupported, enter Recovery with the hardware keys.
The bundled Recovery is an AOSP/Lineage-derived recovery built from this ROM.
Compatibility of older third-party recoveries with Android 16 decryption and
installation has not been verified.

3. In Recovery choose ``Factory reset`` → ``Format data/factory reset``,
   and wait for ``Data wipe complete``.
4. Choose ``Apply update`` → ``Apply from ADB``, then run:

~~~sh
adb sideload Project_Infinity-X-3.12-lmi-29.10.2026-GAPPS-UNOFFICIAL.zip
~~~

5. Confirm that Recovery reports success, then reboot.
   ADB progress stalling around 47% before finishing successfully can be normal;
   judge by the result on the phone.

The ROM installer writes boot, dtbo, vbmeta, vbmeta_system and the dynamic partitions;
no extra manual flashing of these images is needed. Do not apply flashing commands
meant for other devices. Do not re-lock the Bootloader.

### Optional Root (SukiSU Ultra)

Confirm that the system boots normally first; switching the boot image does not wipe data.

~~~sh
fastboot flash boot boot-lmi-infinityx-sukisu-v4.3.0.img
fastboot reboot
~~~

Get the manager from the
[official release](https://github.com/SukiSU-Ultra/SukiSU-Ultra/releases/tag/v4.3.0);
this repository does not redistribute it. Do not flash another Magisk root at the same time.
KPM, SUSFS and KSU debug mode are disabled, and SELinux was observed as Enforcing on
the test device; third-party modules and Zygisk/Xposed combinations are untested.
For rebuilding the kernel and driver, and for ABI verification, see
[Source and build](BUILD.zh-CN.md), patches/ and configs/.

### Known Issues
- The notification LED went completely dark once and later returned to solid while charging;
  the cause was not identified, and notification breathing/blinking behavior has not been
  specifically confirmed.
- NFC, Bluetooth pairing, GPS, VoLTE/VoWiFi, standby drain and long-term stability are not
  fully tested.
- POCO F2 Pro and other regional variants have not been independently tested.
- Play Integrity, payment/banking, DRM and game environment checks are not guaranteed.
- This repository runs no OTA service of its own; later versions must be installed manually
  following their own instructions.

## Disclaimer

- This is an individual-maintained, AI-assisted community UNOFFICIAL build.
  It is not affiliated with, authorized by, or endorsed by Xiaomi / Redmi, Google,
  Project Infinity-X, LineageOS, TheMuppets, SukiSU-Ultra / KernelSU;
  all names and trademarks belong to their respective owners.
- Flashing is high risk: it may brick the device, lose data, damage hardware, void the
  warranty, and may break Play Integrity, banking/payment, DRM or game environment checks.
- Proceed only after understanding these risks. You alone bear any data loss, hardware
  damage, account restriction, warranty invalidation or other direct/indirect loss caused
  by downloading, flashing, using or being unable to use this build. This project and its
  contributors provide no warranty of usability, security, integrity or fitness for a
  particular purpose, and accept no liability. Exact terms: LICENSE, Sections 7 and 8.
- Not recommended for work devices, enterprise fleets, or anything that relies on
  payment/identity verification.
- Comply with the laws and license terms that apply to the device, the software and your
  region. These limitations apply to the extent permitted by law; where local law does not
  allow the exclusion of implied warranties, statutory requirements prevail.
- Absent a critical bug that prevents normal use, this project is likely to be the final build.

## License Agreement

| Content | License |
|---|---|
| Documentation and helper scripts (scripts/, reproduction/) | Apache-2.0, see LICENSE |
| Linux kernel, SukiSU / KernelSU driver and their patches | GPL-2.0, see LICENSES/GPL-2.0.txt; corresponding source is provided with each release |
| Upstream device trees, vendor and ROM platform patches | Retain their upstream licenses and SPDX copyright headers |
| Prebuilt ROM, recovery, boot and vendor closed-source components | Not relicensed by this repository |

- When copying, modifying or redistributing content from this repository, retain NOTICE
  and upstream attributions, mark your changes, and include a copy of the Apache-2.0
  license; GPL-2.0 parts must ship their corresponding source under their terms.
- AOSP components in the ROM, Google apps (GAPPS) and vendor closed-source binaries remain
  subject to their own licenses and terms; this repository grants no additional rights.
  Downloads will be removed if a rights holder requests it.
- Do not imply that this build is an official upstream release or is endorsed upstream.
- See SOURCES.json, NOTICE and manifests/pinned.xml for sources, pinned commits and patches.

## Acknowledgements

This build is based on the work of these upstream projects:

- [Project Infinity-X](https://github.com/ProjectInfinity-X): ROM platform and build system
- [LineageOS](https://github.com/LineageOS): lmi / sm8250 device trees, Xiaomi hardware support and kernel
- [TheMuppets](https://github.com/TheMuppets): vendor repositories required for the build
- [SukiSU-Ultra](https://github.com/SukiSU-Ultra/SukiSU-Ultra) and [KernelSU](https://github.com/tiann/KernelSU): optional root implementation
- [AOSP](https://source.android.com) and [Linux](https://www.kernel.org) contributors: Android and kernel foundations

Thanks also to all upstream contributors and device maintainers. All names and trademarks belong to their respective owners.

---

*English translation of the Chinese README. If the two differ, the Chinese version prevails.*
