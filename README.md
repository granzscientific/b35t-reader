Owon/Lilliput provies a mobile app to read data from their B35T device but they
have released no other information.

This script extends the information found at
https://hackaday.io/project/12922-bluetooth-data-owon-b35t-multimeter and prints
out every data update sent by the meter.

This Python script is based partially on a Ruby script available at
https://github.com/cransom/b35t-reader


# How to use

## Setup
Get the MAC address of the meter by running `sudo hcitool lescan` before turning
on the meter and holding the bluetooth button. You should get line with `<MAC
ADDRESS> BDM`. Set this address at the top of the script.

There's no pairing required.

## Usage

Turn on the meter, enable bluetooth, and run the script.

The meter will not sleep while BT is enabled.

If the connection with the meter is lost, the script will try to automatically
reconnect.

If it never reconnects, use Ctrl-C to kill the script and try restarting it. I
have noticed sometimes the meter seems to stop broadcasting and it must be powered
off and back on again.

