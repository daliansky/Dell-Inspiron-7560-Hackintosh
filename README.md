# Dell Inspiron 7000 (7x60) for macOS High Sierra/Sierra

这是我使用的Dell Inspiron 7000(7560)的CLOVER引导文件
## CLOVER
* 支持10.13/10.12.6
* CPU原生支持
* 显卡原生支持，`platform-id` 为 `0x59160000`，注入信息通过 `/CLOVER/ACPI/patched/SSDT-Config.aml`加载
* 声卡为ALC256(ALC3246)，使用 `AppleALC` 仿冒，layout-id:13，注入信息位于 `/CLOVER/ACPI/patched/SSDT-Config.aml`
* 无线网卡更换为bcm94352z，驱动已通过 `config.plist` 加载
* 其它 `ACPI` 补丁修复采用 `hotpatch` 方式，文件位于 `/CLOVER/ACPI/patched`

## ALCPlugFix
> 修复耳机切换及插入无声

进入 `ALCPlugFix` 目录，双击 `install双击自动安装.command` 安装

## HIDPI
将相关文件复制到 `/System/Library/Displays/Contents/Resources/Overrides/` 以实现下面的效果：
![hidpi](http://ous2s14vo.bkt.clouddn.com/hidpi.png)

> 备注：此文件未必适用于你的显示器，请根据自己的显示器提取EDID进行HIDPI制作

## 更新日期：10-4-2017

## QQ群:
331686786 [一起黑苹果](http://shang.qq.com/wpa/qunwpa?idkey=db511a29e856f37cbb871108ffa77a6e79dde47e491b8f2c8d8fe4d3c310de91)

