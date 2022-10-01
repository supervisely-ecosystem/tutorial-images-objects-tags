import supervisely as sly

def create_project(api: sly.Api, workspace_id, project_name, recreate_if_exists=True):
    project = api.project.get_info_by_name(workspace_id, project_name)
    if project is not None:
        api.project.remove(project.id)
    
    # create on server project with name 'animals' with one dataset with name 'cats'
    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    dataset = api.dataset.create(project.id, "dataset01", change_name_if_conflict=True)
    print(f"New project {project.id} with one dataset {dataset.id} on server are created")

    # lets init one annotation class (rectangle), color is green for visual convenience
    cat_class = sly.ObjClass("cat", sly.Rectangle, color=[0, 255, 0])
    # lets init one annotation tag, value can be any string 
    scene_tag = sly.TagMeta("scene", sly.TagValueType.ANY_STRING)

    # init project meta - define classes and tags we are going to label
    project_meta = sly.ProjectMeta(obj_classes=[cat_class], tag_metas=[scene_tag])

    # set classes and tags in our new empty project on server
    api.project.update_meta(project.id, project_meta.to_json())

    # upload local image to dataset
    image_info = api.image.upload_path(dataset.id, name="my-cats.jpg", path="images/my-cats.jpg")

    # init labels (bboxs) for cats and one tag will be assigned to image
    cat1 = sly.Label(sly.Rectangle(top=875, left=127, bottom=1410, right=581), cat_class)
    cat2 = sly.Label(sly.Rectangle(top=549, left=266, bottom=1500, right=1199), cat_class) 
    tag = sly.Tag(scene_tag, value="indoor")

    # init annotaiton and then upload it to server
    ann = sly.Annotation(img_size=[1600, 1200], labels=[cat1, cat2], img_tags=[tag]) # img_size=[height, width]
    api.annotation.upload_ann(image_info.id, ann) 
    
    return project.id   