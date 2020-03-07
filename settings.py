import os
from dotenv import load_dotenv

env_path = '.env'
load_dotenv(dotenv_path=env_path)

# OR, the same with increased verbosity
load_dotenv(verbose=True)
TRACKER_TYPE = os.environ["TRACKER_TYPE"]
