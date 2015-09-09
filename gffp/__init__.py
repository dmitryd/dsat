import dsatutil
import subprocess

def parseArguments():
    """
    Parses arguments
    """
    parser = dsatutil.ArgumentParser(
        description='Publishes the current feature branch'
    )
    parser.add_argument('action', action='store', metavar='gffp', nargs=1, help='Action name')
    return parser.parse_args()


def fetchBranch():
    """
    Fetches current branch name
    """
    process = subprocess.Popen("git branch | grep '^\\* feature/' | awk '{ print $2; }' | awk -v FS=/ '{ print $2; }'", stdout=subprocess.PIPE, shell = True)
    branch = ''
    for line in process.stdout:
        branch = line.strip()
        break
    if branch == '':
        print "Not on a git flow feature branch"
        exit
    return branch


def checkIfPublished(branch):
    """
    Checks if the branch is already published
    """
    process = subprocess.Popen("git br -a -vv | grep " + branch + " | grep '/feature/" + branch + "'", stdout=subprocess.PIPE, shell = True)
    hasRemoteBranch = False
    for line in process.stdout:
        hasRemoteBranch = True
        break
    return hasRemoteBranch


def pushToGit(branch):
    """
    Pushes the branch to git normally
    """
    process = subprocess.Popen("git push origin feature/" + branch, stdout=subprocess.PIPE, shell = True)
    for line in process.stdout:
        print line


def publishToGit(branch):
    """
    Publishes the branch
    """
    process = subprocess.Popen("git flow feature publish " + branch, stdout=subprocess.PIPE, shell = True)
    for line in process.stdout:
        print line


def run():
    """
    Runs the action
    """
    parseArguments()
    branch = fetchBranch()
    if checkIfPublished(branch):
        pushToGit(branch)
    else:
        publishToGit(branch)
