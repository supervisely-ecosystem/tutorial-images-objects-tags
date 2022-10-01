import os
from dotenv import load_dotenv
import supervisely as sly

# for convenient debug, has no effect in production
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

api = sly.Api()


# get project info from server
project_id = int(os.environ["context.slyProjectId"])
print(project_id)