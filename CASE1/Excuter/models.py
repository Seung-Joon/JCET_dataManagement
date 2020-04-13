class Lot:
    def __init__(self, id, upload_flag):
        self.id = id
        self.upload_flag = upload_flag
        self.result = ""

class Lot_List:
    def __init__(self, lot_list):
        list_object = {}
        for lot in lot_list:
            list_object[lot.id] = lot.upload_flag
    
    def get_lot(self, id):
        return self.list_object[id]

    def get_all(self):
        return self.list_object

    def add_lot(self, object):
        list_object[object["id"]] = object

    def pop_lot(self, object):
        list_obejcet[object.id].pop()

    def set_flag(slef, object):
        object.result = True

    def undo_flag(self, object):
        object.result = False

    