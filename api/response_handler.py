from models import User

class ResponseHandler():
    
    @staticmethod
    def single_tuple_to_class_dict(tple):
        return {tple[0]:User(*tple[1:]).__dict__}
    
    @staticmethod
    def list_tuple_to_class_dict(tpleList):
        response_dict = {}
        for i in tpleList:
            key = i[0]
            val = User(*i[1:]).__dict__
            response_dict.update({key:val})
        print("response dict is: ", response_dict)
        return response_dict
    
        