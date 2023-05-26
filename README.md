# jameshall-ninja-site
The source code for jameshall.ninja is a collection of files that are used to create and maintain the jameshall.ninja website. The code is written in a variety of languages, including Python, HTML, CSS, and JavaScript. The code is open source and is available for anyone to use.

## Features

This project is a full-stack solution that uses Google Cloud Firestore, JWT, and cookies for secure user authentication. It also offers utilities for user registration, dashboard creation, and blogging. The framework is customizable and can be tweaked to meet the needs of any project.

## Getting Started

### Prerequisites

Ensure you have Python 3.x installed on your system. You can download Python [here](https://www.python.org/downloads/).

### Installation

To start using, clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/jameseh/jameshall-ninja-site.git
cd jameshall-ninja-site
pip install -r requirements.txt
```

### Running the Application

From the project directory, you can start the application by using either of the following commands:

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

- `app.py`: Contains routes and the main app logic.
- `config.py`: Houses configuration variables. (Additional configuration options are planned for future updates.)
- `utils/`: Holds utility files like `auth.py`, `security.py`, and `db.py`.
- `public/`: Contains HTML, CSS, and JavaScript files. Files with `base` in the name are global, while others extend various pages.

## Dependencies

* [Sanic](https://sanic.readthedocs.io/en/latest/)
* [Jinja2](https://jinja.palletsprojects.io/en/2.10.x/)
* [WTForms](https://wtforms.readthedocs.io/en/2.3.x/)
* [pytest](https://docs.pytest.org/en/latest/)
* [bcrypt](https://pypi.org/project/bcrypt/)
* [pyjwt](https://pyjwt.readthedocs.io/en/latest/)
* [cryptography](https://cryptography.io/en/latest/)
* [google-cloud-datastore](https://github.com/googleapis/python-datastore)

jameshall-ninja-site also uses the following CDNs:

* [Google Fonts](https://fonts.google.com/)
* [Font Awesome](https://fontawesome.com/)

## License

jameshall-ninja-site is licensed under the MIT License. See the [LICENSE](/blob/main/LICENSE) file for more information.
