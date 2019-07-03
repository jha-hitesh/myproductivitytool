# My Productivity Tool

A simple app to manage projects and tasks

## Getting Started

Clone this repo on your local system. 
Create a virtual environment for your project (Recommended)
give execute permission to local.sh file (Recommended)

### Prerequisites

Once you are ready install requirements

```
pip install -r requirements.txt
```

Migrate the models using
```
./local.sh migrate_models
```
OR 
```
python manage.py makemigrations common project
python manage.py migrate
```

### Running

To run the server

```
./local.sh up
```
OR
```
python manage.py runserver
```

### Other helpful commands from local.sh

* django shell: ./local.sh shell
* collectstatic: ./local.sh collectstatic
* deletemigrations : ./local.sh deletemigrations

## Running the tests

 work in progress

## Deployment To Heroku

* follow this guide
  https://devcenter.heroku.com/articles/git


## Authors

* **Hitesh Jha** - *Initial work*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* myself :)
