class Saved:
    def __init__(self, user_id, recipe_id):
        self.__user_id = user_id
        self.__recipe_id = recipe_id

    # Accessor methods
    def get_user_id(self):
        return self.__user_id

    @property
    def get_recipe_id(self):
        return self.__recipe_id

    # Mutator methods
    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_recipe_id(self, recipe_id):
        self.__recipe_id = recipe_id
