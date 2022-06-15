# freqpuzzle
bladeRF freqpuzzle

This Dockerfile/script reproduces the mismatch between frequency as reported by get_frequency(), immediately after set_frequency(). If there is a mismatch, it has been observed to always be -2Hz from the requested frequency.

## procedure

```
$ docker build -f Dockerfile . -t freqpuzzle
$ docker run --privileged -ti freqpuzzle
```

If the mismatch occurs, the script will report (for example) ```wanted 155971680.0 got 155971678.0 (-2.0)```

## environment

* ubuntu 22.04 LTS
* gnuradio 3.10.1

```
bladeRF> version

  bladeRF-cli version:        1.8.0-git-29455d29
  libbladeRF version:         2.4.1-0.2021.10-2

  Firmware version:           2.4.0-git-a3d5c55f
  FPGA version:               0.14.0 (configured from SPI flash)
```
