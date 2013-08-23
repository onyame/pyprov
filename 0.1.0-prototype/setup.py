# See the file "LICENSE.txt" for the full license governing this code.


"""
Setup script.
"""


from distutils.command import clean as _clean
from distutils import core
import os
import subprocess
import shutil
import sys

from distribute_setup import use_setuptools
use_setuptools()
import setuptools


class clean(_clean.clean):
    """ Little clean extension: Cleans up a non-empty build directory. """
    
    def run(self):
        for path in ["build", "doc/html", "doc/doctrees", "dist", ".coverage"]:
            if os.path.isdir(path):
                shutil.rmtree(path)
            elif os.path.isfile(path):
                os.remove(path)


class _BaseCommandRunner(core.Command):
    """ Base class for encapsulating command line commands. """
    
    def run(self):
        self._create_build_dir()
        command = self._create_command()
        self._run_command(command)
        self._perform_post_actions()
    
    @staticmethod
    def _create_build_dir():
        if not os.path.exists("build"):
            os.mkdir("build")

    def _create_command(self):
        pass
    
    def _run_command(self, command):
        if self.verbose:
            print(command)
        subprocess.call(command, shell=True)
    
    def _perform_post_actions(self):
        pass


class pylint(_BaseCommandRunner):
    """ Runs the pylint command. """

    _PACKAGE_NAME = "pyprov"

    description = "Runs the pylint command."
    user_options = [
        ("command=", None, "Path and name of the command line tool."),
        ("out=", None, "Specifies the output type (html, parseable). Default: html")]

    def initialize_options(self):
        self.command = "pylint"
        if sys.platform == "win32":
            self.command += ".bat"
        self.out = "html"
        self.output_file_path = "build/pylint.html"

    def finalize_options(self):
        self.verbose = self.distribution.verbose
        if self.out == "parseable":
            self.output_file_path = "build/pylint.txt"

    def _create_command(self):
        return (
            "{0} --rcfile=dev/pylintrc --output-format={1} src/{2} test/{2}_test > {3}".
            format(self.command, self.out, self._PACKAGE_NAME, self.output_file_path))
        
    def _perform_post_actions(self):
        if self.out == "parseable":
            new_content = list()
            with open(self.output_file_path, "rb") as file_object:
                for line in file_object.readlines():
                    line = line.replace("\\", "/")
                    new_content.append(line)
            with open(self.output_file_path, "wb") as file_object:
                file_object.writelines(new_content)


class test(_BaseCommandRunner):
    """ Runs all unit tests. """
    
    description = "Runs all unit tests using py.test."
    user_options = [
        ("command=", None, "Path and name of the command line tool."),
        ("out=", None, "Specifies the output format of the test results." \
         + "Formats: xml, standard out. Default: standard out."),
        ("covout=", None, "Specifies the output format of the coverage report." \
         + "Formats: xml, html.")]

    def initialize_options(self):
        self.command = "py.test"
        if sys.platform == "win32":
            self.command += ".exe"
        self.out = None
        self.covout = None

    def finalize_options(self):
        self.verbose = self.distribution.verbose
        
    def _create_command(self):
        options = " test"
        if self.out == "xml":
            options = "--junitxml=build/xunit.xml test"
        if not self.covout is None:
            options = (
                "--cov=src --cov-report={0} --cov-config=dev/coveragerc {1}".format(self.covout, options))
        return "{0} {1}".format(self.command, options)
    
def _perform_setup():
    _set_pythonpath()
    _run_setup()


def _set_pythonpath():
    python_path = [os.path.realpath(path) for path in ["src", "test"]]
    python_path = os.pathsep.join(python_path) + os.pathsep + os.environ.get("PYTHONPATH", "")
    os.environ["PYTHONPATH"] = python_path


def _run_setup():
    version = "0.2.0"
    
    setuptools.setup(
        name="PyProv", 
        version=version,
        cmdclass={"clean": clean, "test": test, "pylint": pylint},
        author="Deutsches Zentrum fuer Luft- und Raumfahrt e.V. (DLR)",
        author_email="Clemens.Teichmann@dlr.de",
        maintainer="Deutsches Zentrum fuer Luft- und Raumfahrt e.V. (DLR)",
        maintainer_email="clemens.teichmann@dlr.de",
        url="https://svn.sistec.dlr.de/viewvc/clemens-teichmann/PyProv/?root=students",
        license="New BSD",
        platforms=["Linux", "Unix", "Windows"],
        packages=setuptools.find_packages("src"),
        include_package_data=True,
        package_dir={"" : "src"},
        entry_points={
            "console_scripts": ["pyprov = pyprov.main:cmd_main"]},
        command_options={
            "build_sphinx": {
               "version": ("setup.py", version),
               "release": ("setup.py", version)}},
    )


if __name__ == "__main__":
    _perform_setup()