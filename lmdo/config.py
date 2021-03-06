"""
lmdo system configuration
"""

# File for lmdo project config data
PROJECT_CONFIG_TEMPLATE = 'lmdo.yml.j2'
PROJECT_CONFIG_FILE = 'lmdo.yml'

# PIP
PIP_VENDOR_FOLDER = 'vendored'
PIP_REQUIREMENTS_FILE = 'requirements.txt'

# Cloudformations
CLOUDFORMATION_DIRECTORY = 'cloudformation'
CLOUDFORMATION_TEMPLATE_ALLOWED_POSTFIX = ['json', 'template', '.yml']
CLOUDFORMATION_TEMPLATE = 'main'
CLOUDFORMATION_PARAMETER_FILE = 'params.json'

# Lambda
LAMBDA_MEMORY_SIZE = 128
LAMBDA_RUNTIME= 'python2.7'
LAMBDA_TIMEOUT = 180

# Files and directories excluding from packaging
LAMBDA_EXCLUDE= {
    'dir': [
        'tests',
        '*boto*',
        '*.git*',
        '.cache',
        'cloudformation',
        'swagger',
    ],
    'file': [
        'lmdo.yml',
        '*.pyc',
        '.gitignore',
        '.coverage',
        '.travis.yml',
        'requirement.txt',
    ]
}

LAMBDA_DEFAULT_ASSUME_ROLES = [
    "apigateway.amazonaws.com", 
    "lambda.amazonaws.com", 
    "events.amazonaws.com", 
    "ec2.amazonaws.com"
]

# Apigateway
SWAGGER_DIR = 'swagger'
SWAGGER_FILE = 'apigateway.json'

# S3
S3_UPLOAD_EXCLUDE = {
    'dir': [
        '*.git*',
        '.gitignore',
        '*.md'
    ],
    'file': [
        '.DS_Store'
    ]
}

# Mandatory keys in the config file
CONFIG_MANDATORY_KEYS= [
    'User', 
    'Stage', 
    'Service',
    'Profile'
]
    
# Template
IAM_ROLE_APIGATEWAY_LAMBDA = 'apigateway_lambda_role.json'
IAM_POLICY_APIGATEWAY_LAMBDA_INVOKE = 'iam_policy_lambda_invoke.json'
IAM_ROLE_LAMBDA_ASSUME = 'default_lambda_assume_role.json'
IAM_POLICY_LAMBDA_DEFAULT = 'default_lambda_role_policy.json'
APIGATEWAY_SWAGGER_WSGI = 'wsgi_apigateway.json'

DEFAULT_ASSUME_ROLES = [
    "apigateway.amazonaws.com", 
    "lambda.amazonaws.com", 
    "events.amazonaws.com", 
    "ec2.amazonaws.com"
]
