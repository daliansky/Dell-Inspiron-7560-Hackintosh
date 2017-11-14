#!/bin/sh

function _init(){

    VendorID=$(ioreg -l | grep "DisplayVendorID" | awk '{print $8}')
    ProductID=$(ioreg -l | grep "DisplayProductID" | awk '{print $8}')
    EDID=$(ioreg -l | grep "IODisplayEDID" | awk '{print $8}' | sed -e 's/.$//' -e 's/^.//')

    Vid=$(echo "obase=16;$VendorID" | bc | tr 'A-Z' 'a-z')
    Pid=$(echo "obase=16;$ProductID" | bc | tr 'A-Z' 'a-z')

    edID=$(echo $EDID | sed 's/../b5/21')

    EDid=$(echo $edID | xxd -r -p | base64)
    thisDir=$(dirname $0)
    thatDir="/System/Library/Displays/Contents/Resources/Overrides"
}

function enable_hidpi(){

    mkdir -p $thisDir/tmp/DisplayVendorID-$Vid
    cp $thisDir/Icons.plist $thisDir/tmp/
    dpiFile=$thisDir/tmp/DisplayVendorID-$Vid/DisplayProductID-$Pid
    sudo chmod -R 777 $thisDir

cat > "$dpiFile" <<-\HIDPI
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>DisplayProductID</key>
    <integer>PID</integer>
    <key>DisplayVendorID</key>
    <integer>VID</integer>
    <key>DisplayProductName</key>
    <string>Color LCD</string>
    <key>IODisplayEDID</key>
    <data>
        EDid
    </data>
    <key>scale-resolutions</key>
    <array>
        <data>
        AAAMgAAABwgA
        </data>
        <data>
        AAALQAAABlQA
        </data>
    </array>
    <key>target-default-ppmm</key>
    <real>10.0699301</real>
</dict>
</plist>
HIDPI

    sed -i '' "s/VID/$VendorID/g" $dpiFile
    sed -i '' "s/PID/$ProductID/g" $dpiFile
    sed -i '' "s:EDid:${EDid}:g" $dpiFile
    sed -i '' "s/VID/$Vid/g" $thisDir/tmp/Icons.plist
    sed -i '' "s/PID/$Pid/g" $thisDir/tmp/Icons.plist

    sudo cp -r $thisDir/tmp/* $thatDir/
    rm -rf $thisDir/tmp
    echo "开启成功，重启生效"

}

start(){
    _init

cat << EOF
----------------------------------------
|*************** HIDPI ****************|
----------------------------------------
(1) 开启HIDPI
(2) 关闭HIDPI

EOF
read -p "输入你的选择[1~2]: " input
case $input in
    1) enable_hidpi
;;
2) sudo rm -rf $thatDir/DisplayVendorID-$Vid && echo "已关闭，重启生效"
;;
*) break
;;
esac 
}

start