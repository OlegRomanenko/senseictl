#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import yaml
import pyudev
from sensei import hidrawpure as hidraw
import webcolors
import copy
import enum

SENSEIRAW_HID_ID = '0003:00001038:00001369'

LED_LOGO = 1

class LedStyles(enum.Enum):
    LED_STYLE_STEADY = 1
    LED_STYLE_BREATHE_SLOW = 2
    LED_STYLE_BREATHE_MEDIUM = 3
    LED_STYLE_BREATHE_FAST = 4
    LED_STYLE_ON_CLICK = 5

    @classmethod
    def values(cls):
        return list(map(lambda k: k.value, LedStyles))

#
# Auxiliary functions

def find_device_path(hid_id):
    # find the appropriate /dev/hidrawX device
    ctx = pyudev.Context()
    dev = next((dev for dev in ctx.list_devices(HID_ID=hid_id)
            if dev.sequence_number == 0 and list(dev.children)))

    child = next(dev.children)
    if child.subsystem == 'hidraw':
        return child['DEVNAME']

def open_hiddevice(hid_id):
    dev_path = find_device_path(hid_id)
    try:
        return hidraw.HIDRaw(open(dev_path, 'w+'))
    except PermissionError:
        print("\nYou don't have write access to {0}".format(dev_path))
        print("""
        Run this script with sudo or ensure that your user belongs to the
        same group as the device and you have write access. For instance:
          sudo groupadd sensei
          sudo chown $(ls -l {0} | cut -d ' ' -f 4):rival {0}
          sudo adduser $(whoami) sensei
          sudo chmod g+w {0}
        Perhaps create a udev rule:
          echo 'KERNEL=="hidraw*", GROUP="sensei"' > /etc/10-local-sensei.rules
          udevadm trigger
        """.format(dev_path))
        sys.exit(1)

def open_device():
        return SenseiRaw()

#
# Main classes

class SenseiRaw(object):

    def __init__(self, hid_id = SENSEIRAW_HID_ID):
        # constructor
        # needs a hidraw device
        device = open_hiddevice(hid_id)
        self.__device = device
        self.FACTORY_PROFILE = Profile()
        self.FACTORY_PROFILE.led_style = 2
        self.FACTORY_PROFILE.cpi1 = 800
        self.FACTORY_PROFILE.cpi2 = 1600
        self.FACTORY_PROFILE.polling_rate = 1000
        self.__profile = self.FACTORY_PROFILE

    def send(self, report):
        # send a report packet to the device
        self.__device.sendFeatureReport(report)


    def _set_led_style(self, led, style):
        if led != LED_LOGO:
            raise ValueError("Invalid LED: %s" % (led,))
        if LedStyles(style) in LedStyles:
            return '\x07%s%s' % (chr(led), chr(style))
        raise ValueError(
                "Invalid Style %s, valid values are 1, 2, 3, 4 and 5" % (style,))

    def set_led_style(self, style):
        return self._set_led_style(LED_LOGO, style)

    def set_cpi(self, cpinum, value):
        if cpinum not in (1,2):
            raise ValueError("Invalid CPI Number: %s" % (cpinum,))
        if value % 50:
            raise ValueError("CPI Must be an increment of 50")
        if not (50 <= value <= 6500):
            raise ValueError("CPI Must be between 50 and 6500")
        return '\x03%s%s' % (chr(int(cpinum)), chr(int(value/50)),)

    def set_cpi_1(self, value):
        return self.set_cpi(1, value)

    def set_cpi_2(self, value):
        return self.set_cpi(2, value)

    def set_polling_rate(self, rate):
        if rate == 1000:
            b = '\x01'
        elif rate == 500:
            b = '\x02'
        elif rate == 250:
            b = '\x03'
        elif rate == 125:
            b = '\x04'
        else:
            raise ValueError("Invalid Polling Rate, valid values are 1000,"
                             " 500, 250 and 125")
        return "\x04\x00%s" % (b,)

    def commit(self):
        return '\x09'

#
# Profiles

class Profile(object):

    def __init__(self, led_style=LedStyles.LED_STYLE_STEADY, cpi1=800,
            cpi2=1600, pooling_rate=1000):
        self.led_style = led_style
        self.cpi1 = cpi1
        self.cpi2 = cpi2
        self.polling_rate = pooling_rate

    @classmethod
    def copy_profile(cls, profile):
        return copy.deepcopy(profile)

    @classmethod
    def find_profile(cls, name):
        def find_profile_file(_dir):
            for f in os.listdir(_dir):
                n, x = os.path.splitext(f)
                if x.lower() in ('.yml', '.yaml', ''):
                    if n.lower() == name:
                        return os.path.join(_dir, f)
        profile = None
        if os.path.exists(name):
            return name
        f = find_profile_file(".")
        if f:
            return f
        sensei_dir = os.path.join(os.path.expanduser("~"), ".sensei")
        if os.path.exists(sensei_dir):
            f = find_profile_file(sensei_dir)
        if f:
            return f

    @classmethod
    def from_yaml(cls, stream):
        cfg = yaml.load(stream)
        profile = cls.copy_profile(FACTORY_PROFILE)
        for k, v in cfg.items():
            if hasattr(profile, k):
                setattr(profile, k, v)
        return profile

    def to_report_list(self, current_state=None):
        items = [
            set_led_style(self.logo_style),
            set_cpi_1(self.cpi1),
            set_cpi_2(self.cpi2),
            set_polling_rate(self.polling_rate)
        ]
        if current_state:
            return [i for i in items if i not in current_state]
        return items
