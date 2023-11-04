# 0x00. Personal data

`Back-end`
`Authentification`

## Learning Objectives

- At the end of this project, you are expected to be able to explain to anyone, without the help of Google:

- What you should learn from this project:

- Examples of Personally Identifiable Information (PII)
- How to implement a log filter that will obfuscate PII fields
- How to encrypt a password and check the validity of an input password
- How to authenticate to a database using environment variables

## Requirements

- All your files should end with a new line
- A README.md file, at the root of the folder of the project, is mandatory
- The first line of all your files should be exactly #!/usr/bin/env python3
- Your code should use the pycodestyle style (version 2.5.*)
- All your files must be executable
- The length of your files will be tested using wc
- All your modules should have a documentation (python3 -c 'print(__import__("my_module").__doc__)')
- All your classes should have a documentation (python3 -c 'print(__import__("my_module").MyClass.__doc__)')
- All your functions (inside and outside a class) should have a documentation (python3 -c 'print(__import__("my_module").my_function.__doc__)' and python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)')
- A documentation is not a simple word, it’s a real sentence explaining what’s the purpose of the module, class or method (the length of it will be verified)

## Tasks

0. Regex-ing

- Write a function called filter_datum that returns the log message obfuscated:

- Arguments:
    - fields: a list of strings representing all fields to obfuscate
    - redaction: a string representing by what the field will be obfuscated
    - message: a string representing the log line
    - separator: a string representing by which character is separating all fields in the log line (message)
- The function should use a regex to replace occurrences of certain field values.
- filter_datum should be less than 5 lines long and use re.sub to perform the substitution with a single regex.

```
bob@dylan:~$ cat main.py
#!/usr/bin/env python3
"""
Main file
"""

filter_datum = __import__('filtered_logger').filter_datum

fields = ["password", "date_of_birth"]
messages = ["name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;", "name=bob;email=bob@dylan.com;password=bobbycool;date_of_birth=03/04/1993;"]

for message in messages:
    print(filter_datum(fields, 'xxx', message, ';'))

bob@dylan:~$
bob@dylan:~$ ./main.py
name=egg;email=eggmin@eggsample.com;password=xxx;date_of_birth=xxx;
name=bob;email=bob@dylan.com;password=xxx;date_of_birth=xxx;
bob@dylan:~$
```

# Logging - Logging facility for Python

- The logging module defines functions and classes which implement a flexible event logging system for applications and libraries.

- The key benefit of having the logging API provided by a standard library module is that all Python modules can participate in logging, so your application log can include your own messages integrated with messages from third-party modules.

- The module provides a way for applications to configure different log handlers and different log levels for individual modules.

- The basic classes defined by the module, together with their functions, are described below.
    - Loggers expose the interface that application code directly uses.
    - Handlers send the log records (created by loggers) to the appropriate destination.
    - Filters provide a finer grained facility for determining which log records to output.
    - Formatters specify the layout of log records in the final output.

- Logging is a means of tracking events that happen when some sw runs. The software’s developer adds logging calls to their code to indicate that certain events have occurred. An event is described by a descriptive message which can optionally contain variable data (i.e. data that is potentially different for each occurrence of the event). Events also have an importance which the developer ascribes to the event; the importance can also be called the level or severity.

#### When to use logging: Tasks you want to perform with logging

- The logging module provides a nice API to the python developer. It’s not the only one, but it’s well supported and rich in features. It’s also part of the standard library, which means that it’s always available to you. The logging module is intended to be thread-safe without any special work needing to be done by its clients. It is based on the C version of syslog, and retains the same API. As such, it is backward compatible with syslog messages, while providing a number of extensions to syslog.

- Display console output for ordinary usage of a command line script -> use `print()`
- Report events that occur during normal operation of a program (e.g. for status monitoring or fault investigation) -> use `logging.info()` or `logging.debug()`
- Issue a warning regarding a particular runtime event -> use `logging.warning()`
    - `warnings.warn()`: in library code if the issue is avoidable and the client application should be modified to eliminate the warning.
    - `logging.warning()`: if there is nothing the client application can do about the situation, but the event should still be noted.
- Report an error regarding a particular runtime event -> Raise an exception
- Report suppression of an error without raising an exception or terminating the program -> use `logging.error()`

- The logging functions are named after the level or severity of the events they are used to track. The standard levels and their applicability are described below (in increasing order of severity):

- `DEBUG`: Detailed information, typically of interest only when diagnosing problems.
- `INFO`: Confirmation that things are working as expected.
- `WARNING`: An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
- `ERROR`: Due to a more serious problem, the software has not been able to perform some function.
- `CRITICAL`: A serious error, indicating that the program itself may be unable to continue running.

### Filter

- Apply this logger's to the record and return `True` if the record is to be processed. The filters are
consulted in turn, until one of them returns a non-zero value for `filter()`, if none of them return a false value, the record will be processed (passed onto handlers). If one returns a false value, no further processing of the record occurs.

## Filter Objects

