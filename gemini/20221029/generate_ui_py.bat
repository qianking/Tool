echo off
CD /D "%~dp0"
pyside6-uic ui.ui > ui.py
