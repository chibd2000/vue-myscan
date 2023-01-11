import datetime
import random

from module.asynchttp import AsyncFetcher
from module.attributedict import AttributeDict
from module.database import GithubDB
import asyncio
import aiohttp
import time

from utils.conf_reader import get_database_conf, get_github_conf, get_celery_conf

"""
实现：github monitor 主要实现了对于想要跟踪漏洞的项目的commit记录监控展示以及收发信息提醒的实现
为什么要写这个？
- 主要的原因是之后的工作更多的需要追漏洞的细节，所以这边实现了这个功能然后给自己使用

不太喜欢看别人的代码再去写，因为看别人的代码比较累，自己还是更愿意先用自己的思路去实现一次，然后还有什么可以改正的再去参考别人代码
"""


class GithubError(Exception):
    pass


class GithubTokenError(GithubError):
    def __init__(self, message):
        self.message = message


class GithubLimitError(GithubError):
    def __init__(self, message):
        self.message = message


class GithubGrammarError(GithubError):
    def __init__(self, message):
        self.message = message


class GithubMonitor:
    def __init__(self):
        self.source = 'Base'
        self._verify_addr = 'https://api.github.com/user'
        self._apis = get_github_conf()['api']
        self.branch_addr = 'https://api.github.com/repos/{}/branches'
        self.commit_addr = 'https://api.github.com/search/commits?q={}'
        self.issue_addr = 'https://api.github.com/search/issues?q={}'
        self.request_limit = 1

        self._init_db()

    def _init_db(self):
        db_conf = get_database_conf()
        self.db_conn = GithubDB(db_conf)

    def time_format(self):
        return time.strftime("%Y-%m-%d", time.localtime(int(time.time())-86400))

    async def get_fetch_json(self, session, url, headers=None):
        response = await AsyncFetcher.fetch_response(session=session, url=url, json=True, headers=headers)
        ret_json = await response.json(encoding='utf-8')
        if response.status == 422:
            raise GithubGrammarError('commit grammar error') from None
        elif response.status == 403:
            raise GithubLimitError('request limit error') from None
        else:
            return ret_json

    async def verify_api_available(self):
        try:
            api_list = self._apis.split(',')
            headers = {'Accept': 'application/vnd.github+json',
                       'Authorization': 'Bearer {}'.format(api_list[random.randint(0, len(api_list) - 1)]),
                       'X-GitHub-Api-Version': '2022-11-28'}
            async with aiohttp.ClientSession() as session:
                response = await AsyncFetcher.fetch_response(session=session, url=self._verify_addr, headers=headers)
                if response.status == 200:
                    return True, headers
                elif response.status == 401:
                    raise GithubTokenError('token error') from None
        except GithubTokenError as e:
            print(e.__str__())
            return False, None
        except Exception as e:
            print(e.__str__())
            return False, None


class GithubCommitStatus:
    ADD = 'added'
    MODIFY = 'modified'
    REMOVE = 'removed'


class GithubCommit(object):
    def __init__(self, monitor_id, commit_sha):
        self.monitor_id = monitor_id
        self.commit_sha = commit_sha
        self.commit_url = ''
        self.commit_message = ''
        self.commit_author_name = ''
        self.commit_author_date = ''
        self.commit_committer_name = ''
        self.commit_committer_date = ''
        # self.commit_file = []
        # self.commit_status = ''
        self.commit_branch = ''
        self.commit_level = ''

    def __eq__(self, other):
        return other == self.commit_sha

    def __hash__(self):
        return self.commit_sha


class GithubIssue(object):
    def __init__(self, monitor_id, id):
        self.issue_id = id
        self.monitor_id = monitor_id
        self.issue_url = ''
        self.issue_create_user = ''
        self.issue_create_date = ''
        self.issue_status = ''
        self.issue_level = ''
        self.issue_title = ''
        self.issue_body = ''
        self.type = ''
        self.is_visited = ''

    def __eq__(self, other):
        return other == self.issue_id

    def __hash__(self):
        return self.issue_id


