setup(
    name="DoubleClicker",
    version="1.0.0",
    description="This double clicker allows you to customise nearly every aspect of it just to make it bypass.",
    long_description="README.MD",
    long_description_content_type="text/markdown",
    url="https://github.com/dogesupremacy/DoubleClicker",
    author="dogesupremacy",
    author_email="darragh@dowsetts.org",
    license="GNU General Public License (GPL)",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=[
        "pywin32", "PyQt5"
    ],
    include_package_data=True,
    install_requires=[
        "pywin32", "PyQt5"
    ],
    entry_points={"console_scripts": ["WasdInfo=src.__main__:main"]},
)