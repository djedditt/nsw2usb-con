#!/usr/bin/env python3

# SPDX-License-Identifier: BSD-1-Clause
# Copyright (c) 2025 djedditt

import sys, time
import usb.core, usb.util

VID_NINTENDO   = 0x057E
PID_SW2_PROCON = 0x2069
PID_SW2_NGCCON = 0x2073
INTERFACE      = 1

# thanks to Mitch from HHL for the setup report
INIT_REPORT    = bytes([0x03, 0x91, 0x00, 0x0D, 0x00, 0x08, 0x00, 0x00,
                        0x01, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])

# set player led command
PLED_REPORT    = bytes([0x09, 0x91, 0x00, 0x07, 0x00, 0x08, 0x00, 0x00,
                        0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

def main():
    # find the controller
    dev = next((d for d in usb.core.find(find_all=True)
                if d.idVendor == VID_NINTENDO
                and d.idProduct in (PID_SW2_PROCON, PID_SW2_NGCCON)), None)
    if not dev:
        sys.exit("error: controller not found")

    # detach if bound
    try:
        if dev.is_kernel_driver_active(INTERFACE):
            dev.detach_kernel_driver(INTERFACE)
    except usb.core.USBError as e:
        sys.exit(f"error: could not detach kernel driver: {e}")

    try:
        dev.set_configuration()
    except usb.core.USBError as e:
        sys.exit(f"error: could not set configuration: {e}")

    try:
        usb.util.claim_interface(dev, INTERFACE)
    except usb.core.USBError as e:
        sys.exit(f"error: could not claim interface {INTERFACE}: {e}")

    # locate bulk-out endpoint
    intf   = dev.get_active_configuration()[(INTERFACE, 0)]
    ep_out = next((e for e in intf.endpoints()
                 if usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
                 and e.bmAttributes == usb.util.ENDPOINT_TYPE_BULK), None)
    if not ep_out:
        sys.exit("error: bulk-out endpoint not found")

    ep_out.write(INIT_REPORT)
    print("init report sent..")
    time.sleep(0.05)
    ep_out.write(PLED_REPORT)
    print("player 1 led set..")
    print("press ctrl-c to exit")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        usb.util.release_interface(dev, INTERFACE)
        try:
            dev.attach_kernel_driver(INTERFACE)
        except usb.core.USBError:
            sys.exit("error: could not reattach kernel driver")

if __name__ == "__main__":
    main()
