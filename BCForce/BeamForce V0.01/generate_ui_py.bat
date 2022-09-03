echo off
CD /D "%~dp0"
pyside6-uic BC_ui.ui > BC_ui.py
