#-*- coding: utf-8 -*-

from fabric.api import *

import codecs
import json
import requests

@task
def export(GITHUB_USER, GITHUB_PASSWORD, REPO):
    AUTH = (GITHUB_USER, GITHUB_PASSWORD)

    ISSUES_FOR_REPO_URL = 'https://api.github.com/repos/%s/issues?state=all' % REPO
    issues = requests.get(ISSUES_FOR_REPO_URL, auth=AUTH)

    def get_comments(issue):
        ret = issue.copy()
        if issue["comments"] > 0:
            COMMENTS_URL = issue["comments_url"]
            comments = requests.get(COMMENTS_URL, auth=AUTH)
            ret["comments_body"] = comments.json()
        else:
            ret["comments_body"] = []
        return ret

    output = [get_comments(issue) for issue in issues.json()]

    output_file_name = REPO.replace("/", "---") + ".json"
    w = codecs.open(output_file_name, "w", "utf-8")
    json.dump(output, w, indent=2, ensure_ascii=False)
    w.close()

