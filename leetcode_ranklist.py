import sys
from leetcode import app
from leetcode.config import local_config

# Run!
if local_config.is_debug:
    app.run(debug = True)
else:
    app.run(host = local_config.flask_host,
            port = local_config.flask_port)
