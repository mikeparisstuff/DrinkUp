import base64
import uuid
import hashlib
import hmac

class Security(object):
    '''
    A class to handle the encryption of requests to be used for API authentication.
    Uses the sha1 algorithm to produce an HMAC object and returns its hexdigest.
    '''

    def hash_request(self, request):
        '''
        Hash the given request according to the rules that we define.

        TODO:
        Extract access_token from request.
        Find User with that access token as their username.
        Create the string to sign and then hash it and return teh value.
        '''
        # TODO: Make more robust. see http://docs.aws.amazon.com/AmazonS3/latest/dev/RESTAuthentication.html
        pass

def create_new_private_key():
        r_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
        hash_val = hashlib.sha256(r_uuid)
        return hash_val.hexdigest()


