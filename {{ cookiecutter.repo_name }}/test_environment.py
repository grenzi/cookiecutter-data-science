import sys

REQUIRED_PYTHON = "{{ cookiecutter.python_interpreter }}"


def main():
    system_major = str(sys.version_info.major)
    required_major = str(REQUIRED_PYTHON[0])

    if system_major != required_major:
        raise TypeError(
            "This project requires Python {}. Found: Python {}".format(
                required_major, sys.version))
    else:
        print(">>> Development environment passes all tests!")


if __name__ == '__main__':
    main()
