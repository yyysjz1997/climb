# Library to adjust display brightness through sys files
#
# Author: Kevin Thomas <hamgom95@gmail.com>
# Last Change: March 10, 2017
# URL https://github.com/hamgom95/sys_backlight

"""
Example:
    b = Backlight()
    b.setrel(60) # set brightness to 60%

"""

class Backlight:
    def __init__(self):
        self.minbrightness = 0
        self.maxbrightness = int(open(("/sys/class/backlight/intel_backlight/max_brightness"),'r').read())
        self.diff = (self.maxbrightness - self.minbrightness)
    def set(self,bgvalue):
        if (self.valid(bgvalue)):
            open("/sys/class/backlight/intel_backlight/brightness",'w').write(str(bgvalue))
            self.bgvalue = bgvalue
    def get(self):
        return int(open("/sys/class/backlight/intel_backlight/brightness",'r').read())
    def valid(self,bgvalue):
        if ( self.maxbrightness >= bgvalue >= self.minbrightness):
            return True
        else: False
    def add(self,inc):
        b_new = self.get() + inc
        if (self.valid(b_new)):
            self.set(b_new)
    def sub(self,dec):
        b_new = self.get() + dec
        if (self.valid(b_new)):
            self.set(b_new)
    def getrel(self):
        percentage = (self.get() / self.diff) * 100
        return int(percentage)
    def setrel(self,per):
        if (100 >= per >= 0):
            b_new = int(per / 100 * self.diff)
            self.set(b_new)
    def addrel(self,per):
        b_new = self.getrel() + per
        self.setrel(b_new)
    def subrel(self,per):
        b_new = self.getrel() - per
        self.setrel(b_new)

def example():
    pass

if __name__ == "__main__":
    example()