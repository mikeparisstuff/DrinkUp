class UserStatsMiddleware(object):
    '''
    This will update an authenticated user's last_active timestamp
    with each network call.
    '''

    def process_request(self,request):
        '''
        This should return None upon successful execution, so that Django will
        continue processing the request normally.
        '''
        user = request.user

        if not user.is_authenticated():
            # User is not authenticated, thus there is no profile to update
            return None

        if user.is_staff or user.is_superuser:
            # No need to update staff or superuser
            return None

        my_profile = user.profile_set.get()

        #update the user's last active timestamp
        my_profile.update_last_active()

        #Save changes
        my_profile.save()

        return None
