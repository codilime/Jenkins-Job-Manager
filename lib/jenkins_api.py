import netrc
import jenkins


def get_jenkins_server(jenkins_base_address: str = 'localhost:8080', 
                       username: str = None, 
                       api_token: str = None) -> jenkins.Jenkins:
    """
    https://python-jenkins.readthedocs.io/en/latest/examples.html
    """
    if not (username and api_token):
        # Loading credentials from the .netrc file.
        netrc_credentials = netrc.netrc()
        username, _, api_token = netrc_credentials.authenticators(jenkins_base_address)

    jenkins_full_address = f'{jenkins_base_address}/jenkins'
    jenkins_project_url = f'http://{jenkins_full_address}'

    jenkins_server = jenkins.Jenkins(jenkins_project_url, username, api_token)
    return jenkins_server
