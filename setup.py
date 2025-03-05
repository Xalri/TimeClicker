from cx_Freeze import setup, Executable

# List all necessary modules explicitly
build_exe_options = {
    "packages": ["pygame", "numpy", "psutil"],
    "includes": ["OpenGL.GL", "numpy.core._methods", "numpy.lib.format"],
    "excludes": ["pytest", "tkinter", "unittest"],
    "include_files": ["src/icon.ico"],  # Ensure necessary assets are included
}

setup(
    name="Time Clicker",
    version="1.0",
    description="Your Time Clicker App",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base="Win32GUI", icon="src/icon.ico")]
)
