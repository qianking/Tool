echo off
CD /D "%~dp0"
pyside6-uic IPLAS_ui.ui > IPLAS_ui.py
