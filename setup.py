from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os", "sys", "PyQt5", "metaphor_python"],
    "excludes": [],
    "include_files": ["API_key.txt", "NexaFetch_icon.ico"]
}

setup(
    name="NexaFetch",
    version="0.1",
    description="NexaFetch Content Aggregator",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base="Win32GUI", icon="NexaFetch_icon.ico")]
)
