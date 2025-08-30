

# Environement Setup:

1. PySpark is not compatible with the current Python 3.13.  To work around this issue, I downgraded to 3.10 using the following work-around:

    - Installed Python 3.10.11 from the pyton site at https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe

2. Created a python virtual environment `venv` for the project folder

        py -3.10 -m venv .venv

        .venv\Scripts\Activate

    - To deactive the `venv` enter in the terminal:

            deactivate

2. Installed `pyspark` and during the install, I was provided a notice to also update `pip`.

        pip install pyspark

        python.exe -m pip install --upgrade pip






