import os
from dotenv import load_dotenv
import supervisely as sly
from src.demo_project import create_project

# for convenient debug, has no effect in production
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

api = sly.Api()

team_id = int(os.environ["context.teamId"])
workspace_id = int(os.environ["context.workspaceId"])

# create demo project, code is copied from tutorial:
# https://developer.supervise.ly/getting-started/intro-to-python-sdk
project_id = create_project(api, workspace_id, "animals-tutorial", recreate_if_exists=True)

# get project info from server
project_info = api.project.get_info_by_id(project_id)
print(f"Working project: [id={project_info.id}] {project_info.name}")

# Project meta consists of:
# 1. collection of object classes - that can be used in spatial labeling (polygons, rectangles, masks, and so on)
# 2. collection of tag metas - information abot tags that can be assigned to images / objects

# get project meta from server
project_meta_json = api.project.get_meta(project_id)
project_meta = sly.ProjectMeta.from_json(project_meta_json)
print(project_meta)

# you can learn how to create object classes in the tutorials:
# https://developer.supervise.ly/getting-started/intro-to-python-sdk
# https://developer.supervise.ly/getting-started/spatial-labels

# in this tutorial we will focus on how to work with tags

# Let's create tag meta that can be assigned to images and objects of any classes (without any restrictions)
# tag_meta1 = sly.TagMeta(name="Tag1", value)