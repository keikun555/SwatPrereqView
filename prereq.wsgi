import sys
activate_this = os.path.join('/srv/services/prereq/SwatPrereqView/bin/activate_this.py')
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))
sys.path.insert(0, '/srv/services/prereq')
from prereqvis import app as application
sys.stdout = sys.stderr