- Filter objects are used to perform arbitrary filtering of LogRecords. Loggers and Handlers can optionally use Filter objects to filter records as desired. The base filter class only allows events which are below a certain point in the logger hierarchy. For example, a filter initialized with "A.B" will allow events logged by loggers "A.B", "A.B.C", "A.B.C.D", "A.B.D" etc. but not "A.BB", "B.A.B" etc. If initialized with the empty string, all events are passed.

`class logging.Filter(name='')`
- Return a new instance of the Filter class. If no name is specified, it defaults to the empty string, which will result in a filter that allows all events through.

`filter(record)`: Determine if the specified record is to be logged. Is the specified record to be logged? Returns zero for no, nonzero for yes. If deemed appropriate, the record may be modified in-place by this method.

- Note that filters attached to handlers are consulted before an event is emitted by the handler, whereas filters attached to loggers are consulted whenever an event is logged (using debug(), info(), etc.). This means that events which have been generated by descendant loggers will not be filtered by a logger's filter setting, unless the filter has also been applied to those descendant loggers.
## What is Personally identifiable information (PII)?

- PII is any information about an individual maintained by an agency, including (1) any information that can be used to distinguish or trace an individual‘s identity, such as name, social security number, date and place of birth, mother‘s maiden name, or biometric records; and (2) any other information that is linked or linkable to an individual, such as medical, educational, financial, and employment information.

- However, the line between PII and other kinds of information is blurry. As stressed by the US General Services Administration, the “definition of PII is not anchored to any single category of information or technology. Rather, it requires a case-by-case assessment of the specific risk that an individual can be identified”. 

## Examples of PII

- The following are examples of PII that can be used to identify an individual. Please note that this list is not exhaustive.

- (1) Full name
- (2) National identification number
- (3) IP address (in some cases)
- (4) Vehicle registration plate number
- (5) Driver's license number
- (6) Face, fingerprints, or handwriting
- (7) Credit card numbers
- (8) Digital identity
- (9) Date of birth

- NIST states that linked information can be “Asset information, such as Internet Protocol (IP) or Media Access Control (MAC) address or other host-specific persistent static identifier that consistently links to a particular person or small, well-defined group of people”. That means cookies and device ID fall under the definition of PII.

- Linkeable  information is indirect and on its own may not be able to identify a person, but when combined with another piece of information could identify, trace or locate a person. 

- Here are some examples that can be considered as linkable information:

- (1) Telephone number
- (2) Email address
- (3) Social security number (SSN)
- (4) Physical address
- (5) Maiden name
- (6) Alias

### What's non-PII?

- Non-Personally identifiable information (non-PII) is data that cannot be used on its own to trace, or identify a person. Examples of non-PII include, but are not limited to:

- (1) Aggregated statistics on the use of product / service
- (2) Browser type
- (3) OS
- (4) Referring / exit pages and URLS.
- (5) Partially or fully masked IP addresses

- However, the classification of PII and non-PII is vague. Moreover, NIST doesn't reference cookie IDs and device IDs, so many AdTech companies, advertisers, and publishers consider them as non-PII.

-  As we’ll see, this is in contrast to the definition of personal data, which treats such digital tackers as information that could identify an individual.

## What is personal data?

- As defined by the GDPR, personal data is `any information relating to an identified or identifiable natural person (‘data subject’); an identifiable natural person is one who can be identified, directly or indirectly, in particular by reference to an identifier such as a name, an identification number, location data, an online identifier or to one or more factors specific to the physical, physiological, genetic, mental, economic, cultural or social identity of that natural person`.

- This definition applies not only to a person’s name and surname, but to details that could identify that person. That’s the case when, for instance, you’re able to identify a visitor returning to your website with the help of a cookie or login information. 

- Under the GDPR you can consider cookies as personal data because `Natural persons may be associated with online identifiers provided by their devices, applications, tools and protocols, such as internet protocol addresses, cookie identifiers or other identifiers such as radio frequency identification tags. This may leave traces which, in particular when combined with unique identifiers and other information received by the servers, may be used to create profiles of the natural persons and identify them.`

- And the definition of personal data covers various pieces of information, including:

- (1) Transactional history
- (2) IP address
- (3) Cookie ID
- (4) Browser fingerprint
- (5) Posts on social media

- Basically, it's any info relating to an individual or identifiable person, directly or indirectly.

## What's non-personal data?

- Following the GDPR provisions, non-personal data is data that won't let you identify an individual. It's any information that doesn't relate to an identified or identifiable person.(Anonymous data).

`The principles of data protection should therefore not apply to anonymous information, namely information which does not relate to an identified or identifiable natural person or to personal data rendered anonymous in such a manner that the data subject is not or no longer identifiable.`

- Other examlpes of non-personal data include:

- (1) Generalized data, e.i. age range e.g. 20-40
- (2) Aggregated data, e.g. 1000 people visited a website
- (3) Aggregated statistics on the use of a product or service
- (4) Partially or fully masked IP addresses

