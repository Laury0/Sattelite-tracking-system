from Core.Space_Objects import Satellite, GroundStation

class SpaceObjectFactory:
    @staticmethod
    def create_object(obj_type, *args):
        if obj_type == "satellite":
            return Satellite(*args)
        elif obj_type == "ground":
            return GroundStation(*args)
        else:
            raise ValueError("Unknown object type")
