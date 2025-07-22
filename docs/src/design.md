# Design

Daedalus is designed as a comprehensive Raspberry Pi add-on board for robotics applications.

## Power Supply

The board features a switch mode power supply that can accept input voltages from 7V to 25V (suitable for 2S to 6S LiPo batteries) and provides a stable 5V output at up to 6A continuous current.

Additionally, a 3.3V linear regulator provides power for low-power components and ensures clean power for sensitive analog circuits.

## Microcontroller

An onboard RP2040 co-processor provides additional GPIO and processing capabilities, complementing the Raspberry Pi's capabilities.

## Sensors

The board includes an MPU-6050 IMU (Inertial Measurement Unit) providing:
- 3-axis gyroscope
- 3-axis accelerometer  
- Temperature sensor

## GPIO

The board provides 16 GPIO pins total:
- 8 GPIO pins connected to the Raspberry Pi
- 8 GPIO pins connected to the RP2040 MCU

This allows for flexible interfacing with external sensors, actuators, and other peripherals commonly used in robotics applications.