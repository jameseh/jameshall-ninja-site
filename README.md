SanicPlus - Simple and Modern Web Frontend for Sanic

SanicPlus aims to provide an easy-to-use, modern, and simple frontend solution built on top of the high-performance Sanic web framework. Written in Python, SanicPlus is designed to streamline the process of building web applications by handling frontend rendering using HTML, CSS, and JavaScript. Furthermore, it offers out-of-the-box features such as user authentication using JWT and cookies.

## Features

SanicPlus distinguishes itself with the following features:

- Full-Stack Solution: Handles both frontend (HTML, CSS, JavaScript) and backend (Python) elements.
- Database Interactions: Utilizes SQLAlchemy to interact with the database.
- User Authentication: Employs JWT and cookies for secure user authentication.
- Extensible User Features: Offers utilities for user registration, dashboard creation, and blogging.
- Customizable: Offers several ways to tweak the framework according to the needs of the project.
- (Coming Soon) Unit Testing: Will offer built-in unit testing support.

## Getting Started

### Prerequisites

Ensure you have Python 3.x installed on your system. You can download Python [here](https://www.python.org/downloads/).

### Installation

To start using SanicPlus, clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/jameseh/sanicplus.git
cd sanicplus
pip install -r requirements.txt
```

### Running the Application

From the SanicPlus directory, you can start the application by using either of the following commands:

```bash
sanic app:app --host 0.0.0.0 --port 8080
```
or
```bash
python app.py --host 0.0.0.0 --port 8080
```

After running one of the above commands, navigate to http://localhost:8080 to view your application.

For more details on running Sanic applications, including different options and configurations, please refer to the official [Sanic Running Guide](https://sanic.dev/en/guide/deployment/running.html).

## Customization

Customize SanicPlus to suit your project requirements:

- `app.py`: Contains routes and the main app logic.
- `config.py`: Houses configuration variables. (Additional configuration options are planned for future updates.)
- `models/`: Stores model schemas.
- `utils/`: Holds utility files like `auth.py`, `security.py`, and `db.py`.
- `public/`: Contains HTML, CSS, and JavaScript files. Files with `base` in the name are global, while others extend various pages.

## Dependencies

SanicPlus depends on the following libraries:

* [Sanic](https://sanic.readthedocs.io/en/latest/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [Jinja2](https://jinja.palletsprojects.io/en/2.10.x/)
* [WTForms](https://wtforms.readthedocs.io/en/2.3.x/)
* [pytest](https://docs.pytest.org/en/latest/)
* [bcrypt](https://pypi.org/project/bcrypt/)
* [pyjwt](https://pyjwt.readthedocs.io/en/latest/)
* [cryptography](https://cryptography.io/en/latest/)

SanicPlus also uses the following CDNs:

* [Google Fonts](https://fonts.google.com/)
* [Font Awesome](https://fontawesome.com/)

## License

SanicPlus is licensed under the MIT License. See the [LICENSE](/blob/main/LICENSE) file for more information.
