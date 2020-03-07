# CAPS Command Line Interface
A repository to discuss, define and implement an approach for easily uploading models


### Prerequisites

What things you need to install to run the software and how to install them

```
Python3
```

### Installing

A step by step series of examples that tell you how to get a development env running

#### MacOS and Linux Guide for creating virtual environment
Create a python3 virtual environment from the parent directory of this project
```
python3 -m venv caps-cli-dev
```

Activate the python3 virtualenv
```
source caps-cli-dev/bin/activate
```

#### Windows Guide for creating virtual environment
Create a python3 virtual environment from the parent directory of this project
```
py -m venv caps-cli-dev
```

Activate the python3 virtualenv
```
.\caps-cli-dev\Scripts\activate
```

For more info [visit this](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### Building the Project
Now navigate to the project folder (ModelCatalogInsertion)
```
cd ModelCatalogInsertion
```


Build the project
```
python3 setup.py install
```

#### Running the Project
Help functionality in the CLI
```
caps-cli --help
```

Use this command to know the details of each CLI function (options, arguments)
```
caps-cli <initialize, push, validate> --help
```

Run this command to test the template creation functionality (with 2 inputs, 3 outputs and 1 parameter)
```
caps-cli initialize -i 2 -o 3 -p 1
```
Running the above command will generate a yaml outline. By default this will create the outline in the current directory, use `-d path/to/location` to speciy a location. By default the yaml will be named `example_yaml.yaml`, user can also use `-d fileName.yaml` to name the output (note the user must specify .yaml after the name. Otherwise the program does not know if it is a directory or filename). By default this will not override an existing file if they share the same name. use flag `-f` to force override.



Run this command to transform the input YAML into a postable JSON object
```
caps-cli push <path_of_yaml_file_from_root_of_the_project>
```

Run this command to validate the JSON schema obtained by using the above command
```
caps-cli validate <path_of_json_file_from_root_of_the_project>
```

Use this command to deactivate the python virtual environment
```
deactivate
```
