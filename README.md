# mailman
a mail manager for sending mass personalized emails and newsletters

## Usage

To see details on the different commands, type one of the following into the console:
```
python mailman.py -h
python mailman.py --help
```

## Commands

The different commands available are `deliver` and `newsletter`.

### mailman.deliver

The deliver command sends an email to a list of recipients replacing any replacer fields 
(denoted by `${ATTR}` where `ATTR` is an attribute name)
with matching attributes found in the recipient CSV list.

If any replacer fields remain after substitution into the template, an error will be thrown and the email will not be sent.

The deliver command usage is shown:
```
mailman.py deliver [-h] [-p --plaintext] subj CSV PT [HTML]
```
The parameters of the command are:
- `-h` or `--help` provides documentation of the command in console
- `-p` or `--plaintext` sends the emails without an HTML alternative (therefore not requiring an HTML positional argument)
- subj` sets the subject line of the email
- `CSV` is a filepath to the recipient list in a .csv format
- `PT` is a filepath to the plaintext template of the email in a .txt format
- `HTML` is a filepath to the HTML template of the email in a .html format (is required unless `--plaintext` is active)

### mailman.newsletter

The newsletter command sends an email to a list of recipients. 
A data template given by a JSON file determines the content of the template.

The newsletter command usage is shown:
```
mailman.py newsletter [-h] CSV JSON
```
The parameters of the command are:
- `-h` or `--help` provides documentation of the command in console
- `CSV` is a filepath to the recipient list in a .csv format
- `JSON` is a filepath to the JSON file that contains the contents of the newsletter.
