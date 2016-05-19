SenseiCTL
--

**SenseiCTL** is an unofficial configuration tool for the SteelSeries Sensei Raw Gaming Mouse under linux and is based on [**RivalCTL**](https://github.com/nixi-awoo/rivalctl). This peripheral nor any other product made by SteelSeries, has official Linux support today. The tool is limited in it's functionality, since everything had to be reverse-engineered.


Installation
--

Requirements:

    Required:
    pyudev>=0.16
    webcolors>=1.4
    ioctl-opt>=1.2
    PyYAML==3.11

    Optional (for the experiments):
    psutil==3.4.2
    six==1.10.0

    Write permission to the device is required as well

Manual Installation:

    git clone https://github.com/dneto/senseictl.git
    sudo python setup.py install

 
Usage
--

    usage: senseictl [-h] [--commit] [--reset] [--profile PROFILE]
                     [--led-style STYLE] [--led-intensity INTENSITY] [--cpi1 CPI]
                     [--cpi2 CPI] [--polling-rate RATE]

    A tool to configure the SteelSeries RAW Gaming Mouse
    optional arguments:
      -h, --help            show this help message and exit
      --commit              Save to firmware
      --reset               Reset all options to FACTORY defaults
      --profile PROFILE     profile name or path to file
      --led-style STYLE     LED Style [1=Steady, 2-4=Breathe Speed, 5=On Click]
      --led-intensity INTENSITY
                            LED Intensity [1=Off, 2=Low, 3=Medium, 4=High]
      --cpi1 CPI            50-6500 in increments of 50 [default 800]
      --cpi2 CPI            50-6500 in increments of 50 [default 1600]
      --polling-rate RATE   1000, 500, 250, or 125 [default=1000]
