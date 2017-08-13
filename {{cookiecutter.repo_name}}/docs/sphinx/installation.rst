.. _{{cookiecutter.package_name}}-installation:

Installation
============

**Painless Installation**::

    pip install {{cookiecutter.package_name}}

**or to upgrade an existing {{cookiecutter.package_title}} installation**::

    pip install --upgrade {{cookiecutter.package_name}}

.. admonition:: Hint
    :class: hint

    By default, ``pip`` will update any underlying package on which {{cookiecutter.package_name}} depends. If you want to prevent that you can upgrade {{cookiecutter.package_name}} with ``pip install -U --no-deps {{cookiecutter.package_name}}``. This could, however, make {{cookiecutter.package_name}} to not work correctly. Instead, you can try ``pip install -U --upgrade-strategy only-if-needed {{cookiecutter.package_name}}``, which will upgrade a dependency only if needed.

**Developer Installation**::

    git clone https://github.com/{{cookiecutter.github_username}}/{{cookiecutter.repo_name}} {{cookiecutter.repo_name}}
    cd {{cookiecutter.repo_name}}
    pip install -r requirements.txt
    python setup.py install


|

