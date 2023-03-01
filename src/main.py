import json
import requests

LCACOLLECT_URL = "https://api.lcacollect.dk/graphql"
# This is the authentication token for LCAcollect. It can either we copied from the Dev Console in the browser after
# logging in or you can use MS's auth package for Python:
# https://github.com/AzureAD/microsoft-authentication-library-for-python
TOKEN = "Bearer ey..."


def main():
    user = get_user_account()
    create_project(user.get("id"))
    list_projects()


def list_projects():
    """List the projects you have access to on LCAcollect"""

    query = """
      query {
        projects {
          name
          id
        }
      }
    """

    headers = {"content-type": "application/json", "Authorization": TOKEN}
    response = requests.post(LCACOLLECT_URL, headers=headers, json={"query": query})
    response.raise_for_status()

    data = response.json()
    print("PROJECTS:\n")
    print(json.dumps(data["data"]["projects"], indent=4))


def get_user_account():
    """Get your user account for LCAcollect"""

    query = """
      query {
        account {
          name
          id
        }
      }
    """

    headers = {"content-type": "application/json", "Authorization": TOKEN}
    response = requests.post(LCACOLLECT_URL, headers=headers, json={"query": query})
    response.raise_for_status()

    data = response.json()
    print("USER:\n")
    print(json.dumps(data["data"]["account"], indent=4))

    return data["data"]["account"]


def create_project(user_id: str):
    """Create a new project on LCAcollect and add an user as project member"""

    query = """
      mutation($name: String!, $userId: String!) {
        addProject(name: $name, members: [{userId: $userId}]) {
          name
          id
        }
      }
    """

    headers = {"content-type": "application/json", "Authorization": TOKEN}
    response = requests.post(LCACOLLECT_URL, headers=headers, json={
        "query": query,
        "variables": {"name": "New Project From API", "userId": user_id}
    })
    response.raise_for_status()

    data = response.json()
    print("NEW PROJECT\n")
    print(json.dumps(data["data"]["addProject"], indent=4))
    print()


if __name__ == "__main__":
    main()