class GithubKeywordMatcherLevel:
    HIGH = 1
    LOW = 0


class GithubKeywordMatcher:
    name = 'keyword matcher'

    def __init__(self):
        self.keyword = ['bug', 'rce', 'command', 'exec', 'fix', 'inject', 'xxe', 'sql', 'overstep', 'upload',
                        'security', 'vulnerability', 'bypass', '修复', '越权', '漏洞', '命令执行', '权限', '绕过', '注入',
                        '后门', '安全', 'CVE-']

    def check_keyword(self, text: str):
        word_list = text.lower().split(' ')
        if any(word in word_list for word in self.keyword):
            return GithubKeywordMatcherLevel.HIGH
        else:
            return GithubKeywordMatcherLevel.LOW


class GithubBuiler:
    def _date_format(self, date):
        return int(time.mktime(time.strptime(datetime.datetime.strftime(
            datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z") + datetime.timedelta(hours=8), "%Y-%m-%d %H:%M:%S"),
                                             "%Y-%m-%d %H:%M:%S")))


class GithubCommitBuiler(GithubBuiler):
    name = 'commit builder'

    def __init__(self, monitor_id, commit_sha):
        super(GithubCommitBuiler, self).__init__()
        self.github_commit = GithubCommit(monitor_id, commit_sha)
        self.keyword_matcher = GithubKeywordMatcher()

    def build_branch(self, branch_json):
        if len(branch_json) > 0:
            for branch in branch_json:
                if branch['commit']['sha'] == self.github_commit.commit_sha:
                    self.github_commit.commit_branch = branch['name']
        else:
            self.github_commit.commit_branch = '-'

    def build_level(self):
        self.github_commit.commit_level = self.keyword_matcher.check_keyword(self.github_commit.commit_message)

    def build_commit(self, ret_json: dict):
        self.github_commit.commit_url = ret_json['html_url']
        self.github_commit.commit_message = ret_json['commit']['message']
        self.github_commit.commit_author_name = ret_json['commit']['author']['name']
        self.github_commit.commit_author_date = self._date_format(ret_json['commit']['author']['date'])
        self.github_commit.commit_committer_name = ret_json['commit']['committer']['name']
        self.github_commit.commit_committer_date = self._date_format(ret_json['commit']['committer']['date'])

    @property
    def build_info(self):
        return {'commit_sha': self.github_commit.commit_sha, 'monitor_id': self.github_commit.monitor_id,
                'commit_url': self.github_commit.commit_url, 'commit_message': self.github_commit.commit_message,
                'commit_author_name': self.github_commit.commit_author_name,
                'commit_author_date': self.github_commit.commit_author_date,
                'commit_committer_name': self.github_commit.commit_committer_name,
                'commit_committer_date': self.github_commit.commit_committer_date,
                'commit_branch': self.github_commit.commit_branch, 'commit_level': self.github_commit.commit_level,
                'is_visited': 0}

    def build_mail_content(self, target):
        data = '''------------------------\n'''
        data += '仓库:' + str(target) + '\n'
        for index, value in self.build_info.items():
            if index == 'commit_sha' or index == 'monitor_id' or index == 'is_visited':
                continue
            if index == 'commit_url':
                data += '地址:' + str(value) + '\n'
            elif index == 'commit_message':
                # message_value = str(value)[:10] if len(str(value)) > 10 else str(value)
                data += '信息:' + str(value) + '\n'
            elif index == 'commit_author_name':
                data += '作者名称:' + str(value) + '\n'
            elif index == 'commit_author_date':
                data += '作者时间:' + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(value))) + '\n'
            elif index == 'commit_committer_name':
                data += '提交者名称:' + str(value) + '\n'
            elif index == 'commit_committer_date':
                data += '提交时间:' + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(value))) + '\n'
            elif index == 'commit_branch':
                data += '分支:' + str(value) + '\n'
            elif index == 'commit_level':
                vuln_level = '高' if value == 1 else '低'
                data += '风险程序:' + vuln_level + '\n'
        return data


