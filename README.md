# Dell Inspiron 7000 I/II (7x60/7x72) for macOS Mojave/High Sierra

这是我使用的Dell Inspiron 7000(7560)的CLOVER引导文件，它同样也适用于Dell Inspiron 7460/7472/7572等I代II代机型

## 电脑配置

| 规格     | 详细信息                                              |
| -------- | ----------------------------------------------------- |
| 电脑型号 | 戴尔 Inspiron 7560 笔记本电脑                         |
| 操作系统 | macOS Mojave 18E226/macOS High Sierra 10.13.6 17G2208 |
| 处理器   | 英特尔 Core i7-7500U @ 2.70GHz 双核                   |
| 内存     | 16 GB ( 金士顿 DDR4 2400MHz )                         |
| 硬盘     | 建兴 CV1-8B512 (512 GB / 固态硬盘 )                   |
| 显卡     | 英特尔 HD Graphics 620 (platform-id:0x59160000)       |
| 显示器   | 奇美 CMN15E0 FHD 1920x1080 (15.6 英寸)                |
| 声卡     | ALC256 (layout-id:2/56)                               |
| 网卡     | 英特尔7265已更换为Bcm94352z(14E4:43B1)                |

## 安装镜像

直接使用博客中的镜像进行安装：[【黑果小兵】macOS Mojave 10.14(18A389) with Clover 4670原版镜像](https://blog.daliansky.net/macOS-Mojave-10.14-18A389-Release-with-Clover-4670-original-mirror.html)

## CLOVER

* 支持Mojave/High Sierra/Sierra
* CPU原生支持，变频正常
* 睡眠唤醒正常，最新增加睡眠呼吸灯
* 显卡原生支持，采用`Lilu+WhateverGreen`通过`Clover/device/Properties`方式注入，同时支持HDMI显示输出
* 声卡为ALC256(ALC3246)，使用 `AppleALC` 仿冒，layout-id:2或者56，通过`Clover/device/Properties`方式注入，支持HDMI Audio声音输出
* 无线网卡更换为bcm94352z，添加`SSDT-7560-DW1560.aml`以解决可能存在的睡眠唤醒后蓝牙失效的问题
* 显示器亮度调节正常；亮度调节快捷键：`f11/f12`
* USB遮盖采用`INTEL FB-Patcher`生成`USBPower.kext`，它位于`Clover/kexts/Other`
* 添加PCI设备信息
* 其它 `ACPI` 补丁修复采用 `hotpatch` 方式，文件位于 `/CLOVER/ACPI/patched`

## 系统截图

![0About](./screenshot/0About.png)
![0Displays](./screenshot/0Displays.png)
![0Displays1](./screenshot/0Displays1.png)
![0Memory](./screenshot/0Memory.png)
![1Audio](./screenshot/1Audio.png)
![1Audio2](./screenshot/1Audio2.png)
![1AudioPatch](./screenshot/1AudioPatch.png)
![2BlueTooth](./screenshot/2BlueTooth.png)
![2BlueTooth2](./screenshot/2BlueTooth2.png)
![3Wifi](./screenshot/3Wifi.png)
![4Sata](./screenshot/4Sata.png)
![5Ethernet](./screenshot/5Ethernet.png)
![6USB](./screenshot/6USB.png)
![6USBFinal](./screenshot/6USBFinal.png)
![7Light](./screenshot/7Light.png)
![8Volume](./screenshot/8Volume.png)
![9Drivers](./screenshot/9Drivers.png)
![Clover](./screenshot/Clover.png)




## ALCPlugFix

> 修复耳机切换及插入无声

进入 `ALCPlugFix` 目录，双击 `install双击自动安装.command` 安装

## HIDPI **感谢 @[冰水加劲Q](https://github.com/xzhih)**

进入 `一键开启HIDPI并注入EDID` 目录，点击 `双击.command` 命令执行后以实现下面的效果：
![hidpi](http://7.daliansky.net/hidpi.jpg)

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
            * Apfs.efi常规更新到10.13.4Beta5
    * 驱动更新
        * InterGraphicsFixup v1.2.5
        * AppleALC v1.2.3
        * Lilu v1.2.3
        * Shiki v2.2.3
        * AirportBrcmFixup v1.1.1
* 4-9-2018

    * Clover常规更新

        * Clover_v2.4k_r4429 更新支持macOS 10.13.4
        * Apfs.efi常规更新到10.13.5DB1
    * 驱动更新

      * InterGraphicsFixup v1.2.7
      * AppleALC v1.2.6
      * Shiki v2.2.6
      * AirportBrcmFixup v1.1.2
* 7-21-2018
    * 支持`Mojave`/`High Sierra`/`Sierra`
    * CLOVER常规更新
        * Clover v2.4k r4618，支持10.13.6 17G2112
        * 使用`ApfsDriverLoader-64.efi`，不需要再频繁地更新`apfs.efi`了
    * 驱动更新
        * Lilu v1.2.5
        * AppleALC v1.3.0
        * WhateverGreen v1.2.0
* 8-4-2018
    * CLOVER常规更新到v2.4k r4630
        * 使用新的显卡驱动方式，更好地支持10.13/10.14
    * 驱动更新
        - Lilu v1.2.6
        - AppleALC v1.3.1
        - WhateverGreen v1.2.1
* 8-6-2018
    * Clover添加Disable minStolenSize less or equal fStolenMemorySize assertion，解决卡DVMT；另一种方法请移步：[通过修改DVMT Pre-Allocated解决AppleIntelKBLGraphicsFramebuffer问题](http://bbs.pcbeta.com/forum.php?mod=viewthread&tid=1730172&page=1#pid46869870)
    * SMBIOS设置为MacBookPro15,2，它只支持10.13.6（17G2112/17G2208)以及10.14Beta版本，旧的系统请使用配置文件`config_MBP141.plist`
* 8-8-2018

    * 增加Brcm94352z/DW1560注入信息，解决10.13.6(17G2112/17G2208)/10.14蓝牙失效问题
* 8-11-2018

    * 加入了I2C触摸板的支持，开启更多手势
* 9-22-2018
    * 使用`FB Patcher`生成USBPower.kext，弃用`USBInjectAll.kext`和`SSDT-UIAC-ALL.aml`
    * `VoodooI2C`更新到v2.0.1特别版，触摸板支持更多手势，支持双指捏合缩放，支持`Mojave`和`HighSierra`
    * 声卡id注入:2，以解决部分机型无法驱动的问题
    * 驱动常规更新
        * Lilu v1.2.7
        * WhatEverGreen v1.2.3
        * AppleALC v1.3.2
    * 修改主题文件，适配`Mojave`
* 9-24-2018
    * `config.plist`修正
        * 删除`kextstopatch`里面关于`minStolen`的补丁
        * 删除USB端口限制补丁
    * 添加`USBPower.kext`驱动，删除`SSDT-UIAC-ALL.aml`
    * 修正`SSDT-PCIList.aml`显示信息
    * 修正自带主题`Hackintosh_ID`适配`Mojave`图标
* 9-29-2018
    * 增加睡眠呼吸灯
    * 添加`DW1560`信息的注入，有效改善睡眠唤醒后蓝牙失效
* 4-6-2019

    * 更新支持到Mojave 10.14.4
    * 常规驱动更新
* 5-2-2019
    * 更新`CLOVER`到v4924
    * 修正`PCIList`信息
    * 添加开机声音
    * 修改电池驱动为`SMCBatteryManager.kext`
* 5-19-2019
    * 更新`CLOVER`到v4928
    * 添加`ComboJack`，解决耳麦输入
    * 修改`ALCPlugfix`，支持睡眠唤醒后`内置麦克风`和`耳麦`完美切换
* 6-4-2019
    * 更新 CLOVER 到 v4940
    * 添加 macOS Catalina 支持
    * 常规驱动更新




## 如果你认可我的工作，可以通过 `打赏` 支持我后续的更新
|微信|支付宝|
| --- | --- |
|![wechatpay_160](http://7.daliansky.net/wechatpay_160.jpg)|![alipay_160](http://7.daliansky.net/alipay_160.jpg)|


## QQ群:
331686786 [一起黑苹果](http://shang.qq.com/wpa/qunwpa?idkey=db511a29e856f37cbb871108ffa77a6e79dde47e491b8f2c8d8fe4d3c310de91)

158976808 [燃7000黑苹果交流群](http://shang.qq.com/wpa/qunwpa?idkey=e2a57e954de694774549b675dda9cd9a6f5cf30db3a53d4d82a34b9013dde5e3)

