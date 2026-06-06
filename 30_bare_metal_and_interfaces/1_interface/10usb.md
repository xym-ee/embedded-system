---
sort: 10
---
# usb

使用 USB 实现一个 XBOX 手柄。


https://www.partsnotincluded.com/understanding-the-xbox-360-wired-controllers-usb-data/


## The Device Descriptor

```c
/* USB Standard Device Descriptor */
__ALIGN_BEGIN uint8_t USBD_FS_DeviceDesc[USB_LEN_DEV_DESC] __ALIGN_END =
  {
    18,                         /*bLength */
    1,                          /*bDescriptorType*/
    0x00,                       /* bcdUSB */  
    0x02,
    DEVICE_CLASS,             /*bDeviceClass*/
    DEVICE_SUBCLASS,          /*bDeviceSubClass*/
    DEVICE_PROTOCOL,          /*bDeviceProtocol*/
    USB_MAX_EP0_SIZE,         /*bMaxPacketSize*/			// --> EP0_SIZE dando problema
    LOBYTE(VENDOR_ID),        /*idVendor*/
    HIBYTE(VENDOR_ID),        /*idVendor*/
    LOBYTE(PRODUCT_ID),       /*idVendor*/
    HIBYTE(PRODUCT_ID),       /*idVendor*/
    LOBYTE(DEVICE_VERSION),   /*bcdDevice rel. 2.00*/
    HIBYTE(DEVICE_VERSION),
    1,           							/*Index of manufacturer  string*/
    2,								       	/*Index of product string*/
    3,        								/*Index of serial number string*/
    1  												/*bNumConfigurations*/
  } ; 
/* USB_DeviceDescriptor */
```

```
bLength: 18
bDescriptorType: 0x01 (DEVICE)
bcdUSB: 0x0200
bDeviceClass: 0xFF (Vendor Specific)
bDeviceSubClass: 0xFF
bDeviceProtocol: 0xFF
bMaxPacketSize0: 8
idVendor: 0x045E (Microsoft Corp.)
idProduct: 0x028E (Xbox360 Controller)
bcdDevice: 0x0114
iManufacturer: 1
iProduct: 2
iSerialNumber: 3
bNumConfigurations: 1
```

二进制数组为 0x12 0x01 0x00 0x02 0xff 0xff 0xff 0x08 0x5e 0x04 0x8e 0x02 0x14 0x01 0x01 0x02 0x03 0x01


## Configuration Descriptor

```
bLength: 9
bDescriptorType: 0x02 (CONFIGURATION)
wTotalLength: 153
bNumInterfaces: 4
bConfigurationValue: 1
iConfiguration: 0
bmAttributes: 0b10100000 (NOT SELF-POWERED, REMOTE-WAKEUP)
bMaxPower: 250 (500 mA)
```

0x09 0x02 0x99 0x00 0x04 0x01 0x00 0xa0 0xfa





## 控制数据

总共 20 Bytes

- byte0 : 0x00 消息类型，固定不变
- byte1 : 0x14 数据长度，20 bytes
- byte2 : 按键，1 按下，0 释放
  - bit0 : D-UP
  - bit1 : D-DOWN
  - bti2 : D-LEFT
  - bit3 : D-RIGHT
  - bit4 : START
  - bit5 : BACK
  - bit6 : L3
  - bit7 : R3
- byte3 : 按键，1 按下，0 释放
  - bit0 : LB
  - bit1 : RB
  - bit2 : XBOX-LOGO
  - bit3 : unused, 0
  - bit4 : A
  - bit5 : B
  - bit6 : X
  - bit7 : Y
- byte4 : LT, 8bit unsigned integer, 255 is fully depressed
- byte5 : RT, 8bit unsigned integer, 255 is fully depressed
- byte6 : LX, low byte of 16-bit signed integet
- byte7 : LX, high byte of 16-bit signed integet
- byte8 : LY, low byte of 16-bit signed integet
- byte9 : LY, high byte of 16-bit signed integet
- byte10 : RX, low byte of 16-bit signed integet
- byte11 : RX, high byte of 16-bit signed integet
- byte12 : RY, low byte of 16-bit signed integet
- byte13 : RY, high byte of 16-bit signed integet
- byte14-19 : unused, 0x00



	


	












