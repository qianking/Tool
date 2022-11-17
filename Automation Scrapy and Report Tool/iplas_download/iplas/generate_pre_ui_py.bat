echo off
CD /D "%~dp0"
pyside6-uic Pre_proccess_UI.ui > Pre_proccess_UI.py
