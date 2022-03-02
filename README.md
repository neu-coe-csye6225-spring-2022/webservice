# CSYE 6225 Web Service

*Yiqing Huang 001525629 huang.yiqin@northeastern.edu*



## Prerequisites

- Linux, macOS, Windows
- Python 3.6-3.8



## Usage

#### 1. Install all the necessary packages

```bash
pip install django djangorestframework bcrypt mysqlclient
```

#### 2. Deploy the web application

```bash
python manage.py runserver
```

#### 3. Run Unit Test (Optional)

```bash
python manage.py test
```

#### 4. Demo

Please refer to the [API documentation](https://app.swaggerhub.com/apis-docs/spring2022-csye6225/app/a02#/).

For the authenticated APIs, the application only supports *Token-Based authentication*. Since at the current stage, the authentication for a user can only be obtained manually. The following instructions tell how to get a *token*.

 1. Open *Django* Shell

    ```shell
    python manage.py shell 
    ```

 2. Enter the code line by line

    ```python
    >>>from django.contrib.auth import get_user_model
    
    >>>from rest_framework.authtoken.models import Token
    
    >>>User = get_user_model()
    <QuerySet [<User: admin>, <User: jane.doe@example.com>]>
    
    >>>token = Token.objects.create(user=User.objects.all()[1])  # Choose the one you want to create auth
    
    >>>token.key
    xxxxxxxx (your token)
    ```

    
