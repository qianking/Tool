echo off
CD /D "%~dp0"
pyside6-uic lfsdata_ui.ui > lfsdata_ui.py
