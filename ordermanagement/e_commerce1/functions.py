
import uuid
from e_commerce1.views import * 

def gen_object_id(model_instance):
    """
    Generate object id
    """
   
    obj_id = uuid.uuid4()
    count = model_instance.objects.filter(object_id=obj_id).count()
    if count:
        gen_object_id(model_instance)
    else:
        return obj_id