class GithubIssueBuiler(GithubBuiler):
    name = 'issue builder'

    def __init__(self, monitor_id, issue_id):
        super(GithubIssueBuiler, self).__init__()
        self.github_issue = GithubIssue(monitor_id, issue_id)
        self.keyword_matcher = GithubKeywordMatcher()

    def build_level(self):
        self.github_issue.issue_level = self.keyword_matcher.check_keyword(self.github_issue.issue_body) or self.keyword_matcher.check_keyword(self.github_issue.issue_title)

    def build_issue(self, ret_json: dict):
        self.github_issue.issue_url = ret_json['html_url']
        self.github_issue.issue_create_user = ret_json['user']['login']
        self.github_issue.issue_create_date = self._date_format(ret_json['created_at'])
        self.github_issue.issue_status = ret_json['state']
        self.github_issue.issue_title = ret_json['title']
        self.github_issue.issue_body = ret_json['body']
        self.github_issue.type = 'pr' if ret_json['node_id'].startswith('PR') else 'issue'

    @property
    def build_info(self):
        return {'issue_id': self.github_issue.issue_id, 'monitor_id': self.github_issue.monitor_id,
                'issue_url': self.github_issue.issue_url, 'issue_create_user': self.github_issue.issue_create_user,
                'issue_create_date': self.github_issue.issue_create_date,
                'issue_status': self.github_issue.issue_status,
                'issue_level': self.github_issue.issue_level,
                'issue_title': self.github_issue.issue_title,
                'issue_body': self.github_issue.issue_body[:20] if len(self.github_issue.issue_body) > 20 else self.github_issue.issue_body,
                'type': self.github_issue.type,
                'is_visited': 0}

    def build_mail_content(self, target):
        data = '''------------------------\n'''
        data += '仓库:' + str(target) + '\n'
        for index, value in self.build_info.items():
            if index == 'issue_id' or index == 'monitor_id' or index == 'is_visited':
                continue
            if index == 'issue_url':
                data += 'issue地址:' + str(value) + '\n'
            elif index == 'type':
                data += '类型:' + str(value) + '\n'
            elif index == 'issue_title':
                data += '标题:' + str(value) + '\n'
            elif index == 'issue_body':
                data += '内容:' + str(value) + '\n'
            elif index == 'issue_create_user':
                data += '提交用户:' + str(value) + '\n'
            elif index == 'issue_create_date':
                data += '提交时间:' + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(value))) + '\n'
            elif index == 'issue_status':
                data += '状态:' + str(value) + '\n'
            elif index == 'issue_level':
                vuln_level = '高' if value == 1 else '低'
                data += '风险程序:' + vuln_level + '\n'
        return data


