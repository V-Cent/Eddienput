from ctypes import *

_vcontroller = WinDLL('vcontroller.dll')

buttons = {
'Dpad'                  : 0x0001,
'BtnStart'              : 0x0010,
'BtnBack'               : 0x0020,
'BtnThumbL'             : 0x0040,
'BtnThumbR'             : 0x0080,
'BtnShoulderL'          : 0x0100,
'BtnShoulderR'          : 0x0200,
'Home'                  : 0x0400,
'BtnA'                  : 0x1000,
'BtnB'                  : 0x2000,
'BtnX'                  : 0x4000,
'BtnY'                  : 0x8000
}


class State:
    buttons_value = 0x0000
    LT_value = 0x00
    RT_value = 0x00

    LX_value = 0x0000
    LY_value = 0x0000
    RX_value = 0x0000
    RY_value = 0x0000

    def update_state(self, button, value):
        if button == 'TriggerL':
            self.LT_value = value * 0xff
        elif button == 'TriggerR':
            self.RT_value = value * 0xff
        else:
            base = buttons[button]
            if base == 0x0001:  # Dpad case
                mask = 0xfff0
            else:
                mask = 0xffff ^ base
            rest = self.buttons_value & mask
            self.buttons_value = rest + base * value

    def update_thumb(self, LX, LY, RX, RY):
        #values between -32768 and 32767
        self.LX_value = int(LX * 0x7fff)
        self.LY_value = int(LY * 0x7fff)
        self.RX_value = int(RX * 0x7fff)
        self.RY_value = int(RY * 0x7fff)

    def reset(self):
        self.buttons_value = 0x0000
        self.LT_value = 0x00
        self.RT_value = 0x00

        self.LX_value = 0x0000
        self.LY_value = 0x0000
        self.RX_value = 0x0000
        self.RY_value = 0x0000


def connect(use_dinput=False):
    if use_dinput:
        print('Using DirectInput emulation')
    else:
        print('Using XInput emulation')
    return _vcontroller.connect(use_dinput)


def set_state(state):
    return _vcontroller.set_state(state.buttons_value, state.LT_value, state.RT_value, state.LX_value, state.LY_value, state.RX_value, state.RY_value)

def disconnect():
    return _vcontroller.disconnect()
