class Explainer():
    def __init__(self, class_name = 'default Class', assignment = 'default assignment'):
        self._class_name = class_name
        self._assignment = assignment

    #setters
    def set_class_name(self, name):
        self._class_name = name

    def set_assignment(self, assign):
        self._assignment = assign

    #getters
    def get_class_name(self):
        return self._class_name
    
    def get_assignment(self):
        return self._assignment
    
    #methods
    def get_feedback(self, some_info = "None", default = "something went wrong"):
        #make call to llm

        #else
        return default