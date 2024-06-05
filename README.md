# Semgrep Rules Parser
Parses needed ruleset from semgrep rules registry using python default libraries. Preferable python version - **3.11.3**

## Usage
You can either change corresponding variables in code
```py
...
def main() -> None:
    token   = "AUTH_TOKEN"
    ruleset = "RULESET"
    output  = "OUTPUT_FILE"
...
```
or pass these parameters in terminal
```sh
python3 main.py AUTH_TOKEN RULESET OUPUT_FILE
```

Example:
```sh
python3 main.py eyJ...OnE golang rules.yml
```

## How to get authorization token?
1. Go to [Semgrep Rules Registry](https://semgrep.dev/explore) and log into your account.
2. Then open DevTools (`F12` or `ctrl`+`shift`+`I`)
3. Go to `Network` tab and reload page
4. Find any request that has been sent to `semgrep.dev/api` and find `Authorization` header
5. Now you have authorization token!