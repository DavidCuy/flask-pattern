# Debugger config

## Flask debugger

In order to configure a debugger for flask application. You'll need to create a file in the next directory `/code/.vscode/launch.json` with the next content:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "api",
                "FLASK_ENV": "development"
            },
            "args": [
                "run",
                "--no-debugger"
            ],
            "jinja": true
        }
    ]
}
```

## Docker debugger

At first, make sure you have already installed docker engine. After that, create a new file in the next directory `/code/.vscode/tasks.json` with the next content:

```json
{
    "version": "2.0.0",
    "tasks": [{
            "type": "docker-run",
            "label": "docker-run: debug",
            "dependsOn": ["docker-build"],
            "dockerRun": {
                "containerName": "maxitransfer-api",
                "image": "maxitransfer:latest",
                "env": {
                    "FLASK_APP": "api",
                    "FLASK_ENV": "development"
                },
                "volumes": [
                    {
                        "containerPath": "/code",
                        "localPath": "${workspaceFolder}"
                    }
                ],
                "ports": [{
                    "containerPort": 5000,
                    "hostPort": 5000
                }]
            },
            "python": {
                "args": ["run", "--host", "0.0.0.0", "--port", "5000"],
                "module": "flask"
            }
        },
        {
            "label": "docker-build",
            "type": "docker-build",
            "dockerBuild": {
                "context": "${workspaceFolder}",
                "dockerfile": "${workspaceFolder}/Dockerfile.dev",
                "tag": "maxitransfer:latest"
            }
        }
    ]
}
```

Then in the `/code/.vscode/launch.json` add the next content or if you already have a `launch.json` file, just add the next element to the `configurations` list

```json
{
    "version": "0.2.0",
    "configurations": [
        ...,
        {
            "name": "Docker: Python Flask",
            "type": "docker",
            "request": "launch",
      
            "preLaunchTask": "docker-run: debug",
            "python": {
              "pathMappings": [
                {
                  "localRoot": "${workspaceFolder}",
                  "remoteRoot": "/code"
                }
              ],
              "projectType": "flask"
            },
            "dockerServerReadyAction": {
              "action": "openExternally",
              "pattern": "Running on (http?://\\S+|[0-9]+)",
              "uriFormat": "%s://localhost:%s/"
            }
        }
    ]
}
```

## UnitTest

If you want to run some unit test in vscode. You'll need to add the next file: `/code/.vscode/settings.json` with the next content:

```json
{
    "python.testing.unittestArgs": [
        "-v",
        "-s",
        "./tests",
        "-p",
        "*test.py"
    ],
    "python.testing.pytestEnabled": false,
    "python.testing.unittestEnabled": true
}
```
