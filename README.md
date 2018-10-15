# backlog_util
チーム横断のタスクを一斉起票したりするのが面倒くさいので、それの省力化を目指す

このレポジトリでは、coreutil的なパッケージの開発を目指す。別レポジトリでこれをラップしたCLIインタフェースの開発を行う。

# Usage

Install dependencies

```bash
cd path-to-this-project-root
pip install .
```

Code snipet

```python
import json
from backlog.util import load_conf
from backlog.base import BacklogAPI


def main():
    """
    Load conf.yml
    """
    conf = load_conf("conf.yml")["backlog"]
    api = BacklogAPI(conf["space"], conf["api_key"])

    """
    Project API
    """
    # list project users
    # https://developer.nulab-inc.com/ja/docs/backlog/api/2/get-project-list/
    print("# list project users")
    users = api.project.users("SampleProject")
    print(json.dumps(users.json(), indent=2))


    """
    Wiki API
    """
    # list wikis
    # https://developer.nulab-inc.com/ja/docs/backlog/api/2/get-wiki-page-list/
    print("# list wikis")
    wikis = api.wiki.list("SampleProject")
    print(json.dumps(wikis[0], indent=2))

    # get attachment
    # https://developer.nulab-inc.com/ja/docs/backlog/api/2/get-issue-attachment/
    print("# get attachment")
    wiki = [w for w in api.wiki.list("SampleProject") if len(w["attachments"]) > 0][0]
    attachment = api.wiki.get_attachment(
        wikiId=wiki["id"],
        attachmentId=wiki["attachments"][0]["id"])
    print(json.dumps(attachment), indent=2)


if __name__ == "__main__":
    main()
```


# Contact(Slack internal team)

|key|value|
|:---|:---|
|Channel|#ext-dev-backlog-util|
|Owner|@hashimoto|