class GithubCommitMonitor(GithubMonitor):
    def __init__(self):
        super(GithubCommitMonitor, self).__init__()
        self.commit_query = 'committer-date:>={}+repo:{}'

    def check_repeat(self, exists_commit_result, current_sha):
        return not any(commit['commit_sha'] == current_sha for commit in exists_commit_result)

    async def get_commits(self, monitor_id):
        commit_list = list()
        try:
            self.db_conn.update_last_update_time(int(time.time()), monitor_id)
            session_f, headers = await self.verify_api_available()
            monitor_task = self.db_conn.get_monitor_task_by_monitorid(monitor_id)
            if monitor_task:
                target = monitor_task['target']
                commit_query = self.commit_query.format(self.time_format(), target)
                exists_commit_list = self.db_conn.get_commit_by_monitorid(monitor_id, 'commit_sha')
                async with aiohttp.ClientSession() as session:
                    ret_json = await self.get_fetch_json(session=session, url=self.commit_addr.format(commit_query), headers=headers)
                    attr_dict = AttributeDict(ret_json)
                    if attr_dict.total_count > 0:
                        current_request_count = 0
                        for item in attr_dict.get('items'):
                            if current_request_count >= self.request_limit:
                                break
                            item_dict = AttributeDict(item)
                            if self.check_repeat(exists_commit_list, item_dict.sha):
                                commit_json = await self.get_fetch_json(session=session, url=item_dict.url, headers=headers)
                                gmb = GithubCommitBuiler(monitor_id, commit_json['sha'])
                                gmb.build_commit(commit_json)
                                branch_json = await self.get_fetch_json(session=session, url=self.branch_addr.format(target), headers=headers)
                                gmb.build_branch(branch_json)
                                gmb.build_level()
                                self.db_conn.insert_commit(gmb.build_info)
                                current_request_count += 1
                                commit_list.append(gmb.build_mail_content(target))
        except GithubGrammarError as e:
            print(e.__str__())
        except GithubLimitError as e:
            print(e.__str__())
        except Exception as e:
            print(e.__str__())
        finally:
            self.db_conn.update_next_update_time(int(time.time()) + get_celery_conf()['schedule'], monitor_id)
            return commit_list

    async def monitor(self, monitor_id):
        return await self.get_commits(monitor_id)

    async def all_monitor(self):
        task_list = []
        mointor_tasks = self.db_conn.get_monitor_task_by_monitorid()
        for task in mointor_tasks:
            task_list.append(asyncio.create_task(self.get_commits(task['monitor_id'])))
        return await asyncio.gather(*task_list)


class GithubIssuePrMonitor(GithubMonitor):
    def __init__(self):
        super(GithubIssuePrMonitor, self).__init__()
        self.issue_query = 'created:>={}+repo:{}'

    def check_repeat(self, exists_issue_result, current_id):
        return not any(issue['issue_id'] == current_id for issue in exists_issue_result)

    async def get_issues(self, monitor_id):
        issue_list = list()
        try:
            self.db_conn.update_last_update_time(int(time.time()), monitor_id)
            session_f, headers = await self.verify_api_available()
            monitor_task = self.db_conn.get_monitor_task_by_monitorid(monitor_id)
            if monitor_task:
                target = monitor_task['target']
                issue_query = self.issue_query.format(self.time_format(), target)
                exists_issue_list = self.db_conn.get_issue_by_monitorid(monitor_id, 'issue_id')
                async with aiohttp.ClientSession() as session:
                    ret_json = await self.get_fetch_json(session=session, url=self.issue_addr.format(issue_query), headers=headers)
                    attr_dict = AttributeDict(ret_json)
                    if attr_dict.total_count > 0:
                        current_request_count = 0
                        for item in attr_dict.get('items'):
                            if current_request_count >= self.request_limit:
                                break
                            item_dict = AttributeDict(item)
                            if self.check_repeat(exists_issue_list, item_dict.id):
                                gib = GithubIssueBuiler(monitor_id, item_dict.id)
                                gib.build_issue(item)
                                gib.build_level()
                                self.db_conn.insert_issue(gib.build_info)
                                current_request_count += 1
                                issue_list.append(gib.build_mail_content(target))
        except GithubGrammarError as e:
            print(e.__str__())
        except GithubLimitError as e:
            print(e.__str__())
        except Exception as e:
            print(e.__str__())
        finally:
            self.db_conn.update_next_update_time(int(time.time()) + get_celery_conf()['schedule'], monitor_id)
            return issue_list

    async def monitor(self, monitor_id):
        return await self.get_issues(monitor_id)

    async def all_monitor(self):
        task_list = []
        mointor_tasks = self.db_conn.get_monitor_task_by_monitorid()
        for task in mointor_tasks:
            task_list.append(asyncio.create_task(self.get_issues(task['monitor_id'])))
        return await asyncio.gather(*task_list)


if __name__ == '__main__':
    g = GithubIssuePrMonitor()
    asyncio.get_event_loop().run_until_complete(g.monitor('b77d935349fa074c50ec98673858d6a'))
