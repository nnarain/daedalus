# Daedalus

[![Latest Release](https://img.shields.io/github/v/release/nnarain/daedalus)](https://github.com/nnarain/daedalus/releases/latest)
[![CI](https://img.shields.io/github/actions/workflow/status/nnarain/daedalus/release.yml)](https://github.com/nnarain/daedalus/actions/workflows/release.yml)
[![Documentation](https://img.shields.io/badge/docs-mdBook-blue)](https://nnarain.github.io/daedalus/)

![Image not found](docs/daedalus-3d.png)

Daedalus is a Raspberry Pi add-on that aim's to supply the necessary components for common robotics applications such as power distribution, IO, sensors and software defined embedded logic.

The current revision (Rev A) is a Proof-of-concept and contains the following:

- A switch mode power supply taking an input of 7V - 25V (2S to 6S LiPo battery) and and output of 5V @ 6A continuous
- A 3.3V linear regulator
- On board RP2040 co-processor
- MPU-6050 IMU
- 16 GPIO (8x Pi + 8x MCU)
