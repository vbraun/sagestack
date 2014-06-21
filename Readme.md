Sage on Hashdist
================

This is an experimental conversion of the sage packaging system to
hastdist. It does'nt build Sage (yet), only third-party packages.

How to Use
----------

1. Get hashdist: https://github.com/hashdist/hashdist.

2. Make sure that the `hit` command is in the `PATH`.

3. Run `hit init-home` if you haven't before.

3. Go to the `build` subdirectory of this repository.

4. Run `hit build`.

This will build everything up to Python, for now.

5. Start `./default/bin/python` to launch Python
