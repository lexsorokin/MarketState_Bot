
class UserSearchConfig:
    all_users = dict()

    def __init__(self, user_id):
        self.step = None
        self.final_data = None
        self.search_method = None
        self.data_for_watchlist = None
        UserSearchConfig.add_user(user_id, self)

    @staticmethod
    def get_user(user_id):
        if UserSearchConfig.all_users.get(user_id) is None:
            new_user = UserSearchConfig(user_id)
            return new_user
        return UserSearchConfig.all_users.get(user_id)

    @classmethod
    def add_user(cls, user_id, user):
        cls.all_users[user_id] = user
