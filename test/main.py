# This is an example Python script.
# In this example script we will use Lemons (Annotated) project from Ecosystem
# The project consists 2 classes: "lemon" and "kiwi", and 0 tags

#  IMG --- media/no_tags.png ---

import supervisely as sly

# 1. Create Tag Meta
# In order to create Tag itself you must create TagMeta object with parameters such as:
# name (required)
# value_type (required)
# color
# applicable_to images/objects/both
# applicable_classes

# Let's start with creating a simple TagMeta for Lemon
# This TagMeta object can be applied to both images and objects, and also to any class
lemon_tag_meta = sly.TagMeta(name="lemon", value_type=sly.TagValueType.NONE)
print(lemon_tag_meta)
# Name:  lemon
# Value type:none
# Possible values:None
# Hotkey
# Applicable toall
# Applicable classes[]

# Let's change applicable classes of this TagMeta to class "lemon" only and make it applicable only to objects
# We can recreate TagMeta or clone already existing TagMeta with additional parameters
# Most supervisely classes are immutable, so you have to assign or reassign them to variables
lemon_tag_meta = lemon_tag_meta.clone(
    applicable_to=sly.TagApplicableTo.OBJECTS_ONLY, applicable_classes=["lemon"]
)
print(lemon_tag_meta)
# Name:  lemon
# Value type:none
# Possible values:None
# Hotkey
# Applicable toobjectsOnly
# Applicable classes['lemon']

# Now let's create a TagMeta for "kiwi" with "oneof_string" value type
possible_kiwi_values = ["fresh", "ripe", "old", "rotten"]
kiwi_tag_meta = sly.TagMeta(
    name="kiwi",
    applicable_to=sly.TagApplicableTo.OBJECTS_ONLY,
    value_type=sly.TagValueType.ONEOF_STRING,
    possible_values=possible_kiwi_values,
)
print(kiwi_tag_meta)
# Name:  kiwi
# Value type:oneof_string
# Possible values:['fresh', 'ripe', 'old', 'rotten']
# Hotkey
# Applicable toall
# Applicable classes[]


# Now we create a tag meta with "any_number" value type for counting fruits on image
fruits_count_tag_meta = sly.TagMeta(
    "fruits count",
    value_type=sly.TagValueType.ANY_NUMBER,
    applicable_to=sly.TagApplicableTo.IMAGES_ONLY,
)
print(fruits_count_tag_meta)
# Name:  fruits count
# Value type:any_number
# Possible values:None
# Hotkey
# Applicable toimagesOnly
# Applicable classes[]


# Bring all created tag metas together in TagMetaCollection or list
tag_metas = [lemon_tag_meta, kiwi_tag_meta, fruits_count_tag_meta]

# 2. Add TagMetas to our Lemons (Annotated) project
# Create an API object to connect to Supervisely instance
from dotenv import load_dotenv
load_dotenv("secret_tokens.env")
api: sly.Api = sly.Api.from_env()

# Get and create project meta from server
project_id = 13401
project_meta_json = api.project.get_meta(id=project_id)
project_meta = sly.ProjectMeta.from_json(data=project_meta_json)

# Check that our created tag metas for lemon and kiwi don't exist already in project meta
# And if not, add them to project meta
for tag_meta in tag_metas:
    if tag_meta not in project_meta.tag_metas:
        project_meta = project_meta.add_tag_meta(new_tag_meta=tag_meta)

# After adding tag metas to project meta
# Update project meta on Supervisely instance
api.project.update_meta(id=project_id, meta=project_meta)

#  IMG --- media/updated_tags.png ---

# 3. Create Tags from Tag Metas
# Get existing image tags by image id
image_id = 3313896
image_info = api.image.get_info_by_id(id=image_id)
image_tags = image_info.tags
print(image_tags)
# []

# 4. Add tags to image and objects via download/upload annotation
ann_json = api.annotation.download_json(image_id=image_id)
ann = sly.Annotation.from_json(data=ann_json, project_meta=project_meta)

# Assign tag to image
fruits_count_tag = sly.Tag(meta=fruits_count_tag_meta, value=7)
ann = ann.add_tag(fruits_count_tag)

# Cycle through objects in annotation and add appropriate tag
new_labels = []
for label in ann.labels:
    new_label = None
    if label.obj_class.name == "lemon":
        lemon_tag = sly.Tag(meta=lemon_tag_meta)
        new_label = label.add_tag(lemon_tag)
    elif label.obj_class.name == "kiwi":
        kiwi_tag = sly.Tag(meta=kiwi_tag_meta, value="fresh")
        new_label = label.add_tag(kiwi_tag)
    if new_label:
        new_labels.append(new_label)

# Upload updated ann to Supervisely instance
ann = ann.clone(labels=new_labels)
api.annotation.upload_ann(img_id=image_id, ann=ann)


# 5. Adding Tags directly to image/objects without uploading annotation
# Get project meta again after updating it with new tags
project_meta_json = api.project.get_meta(id=project_id)
project_meta = sly.ProjectMeta.from_json(data=project_meta_json)
# Get image tag ID from project meta
fruits_count_tag_id = project_meta.get_tag_meta(fruits_count_tag_meta.name).sly_id
# Add Tag to image using Tag sly ID from project meta
api.image.add_tag(image_id=image_id, tag_id=fruits_count_tag_id, value=7)

# Add Tags to objects
# Download annotation
ann_json = api.annotation.download_json(image_id=image_id)
ann = sly.Annotation.from_json(data=ann_json, project_meta=project_meta)
# Cycle through objects in annotation and add appropriate tag
for label in ann.labels:
    # Get figure sly id
    figure_id = label.geometry.sly_id
    if label.obj_class.name == "lemon":
        # Get tag sly id
        tag_meta_id = project_meta.get_tag_meta(lemon_tag_meta.name).sly_id
        api.advanced.add_tag_to_object(tag_meta_id=tag_meta_id, figure_id=figure_id)
    elif label.obj_class.name == "kiwi":
        tag_meta_id = project_meta.get_tag_meta(kiwi_tag_meta.name).sly_id
        api.advanced.add_tag_to_object(tag_meta_id=tag_meta_id, figure_id=figure_id, value="fresh")

#  IMG --- media/result.png ---
