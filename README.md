# nsw2usb-con

A minimal Python CLI tool to enable Switch 2-Pro-Controller and NSO GameCube controller input streaming via USB. Do note, this is just a temporary workaround until proper drivers become available.

## Prerequisites

* Python 3.7 or higher
* `pyusb` library
* `libusb`

Install dependencies with:

```zsh
% pip install pyusb
```

macOS users might have to install libusb (via brew is recommended, see [https://brew.sh](https://brew.sh))

```zsh
% brew install libusb
```

## Usage

Run the script to enable input streaming and set the player led:

```zsh
% python nsw2usb-con.py
```

or make the script executable,

```zsh
% chmod +x nsw2usb-con.py
% ./nsw2usb-con
```

You should see the following, exit with ctrl-c when you want to stop using the controller:

```zsh
init report sent..
player 1 led set..
press ctrl-c to exit
```

## License

This project is released under the BSD 1-Clause License. See [LICENSE](LICENSE) for details.
