import os

import Environment as env

config = {
    'local': {
        'initial_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "storage", "local")
    },
    's3': {
        "default": {
            #"aws_access_key": env.AWS_ACCESS_KEY,
            #"aws_secret_key": env.AWS_SECRET_KEY,
            #"bucket_name": env.BUCKET_NAME
        },
        "other_config": {

        }
    }
}