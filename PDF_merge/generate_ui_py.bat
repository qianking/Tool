echo off
CD /D "%~dp0"
pyside6-uic pdf_ui.ui > pdf_ui.py
