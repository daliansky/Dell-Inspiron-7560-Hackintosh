# Dell Inspiron 7000 (7x60) for macOS High Sierra/Sierra

这是我使用的Dell Inspiron 7000(7560)的CLOVER引导文件
## CLOVER
* 支持10.13/10.12.6
* CPU原生支持
* 显卡原生支持，`platform-id` 为 `0x59160000`，注入信息通过 `/CLOVER/ACPI/patched/SSDT-Config.aml`加载
* 声卡为ALC256(ALC3246)，使用 `AppleALC` 仿冒，layout-id:13，注入信息位于 `/CLOVER/ACPI/patched/SSDT-Config.aml`
* 无线网卡更换为bcm94352z，驱动已通过 `config.plist` 加载
* 其它 `ACPI` 补丁修复采用 `hotpatch` 方式，文件位于 `/CLOVER/ACPI/patched`
![screenshot18](http://ous2s14vo.bkt.clouddn.com/screenshot18.png)
* 清理了下Drivers64UEFI目录，只保留需要的驱动程序，apfs.efi为不加载log版本。
![Drivers64UEFI](http://ous2s14vo.bkt.clouddn.com/Drivers64UEFI.png)


## ALCPlugFix
> 修复耳机切换及插入无声

进入 `ALCPlugFix` 目录，双击 `install双击自动安装.command` 安装

## HIDPI **感谢 @冰水加劲Q**
进入 `一键开启HIDPI并注入EDID` 目录，点击 `双击.command` 命令执行后以实现下面的效果：
![hidpi](http://ous2s14vo.bkt.clouddn.com/hidpi.png)

## refind
另一个BootLoader
使用方法：将 `refind` 目录复制到 `/EFI` 下即可


## 更新
* 10-8-2017
    * 添加一键开启HIDPI脚本，同时解决内屏黑屏问题，感谢 `冰水加劲Q` 提供的脚本
* 10-7-2017
    * 修复bcm94352z在10.12下的WIFI驱动

## QQ群:
331686786 [一起黑苹果](http://shang.qq.com/wpa/qunwpa?idkey=db511a29e856f37cbb871108ffa77a6e79dde47e491b8f2c8d8fe4d3c310de91)

