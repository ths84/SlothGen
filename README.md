# SlothGen 🦥

SlothGen 🦥 randomly and slowly combines two first names and one last name. ☕️

## Installation

Python > 3.6

### Clone Repository

```
git clone https://github.com/ths84/SlothGen.git
cd SlothGen
```

### Install into a Python virtual environment:

    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    
## 🦥 Generating some names

![SlothGen](slothgen.png?raw=true "SlothGen Intro")

Upon starting SlothGen you are able to create a fresh database or work with an existing one. 
The database will provide first and last names to generate a new (and never seen before) name.
<br><br>A sample database with the filename **"test_db.xlsx"** is already provided and ready to use.
If you want to create a fresh database, SlothGen will first scrape some names from different websites (see below). 
The scraping process will take some time...

## Websites used for building a database

The following websites are currently scraped for building a database for names:

- https://www.vorname.com
- https://de.wiktionary.org/wiki/Verzeichnis:Deutsch/Namen
- https://www.familyeducation.com
