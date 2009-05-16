#!/usr/bin/python

# Repo lives in ~evanm/projects/git-try -- feel free to send patches.

import getpass
import optparse
import os
import subprocess
import tempfile
import traceback
import urllib
import sys


def Backquote(cmd):
  """Like running `cmd` in a shell script."""
  return subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0].strip()


def GetTryServerConfig():
  """Returns the dictionary of try server options or None if they
  cannot be found."""
  script_path = 'tools/tryserver/tryserver.py'
  root_dir = Backquote(['git', 'rev-parse', '--show-cdup'])
  try:
    script_file = open(os.path.join(root_dir, script_path))
  except IOError:
    return None
  locals = {}
  try:
    exec(script_file, locals)
  except Exception, e:
    return None
  return locals


def GetBranchName():
  """Return name of current git branch."""
  branch = Backquote(['git', 'symbolic-ref', 'HEAD'])
  if not branch.startswith('refs/heads/'):
    raise "Couldn't figure out branch name"
  branch = branch[len('refs/heads/'):]
  return branch


def GetPatchName():
  """Construct a name for this patch."""
  short_sha = Backquote(['git', 'rev-parse', '--short=4', 'HEAD'])
  return GetBranchName() + '-' + short_sha


def GetRevision():
  """Get the latest Subversion revision number."""
  for line in Backquote(['git', 'svn', 'info']).split('\n'):
    if line.startswith('Revision:'):
      return line[len('Revision:'):].strip()
  raise "Couldn't figure out latest revision"


def GetRietveldIssueNumber():
  return Backquote(['git', 'config',
                    'branch.%s.rietveldissue' % GetBranchName()])


def GetRietveldPatchsetNumber():
  return Backquote(['git', 'config',
                    'branch.%s.rietveldpatchset' % GetBranchName()])


def GetMungedDiff(branch):
  """Get the diff we'll send to the try server.  We munge paths to match svn."""
  # Make the following changes:
  # - Prepend "src/" to paths as svn is expecting
  # - In the case of added files, replace /dev/null with the path to the file
  #   being added.
  output = []
  if not branch:
    # Try to guess the upstream branch.
    branch = Backquote(['git', 'cl', 'upstream'])
  diff = subprocess.Popen(['git', 'diff-tree', '-p', '--no-prefix',
                           branch, 'HEAD'],
                          stdout=subprocess.PIPE).stdout.readlines()
  for i in range(len(diff)):
    line = diff[i]
    if line.startswith('--- /dev/null'):
      line = '--- %s' % diff[i+1][4:]
    elif line.startswith('--- ') or line.startswith('+++ '):
      line = line[0:4] + 'src/' + line[4:]
    output.append(line)

  return ''.join(output)


def GetEmail():
  # TODO: check for errors here?
  return Backquote(['git', 'config', 'user.email'])


def TryChange(args):
  """Put a patch on the try server using SVN."""
  # TODO: figure out a better way to load trychange
  script_path = '../depot_tools/release'
  root_dir = Backquote(['git', 'rev-parse', '--show-cdup'])
  sys.path.append(os.path.join(root_dir, script_path))
  import trychange
  trychange.checkout_root = os.path.abspath(root_dir)
  trychange.TryChange(args, None, False)


def WriteTryDiffHTTP(config, patch_name, diff, options):
  """Put a patch on the try server."""
  params = {
      'user': getpass.getuser(),
      'name': patch_name,
      'patch': diff
  }

  if options.bot:
    params['bot'] = options.bot

  if options.clobber:
    params['clobber'] = 'true'

  url = 'http://%s:%s/send_try_patch' % (config['try_server_http_host'],
                                         config['try_server_http_port'])
  connection = urllib.urlopen(url, urllib.urlencode(params))
  response = connection.read()
  if (response != 'OK'):
    print "Error posting to", url
    print response
    assert False


if __name__ == '__main__':
  parser = optparse.OptionParser(
      usage='git try [branch]',
      description='Upload the current diff of branch...HEAD to the try server.')
  parser.add_option("-b", "--bot",
                    help="Force the use of a specific build slave (eg mac, "
                         "win, or linux)")
  parser.add_option("-c", "--clobber", action="store_true",
                    help="Make the try run use be a clobber build")
  (options, args) = parser.parse_args(sys.argv)

  branch = None
  if len(args) > 1:
    branch = args[1]

  patch_name = GetPatchName()
  diff = GetMungedDiff(branch)

  # Send directly to try server if we can parse the config, otherwise
  # upload via SVN.
  config = GetTryServerConfig()
  if config is not None:
    print "Sending %s using HTTP..." % patch_name
    WriteTryDiffHTTP(config=config, patch_name=patch_name, diff=diff,
                     options=options)
  else:
    print "Sending %s using SVN..." % patch_name

    # Write the diff out to a temporary file
    diff_file = tempfile.NamedTemporaryFile()
    diff_file.write(diff)
    diff_file.flush()

    email = GetEmail()
    user = email.partition('@')[0]
    args = [
        '--use_svn',
        '--svn_repo', 'svn://svn.chromium.org/chrome-try/try',
        '-u', user,
        '-e', email,
        '-n', patch_name,
        '-r', GetRevision(),
        '--diff', diff_file.name,
    ]
    if options.bot:
      args.extend(['--bot', options.bot])
    if options.clobber:
      args.append('--clobber')
    if GetRietveldPatchsetNumber():
      args.extend([
          '--issue', GetRietveldIssueNumber(),
          '--patchset', GetRietveldPatchsetNumber(),
      ])
    TryChange(args=args)
