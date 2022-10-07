echo off
CD /D "%~dp0"
pyside6-uic ttest.ui > ttest.py
