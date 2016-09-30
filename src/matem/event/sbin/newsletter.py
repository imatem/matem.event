"""
    Instance script for testing a researcher creation

    Execution::

        bin/instance run src/x.y/x/y/testscript.py
"""


def main(app):
    folder = app.unrestrictedTraverse("x/y/z/cancer")

    # Create a researcher
    print "http://localhost/people/9947603276956765"

    # This script does not commit

# If this script lives in your source tree, then we need to use this trick so that
# five.grok, which scans all modules, does not try to execute the script while
# modules are being loaded on the start-up
if "app" in locals():
    main(app)
