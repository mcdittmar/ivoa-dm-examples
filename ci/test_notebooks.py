import glob
import os
import subprocess
import tempfile
import sys

import nbformat


def _notebook_run(filename):
    """Execute a notebook via nbconvert and collect output.
       :returns (parsed nb object, execution errors)
    """
    with tempfile.NamedTemporaryFile(suffix=".ipynb") as fout:
        args = ["jupyter", "nbconvert", "--to", "notebook", "--execute",
                "--ExecutePreprocessor.timeout=60", "--allow-errors",
                "--output", fout.name, filename]

        subprocess.check_call(args)

        fout.seek(0)
        nb = nbformat.read(fout, nbformat.current_nbformat)

    errors = [output for cell in nb.cells if "outputs" in cell
              for output in cell["outputs"]
              if output.output_type == "error"]

    return nb, errors


def test_ipynb():
    os.chdir("notebooks")
    notebooks = glob.glob(os.path.join('*.ipynb'))
    ok = True
    for notebook in notebooks:
        _, errors = _notebook_run(notebook)
        ok = ok and not errors
        if errors:
            print(f"Errors in notebook: {notebook}")

    status = 0 if ok else 1
    sys.exit(status)


if __name__ == '__main__':
    test_ipynb()