echo the bat's path : %~dp0
cd %~dp0

start py -3  %~dp0/python_pkg/start_ui.py
