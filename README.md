To run the script You will need to install dependencies:

```
python3 -m venv myenv
source myenv/bin/activate
pip install requests
python3 task.py --url http://google.com --timeout 5 --retries 5 --sleep 5
```

url: target url

timeout: request timeout in seconds, default 10

retries: number of request retries, default 3

sleep: pause between retries in seconds, default 3


Tested on macos/linux
