# Dell Inspiron 7000 (7x60) for macOS High Sierra/Sierra

这是我使用的Dell Inspiron 7000(7560)的CLOVER引导文件
## CLOVER
* 支持10.13.4Beta/10.13.3/10.12.6
* CPU原生支持
* 显卡原生支持，`platform-id` 为 `0x59160000`，注入信息通过 `/CLOVER/ACPI/patched/SSDT-Config.aml`加载
* 声卡为ALC256(ALC3246)，使用 `AppleALC` 仿冒，layout-id:56，注入信息位于 `/CLOVER/ACPI/patched/SSDT-Config.aml`
* 无线网卡更换为bcm94352z，驱动信息位于 `FakeSMC` 
* 其它 `ACPI` 补丁修复采用 `hotpatch` 方式，文件位于 `/CLOVER/ACPI/patched`
![screenshot18](http://ous2s14vo.bkt.clouddn.com/screenshot18.png)
* 清理了下Drivers64UEFI目录，只保留需要的驱动程序，apfs.efi为不加载log版本。
![Clover](http://7.daliansky.net/dell/Clover.jpg)


## ALCPlugFix

> 修复耳机切换及插入无声

进入 `ALCPlugFix` 目录，双击 `install双击自动安装.command` 安装

## HIDPI **感谢 @[冰水加劲Q](https://github.com/xzhih)**
进入 `一键开启HIDPI并注入EDID` 目录，点击 `双击.command` 命令执行后以实现下面的效果：
![hidpi](http://ous2s14vo.bkt.clouddn.com/hidpi.png)

## refind
另一个BootLoader
使用方法：将 `refind` 目录复制到 `/EFI` 下即可


## 更新
* 10-4-2017
    * 加入显示器edid和HIDPI

* 10-7-2017
    * 修复bcm94352z在10.12下的WIFI驱动

* 10-8-2017
    * 添加一键开启HIDPI脚本，同时解决内屏黑屏问题，感谢 `冰水加劲Q` 提供的脚本

* 10-17-2017
    * EFI更新，修正显卡驱动
    * 驱动更新：
        * Lilu v1.2.0 
        * AppleALC v1.2.1
        * IntelGraphicsDVMTFixup v1.2.0
        * AirportBrcmFixup v1.1.0
    * 驱动修复：
        * IntelGraphicsFixup v1.2.0 

* 10-21-2017
    * Clover 常规更新 Clover_v2.4k_r4259
    * 驱动更新：
        * FakeSMC v1765
    * 修改BCM94352z驱动方式，将注入信息移动到FakeSMC，移除config.plist中的相关信息

* 11-12-2017
    * Clover 常规更新
        * Clover_v2.4k_r4298
    * ALC256声卡驱动更新
        * 添加全新id:56
        * 去除底噪
    * ALCPlugFix更新,修复耳机插入状态

* 3-13-2018

    * 修改独显屏蔽模式，独显屏蔽更彻底，感谢@宪武
    * Clover常规更新
        * Clover_v2.4k_r4418
        * drivers64UEFI更新
            * 使用AptioMemoryFix.efi彻底解决内存分配不足卡+++问题
            * Apfs.efi常规更新到10.13.4Beta3
    * 驱动更新
        * InterGraphicsFixup v1.2.5
        * AppleALC v1.2.3
        * Lilu v1.2.3
        * Shiki v2.2.3
        * AirportBrcmFixup v1.1.1

    ​

## 如果你认可我的工作，可以通过 `打赏` 支持我后续的更新
|微信|支付宝|
| --- | --- |
|![wechatpay_160](http://ous2s14vo.bkt.clouddn.com/wechatpay_160.jpg)|![alipay_160](http://ous2s14vo.bkt.clouddn.com/alipay_160.jpg)|


## QQ群:
331686786 [一起黑苹果](http://shang.qq.com/wpa/qunwpa?idkey=db511a29e856f37cbb871108ffa77a6e79dde47e491b8f2c8d8fe4d3c310de91)

158976808 [燃7000黑苹果交流群](http://shang.qq.com/wpa/qunwpa?idkey=e2a57e954de694774549b675dda9cd9a6f5cf30db3a53d4d82a34b9013dde5e3)

