echo off
CD /D "%~dp0"
pyside6-uic login_ui.ui > login_ui.py
