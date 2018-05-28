# Laputa with GraphQL

## Installation

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python app.py
```

Go to `http://localhost:5000/` and enjoy !

query example:
```
{
 	allUsers{
    name
    createdBy {
      name
    }
    creationDate
    createdUsers {
      name
    }
    passwordEmailSent
    role
    groups {
      name
    }
    privileges {
      smallApp {
        id
        name
      }
      privilege
    }
  }
}
```

mutation examples:
```
mutation {
  updateUser(name:"eric@test.com", groups: ["manager", "developer", "mamou"]) {
    ok
  }
}

mutation{
  createGroup(name: "mamou") {
    ok
  }
}
```
## Change data
You can use graphQL mutations or directly change the fixtures added in `database.py`
