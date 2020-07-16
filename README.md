![PyPI - Downloads](https://img.shields.io/pypi/dm/drfaddons)
# Django REST Framework Add Ons

**A collection package for Django REST Framework**<br>

`Django REST Framework Add Ons` is a collection package collected over a period of one year from various sources.<br>
In each function/class I've specified its source in `docstrings` inside `Source` / `Sources`.<br> 
Wherever there isn't any source, the module has been created by me for my personal use.<br>
This may come in handy to all those who are going to use `Django REST Framework` for creating `API`.<br>

Contributors: **WE'RE LOOKING FOR SOMEONE WHO CAN CONTRIBUTE IN DOCS**
- **[Civil Machines Technologies Private Limited](https://github.com/civilmachines)**: For providing me platform and
funds for research work. This project is hosted currently with `CMT` only. 
- **[Himanshu Shankar](https://github.com/iamhssingh)**: Himanshu Shankar has initiated this project and worked on this
project to collect useful functions and classes that are being used in various projects.
- [Mahen Gandhi](https://github.com/imlegend19): For making this repository into a library. At the time of this commit,
he is an intern with `CMT` and is assigned with the task of making this as a `Python Package` hosted on 
[PyPi](https://pypi.org/).
- [Aditya Gupta](https://github.com/ag93999): For updating this repository and projects using this repository as per
the latest standards. He is also an intern with `CMT` and is assigned with same task as `Mahen`. He updated various
projects using this library to use `GenericAPIView`, such as `CreateAPIView`, `ListAPIView` rather than 
`ValidateAndPerformView View`

#### Installation

- Download and Install via `pip`
```
pip install drfaddons
```
or<br>
Download and Install via `easy_install`
```
easy_install drfaddons
```
- Add, if wanted, `drfaddons` in `INSTALLED_APPS` (This is although not required!)
```
INSTALLED_APPS = [
    ...
    'drfaddons',
    ...
]
```
