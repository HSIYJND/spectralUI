# spectralUI <img src="./src/main/icons/icon.png" width="48" height="48">

spectralUI is an open-source general purpose cross platform tool for analysing hyperspectral images.

## Website
[spectralUI.github.io](https://spectralui.github.io)

## Screenshot

![spectralUI ver 0.1 Screenshot](https://i.ibb.co/F3F9r6b/outp.png)

## Supported Operating Systems

1. Windows 7, 8, 8.1, 10
2. Linux
3. Mac OS 10.5+

## Installation

Download the requirements file
```bash
virtualenv <env_name>
source <env_name>/bin/activate
pip install -r path/to/requirements.txt
```
Replace <env_name> with the name of the environment that you want to create

Run the app using:
```bash
python main.py
```

## Current Features

* Load .mat files
* Display spectral images in each band
* Print metadata
* Plot spectral signature by clicking on a pixel
* Matplotlib navigation toolbar included

## Fututre Plans

* Dark theme support
* Exception handling
* Improve performance
* Display hyperspectral datacube
* Generate sRGB from the input
* Adoption of MVC Architecture
* Include state-of-the-arts Super-Resolution, Segmentation and Classification algorithms for hyperspectral images
* Add support for users to try out their own algorithms
* Auto updater
* CLI support
* Add documentation

## Plans For Much Later

* Re-wirte code in rust, when a stable gui framework is available for rust.
* Support for multiple algorithms.
* Support for Deep learning + GPU acceleration
