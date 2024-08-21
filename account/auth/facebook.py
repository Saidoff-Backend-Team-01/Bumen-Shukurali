import facebook


class Facebook:

    @staticmethod
    def validated(auth_token):
        try:
            graph = facebook.GraphAPI(access_token=auth_token)
            profile = graph.request('/me?fields=id,name,first_name,last_name,email,picture.type(large),birthday&access_token={access_token}')
            return profile
        except:
            return "The token is invalid or expired."